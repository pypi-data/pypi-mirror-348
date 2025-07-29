# Aston AI

Aston is a code intelligence system for parsing, analyzing, and finding test coverage gaps in your code.

## Installation

```bash
# Install from PyPI
pip install astonai
```

## Quick Start

```bash
# Initialize your repository
aston init --offline

# Generate knowledge graph relationships
aston graph build

# View knowledge graph statistics
aston graph stats
```

## Core Commands

### Repository Initialization

```bash
# Initialize repository and create knowledge graph
aston init [--offline]
```

Options:
- `--offline`: Skip Neo4j integration and work with local files only (default)
- `--online`: Use Neo4j if available (broken right now)

### Test Coverage

```bash
# Run tests with coverage
aston test

# Find testing gaps
aston coverage [--threshold 80] [--json results.json] [--exit-on-gap]
```

Options:
- `--threshold`: Minimum coverage percentage (default: 0)
- `--json`: Output results in JSON format
- `--exit-on-gap`: Return code 1 if gaps found (useful for CI)
- `--coverage-file`: Specify custom coverage file location

### Knowledge Graph

```bash
# Build edge relationships between nodes
aston graph build

# View statistics about the knowledge graph
aston graph stats

# Export graph to DOT format
aston graph export [--output graph.dot] [--filter CALLS,IMPORTS] [--open]

# Open interactive graph viewer in browser
aston graph view [--filter CALLS,IMPORTS]
```

The graph command provides:
- `build`: Analyzes your codebase to extract CALLS and IMPORTS edges
- `stats`: Displays node and edge statistics
- `export`: Converts the graph to Graphviz DOT format
- `view`: Opens an interactive D3.js visualization in your browser

### Environment Check

```bash
# Check if all required dependencies are installed
aston check
```

Options:
- `--no-env-check`: Skip environment dependency check (also works with any command)

## Repository-Centric Design

Aston follows a repository-centric approach:
- All operations are relative to the repository root (current directory)
- Data is stored in `.testindex` directory at the repository root
- Path resolution is normalized for consistent matching
- Works with both offline and Neo4j storage

## Environment Variables

```
DEBUG=1                      # Enable debug logging
NEO4J_URI=bolt://localhost:7687  # Optional Neo4j connection
NEO4J_USER=neo4j            # Optional Neo4j username
NEO4J_PASS=password         # Optional Neo4j password
ASTON_NO_ENV_CHECK=1        # Skip environment dependency check
```

