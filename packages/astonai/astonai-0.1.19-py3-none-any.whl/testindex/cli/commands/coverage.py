"""
TestIndex coverage command.

This module implements the `testindex coverage` command that displays test coverage gaps.
"""
import os
import sys
import json as json_lib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import datetime
import shutil

import click
from rich.console import Console
from rich.table import Table

from testindex.core.cli.runner import common_options
from testindex.core.config import ConfigModel, ConfigLoader
from testindex.core.exceptions import CLIError
from testindex.core.logging import get_logger
from testindex.analysis.coverage.ingest import ingest_coverage, find_coverage_file, has_coverage_data
from testindex.core.path_resolution import PathResolver
from testindex.cli.utils.env_check import needs_env

# Set up logger
logger = get_logger(__name__)

# Constants
DEFAULT_CONFIG_DIR = ".testindex"
DEFAULT_CONFIG_FILE = "config.yml"
DEFAULT_THRESHOLD = 0  # Default: report only zero coverage (true gaps)


def load_config() -> Dict[str, Any]:
    """Load configuration from file or environment variables.
    
    Fallback order: 
    1. .testindex/config.yml 
    2. environment variables 
    3. defaults
    
    Returns:
        Dict[str, Any]: Configuration dictionary
    
    Raises:
        CLIError: If configuration cannot be loaded
    """
    try:
        # 1. Try to load from .testindex/config.yml
        config_path = Path(DEFAULT_CONFIG_DIR) / DEFAULT_CONFIG_FILE
        if config_path.exists():
            logger.info(f"Loading config from {config_path}")
            import yaml
            
            # Read raw content for debugging
            with open(config_path, 'r') as f:
                raw_content = f.read()
                logger.info(f"Raw config content: {raw_content}")
            
            # Parse YAML
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f) or {}
                
                # Add default values if missing
                if 'offline_mode' not in config_data:
                    config_data['offline_mode'] = True
                if 'knowledge_graph_dir' not in config_data:
                    config_data['knowledge_graph_dir'] = str(Path(DEFAULT_CONFIG_DIR) / "knowledge_graph")

                logger.info(f"Parsed config data: {config_data}")
                return config_data
        
        # 2. Try to load from environment variables
        neo4j_uri = os.environ.get("NEO4J_URI")
        if neo4j_uri:
            logger.info("Loading config from environment variables")
            return {
                "neo4j_uri": neo4j_uri,
                "neo4j_user": os.environ.get("NEO4J_USER", "neo4j"),
                "neo4j_password": os.environ.get("NEO4J_PASSWORD", ""),
                "vector_store": os.environ.get("VECTOR_STORE_PATH", "vectors.sqlite"),
                "schema_version": "K1"
            }
        
        # 3. Use defaults (offline mode)
        logger.info("Using default offline configuration")
        return {
            "neo4j_uri": None,
            "vector_store": None,
            "schema_version": "K1",
            "offline_mode": True,
            "knowledge_graph_dir": Path(DEFAULT_CONFIG_DIR) / "knowledge_graph"
        }
    
    except Exception as e:
        error_msg = f"Failed to load configuration: {e}"
        logger.error(error_msg)
        raise CLIError(error_msg)


def detect_coverage_gaps(config: Dict[str, Any], threshold: int = DEFAULT_THRESHOLD) -> Tuple[List[Dict[str, Any]], int]:
    """Detect implementations with test coverage below threshold.
    
    Args:
        config: Configuration dictionary
        threshold: Coverage percentage threshold (0-100)
        
    Returns:
        Tuple[List[Dict[str, Any]], int]: List of gaps and total implementation count
        
    Raises:
        CLIError: If gap detection fails
    """
    try:
        # Check if we're in offline mode
        offline_mode = config.get("offline_mode", False)
        logger.info(f"Config values: {config}")
        logger.info(f"Offline mode detected: {offline_mode}")
        
        if offline_mode:
            logger.info("Running gap detection in offline mode")
            return detect_gaps_from_local_json(config, threshold)
        else:
            logger.info("Running gap detection with Neo4j")
            return detect_gaps_from_neo4j(config, threshold)
            
    except Exception as e:
        error_msg = f"Failed to detect coverage gaps: {e}"
        logger.error(error_msg)
        raise CLIError(error_msg)


def detect_gaps_from_neo4j(config: Dict[str, Any], threshold: int) -> Tuple[List[Dict[str, Any]], int]:
    """Detect coverage gaps using Neo4j.
    
    Args:
        config: Configuration dictionary with Neo4j connection details
        threshold: Coverage percentage threshold
        
    Returns:
        Tuple[List[Dict[str, Any]], int]: List of gaps and total implementation count
        
    Raises:
        CLIError: If Neo4j query fails
    """
    try:
        # Import Neo4j client
        from testindex.knowledge.graph.neo4j_client import Neo4jClient, Neo4jConfig
        
        # Create Neo4j config
        neo4j_config = Neo4jConfig(
            uri=config.get("neo4j_uri"),
            username=config.get("neo4j_user", "neo4j"),
            password=config.get("neo4j_password", "")
        )
        
        # Connect to Neo4j
        client = Neo4jClient(neo4j_config)
        
        # Define query for implementations below threshold
        query = """
        MATCH (i:Implementation)
        WHERE i.coverage IS NULL OR i.coverage <= $threshold
        RETURN i.file_path as file, i.name as function, 
               COALESCE(i.coverage, 0) as coverage
        ORDER BY i.file_path, i.name
        """
        
        # Execute query
        result = client.run_query(query, {"threshold": threshold})
        
        # Process results
        gaps = []
        for record in result:
            gaps.append({
                "file": record["file"],
                "function": record["function"],
                "coverage": record["coverage"]
            })
        
        # Get total implementations count
        count_query = "MATCH (i:Implementation) RETURN count(i) as count"
        count_result = client.run_query(count_query)
        total_impls = count_result[0]["count"] if count_result else 0
        
        logger.info(f"Found {len(gaps)} gaps out of {total_impls} implementations")
        return gaps, total_impls
        
    except ImportError:
        logger.error("Neo4j client not available. Install with pip install neo4j")
        raise CLIError("Neo4j client not available")
    except Exception as e:
        error_msg = f"Neo4j gap detection failed: {e}"
        logger.error(error_msg)
        raise CLIError(error_msg)


def detect_gaps_from_local_json(config: Dict[str, Any], threshold: int) -> Tuple[List[Dict[str, Any]], int]:
    """Detect coverage gaps using local JSON files.
    
    Args:
        config: Configuration dictionary with paths
        threshold: Coverage percentage threshold
        
    Returns:
        Tuple[List[Dict[str, Any]], int]: List of gaps and total implementation count
        
    Raises:
        CLIError: If JSON files cannot be read
    """
    try:
        import json
        
        # Get path to knowledge graph directory
        kg_dir = config.get("knowledge_graph_dir", Path(DEFAULT_CONFIG_DIR) / "knowledge_graph")
        
        if isinstance(kg_dir, str):
            kg_dir = Path(kg_dir)
            
        logger.info(f"Looking for nodes.json in: {kg_dir}")
            
        # Check if nodes.json exists
        nodes_file = kg_dir / "nodes.json"
        if not nodes_file.exists():
            raise CLIError(f"Nodes file not found: {nodes_file}")
            
        # Load nodes
        with open(nodes_file, 'r') as f:
            nodes = json.load(f)
            
        # Filter for implementations
        implementations = []
        for node in nodes:
            # Check if it's an implementation node (not a module)
            if node.get("type") == "Implementation":
                # Extract properties
                props = node.get("properties", {})
                
                # Default coverage to 0 if not present
                coverage = props.get("coverage", 0)
                
                implementations.append({
                    "id": node.get("id", "unknown"),
                    "file": node.get("file_path", "unknown"),
                    "function": node.get("name", "unknown"),
                    "coverage": coverage
                })
        
        # Log some sample implementations for debugging
        logger.debug("Sample implementations:")
        for impl in implementations[:5]:
            logger.debug(f"  File: {impl['file']}, Function: {impl['function']}, Coverage: {impl['coverage']}")
        
        # Filter for gaps
        gaps = [impl for impl in implementations if impl["coverage"] <= threshold]
        
        # Log all implementations with coverage > 0 for debugging
        covered_impls = [impl for impl in implementations if impl["coverage"] > 0]
        logger.debug(f"Found {len(covered_impls)} implementations with coverage > 0:")
        for impl in covered_impls[:20]:  # Show up to 20
            logger.debug(f"  Covered: {impl['file']} - {impl['function']} ({impl['coverage']}%)")
        
        # Calculate percentage for summary
        gap_percentage = (len(gaps) / len(implementations)) * 100 if implementations else 0
        logger.info(f"Found {len(gaps)} gaps out of {len(implementations)} implementations ({gap_percentage:.1f}%)")
        
        return gaps, len(implementations)
        
    except Exception as e:
        error_msg = f"Local JSON gap detection failed: {e}"
        logger.error(error_msg)
        raise CLIError(error_msg)


def output_table(gaps: List[Dict[str, Any]], total_impls: int = None) -> None:
    """Output gaps as a pretty table to stdout.
    
    Args:
        gaps: List of coverage gaps
        total_impls: Total number of implementations
    """
    console = Console()
    
    table = Table(title="Coverage Gaps")
    table.add_column("File", style="cyan")
    table.add_column("Function", style="magenta")
    table.add_column("%Cov", justify="right", style="green")
    
    for gap in gaps:
        table.add_row(
            gap["file"],
            gap["function"],
            str(gap["coverage"])
        )
    
    console.print(table)
    
    # Display gap summary
    if total_impls is not None:
        gap_percentage = (len(gaps) / total_impls) * 100 if total_impls > 0 else 0
        console.print(f"Gaps: {len(gaps)} / {total_impls} implementations ({gap_percentage:.1f}%)")
    else:
        console.print(f"Gaps: {len(gaps)} implementations")


def output_json(gaps: List[Dict[str, Any]], output_path: str, repo_info: Dict[str, Any] = None, total_impls: int = None) -> None:
    """Output gaps as JSON to a file.
    
    Args:
        gaps: List of coverage gaps
        output_path: Path to write JSON output
        repo_info: Repository information (optional)
        total_impls: Total number of implementations
        
    Raises:
        CLIError: If JSON output fails
    """
    try:
        # Prepare JSON structure with versioning and metadata
        output = {
            "version": "v1",
            "repo": repo_info or {"sha": "unknown"},
            "gaps": gaps,
            "total_gaps": len(gaps),
            "total_implementations": total_impls,
            "gap_percentage": (len(gaps) / total_impls) * 100 if total_impls and total_impls > 0 else None,
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
        }
        
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            logger.info(f"Created output directory: {output_dir}")
        
        # Write to file
        with open(output_path, 'w') as f:
            json_lib.dump(output, f, indent=2)
            
        logger.info(f"JSON output written to {output_path}")
        
    except Exception as e:
        error_msg = f"Failed to write JSON output: {e}"
        logger.error(error_msg)
        raise CLIError(error_msg)


def get_repo_info() -> Dict[str, Any]:
    """Get information about the current repository.
    
    Returns:
        Dict[str, Any]: Repository information including SHA
    """
    try:
        import subprocess
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        sha = result.stdout.strip()
        return {"sha": sha}
    except Exception:
        return {"sha": "unknown"}


def ensure_coverage_file(coverage_file: Optional[str]) -> Optional[str]:
    """Ensure a coverage file is available for processing.
    
    This function will:
    1. Use the provided coverage_file if specified
    2. Look for coverage.xml in the current directory
    
    Args:
        coverage_file: Path to coverage file (if specified)
        
    Returns:
        Path to the coverage file if found, None otherwise
    """
    # Use the provided file if specified
    if coverage_file and Path(coverage_file).exists():
        logger.info(f"Using specified coverage file: {coverage_file}")
        return coverage_file
    
    # Look in current directory using PathResolver
    local_file = find_coverage_file()
    if local_file:
        logger.info(f"Using coverage file from repository: {local_file}")
        return local_file
    
    logger.warning("No coverage file found")
    return None


@click.command('coverage', help='Display test coverage gaps')
@click.option('--json', 'json_output', type=click.Path(),
              help='Path to write JSON output')
@click.option('--exit-on-gap', is_flag=True,
              help='Exit with code 1 if gaps found')
@click.option('--threshold', type=int, default=0,
              help='Minimum coverage percentage required (default: 0)')
@click.option('--coverage-file', type=click.Path(exists=True), 
              help='Path to coverage.xml file to ingest before checking gaps')
@click.option('--no-env-check', is_flag=True, help='Skip environment dependency check')
@common_options
@needs_env('coverage')
def coverage_command(json_output, exit_on_gap, threshold, coverage_file, verbose, summary_only: bool = False, no_env_check: bool = False, **kwargs):
    """Display test coverage gaps.
    
    This command:
    1. Reads a coverage.xml file
    2. Matches coverage data to code chunks
    3. Detects gaps in test coverage
    4. Displays or exports the gaps
    
    Exit codes:
    - 0: No gaps found, or gaps below threshold
    - 1: Gaps found above threshold (and --exit-on-gap specified)
    - 2: Error occurred
    - 3: CLI-specific error
    - 4: Unexpected error
    
    Note: Uses sys.exit() for non-zero exit codes to ensure consistent behavior when called
    both from command line and in test environments.
    """
    try:
        # Load config
        config = load_config()
        
        # Get repository info
        repo_info = get_repo_info()
        
        # Get knowledge graph directory using PathResolver
        kg_dir = PathResolver.knowledge_graph_dir()
        config["knowledge_graph_dir"] = str(kg_dir)
        logger.info(f"Using knowledge graph directory: {kg_dir}")
        
        # Ensure coverage file is available
        coverage_file = ensure_coverage_file(coverage_file)
        
        # Check if we need to ingest coverage data
        if not has_coverage_data(kg_dir):
            if coverage_file:
                logger.info(f"No coverage data found in graph, ingesting from {coverage_file}")
                updated, total = ingest_coverage(coverage_file, kg_dir)
                logger.info(f"Updated {updated} of {total} nodes with coverage data")
                if updated == 0:
                    console = Console()
                    console.print(f"[yellow]Warning:[/] No coverage data could be extracted from {coverage_file}")
            else:
                console = Console()
                console.print("[yellow]Warning:[/] No coverage data found in knowledge graph and no coverage file specified")
                console.print("Run tests with coverage before using this command:")
                console.print("  pytest --cov --cov-report=xml")
                console.print("Or use our helper command:")
                console.print("  testindex test")
                console.print("Or specify a coverage file:")
                console.print("  testindex coverage --coverage-file=coverage.xml")
                
                # Exit with code 2 to indicate no coverage data
                return 2
        
        # Detect coverage gaps
        gaps, total_impls = detect_coverage_gaps(config, threshold)
        
        # Output results
        if json_output:
            output_json(gaps, json_output, repo_info, total_impls)
        else:
            output_table(gaps, total_impls)
        
        # Return appropriate exit code
        if len(gaps) > 0 and exit_on_gap:
            logger.info(f"Found {len(gaps)} gaps with exit-on-gap flag set, returning exit code 1")
            import sys
            sys.exit(1)
        else:
            logger.info(f"Returning exit code 0 (gaps: {len(gaps)}, exit-on-gap: {exit_on_gap})")
            return 0
        
    except CLIError as e:
        console = Console()
        console.print(f"[red]Error:[/] {e}")
        return 3
    except Exception as e:
        console = Console()
        console.print(f"[red]Unexpected error:[/] {e}")
        return 4 