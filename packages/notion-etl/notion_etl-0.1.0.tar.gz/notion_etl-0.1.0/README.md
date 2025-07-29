# Notion ETL

A Python package for extracting, transforming, and loading data from Notion using Polars DataFrames and the Notion API Client.

The package provides a simple API for loading raw and clean data from Notion databases into Polars DataFrames, allowing for efficient data manipulation and analysis.

## Installation

```bash
pip install notion-etl
```

## Usage

### Authentication

Set your Notion API key as an environment variable:

```bash
export NOTION_TOKEN=secret_...
```

You can also set the token in your code:

```python
import os
from notion_etl.loader import NotionDataLoader

loader = NotionDataLoader(os.environ["NOTION_TOKEN"])
```

### Loading Data from a Notion Database

```python
from notion_etl.loader import NotionDataLoader

loader = NotionDataLoader()
database = loader.get_database("database_id")
database.records # List of records in the database
database.to_dataframe() # Convert to clean Polars DataFrame
database.to_dataframe(clean=False) # Convert to raw Polars DataFrame
```
