# pyldplayer2

A structurally improved version of pyldplayer, providing enhanced functionality for LDPlayer emulator automation and management.

>doc is incomplete, please refer to the source code for more information 

## Features

- **Console Management**: Control and manage LDPlayer instances through `Console` and `BatchConsole` classes
- **File Operations**: Handle various LDPlayer file formats:
  - `LeidianFile`: LDPlayer configuration files
  - `RecordFile`: Record and playback functionality
  - `SMPFile`: Screen mapping files
  - `KMPFile`: Key mapping files
- **Instance Query**: Query and manage LDPlayer instances with the `Query` class
- **CLI Tools**: Command-line interface for easy interaction:
  - `ldplay`: Main CLI tool
  - `reldplay`: Compatible for old scripts

## Installation

```bash
pip install pyldplayer2
```

### Optional Dependencies

The package supports several optional feature sets:

```bash
# Shell features (CLI tools)
pip install pyldplayer2[shell]

# Instance discovery features
pip install pyldplayer2[discover]

# Automation features
pip install pyldplayer2[auto]

# Window management features
pip install pyldplayer2[wnd]

# to install all features
pip install pyldplayer2[all]
```

## Requirements
- Python >= 3.8
- LDPlayer emulator installed on your system

## Usage
### Basic Console Operations

```python
from pyldplayer2 import Console
from pyldplayer2.utils.discover import discover
# Create a console instance
discover()
console = Console()

# Start an instance
console.launch(name="instance_name")

# Stop an instance
console.quit(name="instance_name")
```

### Batch Operations

```python
from pyldplayer2 import BatchConsole
from pyldplayer2.utils.discover import discover
# Create a batch console instance
discover()
batch = BatchConsole()
batch.setScope("name.contains(somename)")
# Perform operations on multiple instances
batch.rock()
batch.quitall()
```
### Instance Query

The `Query` class provides powerful and flexible querying capabilities for LDPlayer instances. Here are all the supported query types:

#### String Queries
```python
from pyldplayer2 import Query
from pyldplayer2.utils.discover import discover

discover()
query = Query()

# String operations
query.query("name.startswith(test)")  # Names starting with 'test'
query.query("name.endswith(dev)")     # Names ending with 'dev'
query.query("name.contains(prod)")    # Names containing 'prod'
query.query("name.find(xyz)")         # Names containing 'xyz' at any position
query.query("name.index(abc)")        # Names containing 'abc' at any position
query.query("name.rfind(def)")        # Names containing 'def' from right
query.query("name.rindex(ghi)")       # Names containing 'ghi' from right

# Regex pattern matching
query.query("name(*dev*)")              # Names matching regex pattern
query.query("name(test?)")              # Names matching regex pattern
query.query("name(test+)")              # Names matching regex pattern

# Range queries
query.query("id[1:5]")                  # IDs between 1 and 5
query.query("id[3:]")                   # IDs greater than 3
query.query("id[:3]")                   # IDs less than 3

# Complex queries
query.query("name.startswith('test') and id[1:5]")  # Combined conditions
```

#### Direct ID/Name Queries
```python
# Query by ID
query.query(1)                          # Instance with ID 1
query.query([1, 2, 3])                  # Instances with IDs 1, 2, 3

# Query by name
query.query(["test1", "test2"])         # Instances named 'test1', 'test2'

# Mixed queries
query.query([1, "test1", 2, "test2"])   # Mix of IDs and names
```

#### Special Queries
```python
# Get all instances
query.query("all")

# Get running instances
query.query("running")
```

#### Query Options
```python
# Get first matching result
query.query("name.startswith('test')", retType="first")

# Limit number of results
query.query("id[1:5]", limit=2)         # Maximum 2 results

# Get only IDs
query.queryInts("name.startswith('test')")

# Get only names
query.queryNames("name.contains('dev')")
```

#### Query Results
The query results contain instance information including:
- `id`: Instance ID
- `name`: Instance name
- `android_started_int`: Running status
- And other instance properties

## Command Line Interface

The package provides two CLI tools:

1. `ldplay`: Main CLI tool for LDPlayer management
2. `reldplay`: Compatible for old scripts

Example CLI usage:
```bash
# List all instances
ldplay cmd list

# Start an instance
ldplay cmd launch --name instance_name

# Stop an instance
ldplay cmd quit --name instance_name
```

## Development

For development setup:

```bash
# Clone the repository
git clone https://github.com/ZackaryW/pyldplayer2.git

# rye is recommended for development
rye sync --all-features
```
