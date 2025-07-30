# MongoDB API Client (Python)

A Python client library for interacting with a MongoDB RESTful API, providing a fluent interface for building queries and performing CRUD operations with robust response handling.

## Overview

The `MongoApiClient` class enables seamless interaction with a MongoDB API server, supporting operations like selecting, inserting, updating, and deleting documents. Key features include:

- **Fluent Query Building**: Chain methods like `where`, `or_where`, `sort_by`, `group_by` for complex queries.
- **Query Aliases**: Use `all` (preferred), `select`, `get`, `get_all` for `find()`, and `first` (preferred), `first_or_none`, `one` for `first()`.
- **Auto-Conversion Control**: Toggle type conversion for query values using `auto_convert_type` in `where`/`or_where`.
- **Grouped Data Handling**: Process grouped query results with `MongoApiResponseData`, including inner pagination and records.
- **Pagination Support**: Handle pagination metadata via `MongoApiResponsePagination`.
- **Retry Mechanism**: Automatically retry failed requests with configurable exponential backoff using a `retry` decorator.
- **Response Wrapping**: Normalize API responses into a consistent `MongoApiResponse` envelope.
- **Iterator and Countable Data**: `MongoApiResponseData` supports iteration and length checking for flexible data handling.

## Installation

Install the package using pip:

```bash
pip install mongo-api-client
```

Ensure Python 3.6+ and the `requests` library are installed (included as a dependency).

## Configuration

Configure the client using constructor parameters or environment variables for sensitive data like API keys. Supported environment variables:

- `MONGO_API_URL`: API server URL (e.g., `api.example.com`).
- `MONGO_API_PORT`: Server port (default: `80`).
- `MONGO_API_KEY`: API key for authentication.
- `MONGO_API_SCHEME`: Protocol (`http` or `https`, default: `https`).
- `MONGO_API_TIMEOUT`: Request timeout in seconds (default: `5.0`).

Example using environment variables:

```python
import os
from mongo_api_client import MongoApiClient

client = MongoApiClient(
    server_url=os.getenv('MONGO_API_URL', 'api.example.com'),
    server_port=int(os.getenv('MONGO_API_PORT', 80)),
    api_key=os.getenv('MONGO_API_KEY', 'your-api-key'),
    scheme=os.getenv('MONGO_API_SCHEME', 'https'),
    auto_convert_values=True,
    timeout=float(os.getenv('MONGO_API_TIMEOUT', 5.0))
)
```

## Usage

### Initializing the Client

Create a `MongoApiClient` instance with your API server details:

```python
from mongo_api_client import MongoApiClient

client = MongoApiClient(
    server_url='api.example.com',
    server_port=80,
    api_key='your-api-key',
    scheme='https',
    auto_convert_values=True,
    timeout=5.0
)
```

### Authentication

The client uses API key authentication by default. Pass the API key in the constructor or via the `MONGO_API_KEY` environment variable.

### Select Queries

The library provides a powerful fluent interface for select queries, with `all()` as the preferred method for fetching multiple documents and `first()` for a single document. Use `get_result()` to access individual document data for single or multiple results, `get_records()` for grouped query results, and `get_count()` for counting documents.

#### Fetching Multiple Documents

Use `all()` (preferred over `select()`, `get()`, or `get_all()`) to fetch multiple documents. Iterate through the results and call `get_result()` on each:

```python
response = (client
    .from_db('my_database')
    .from_collection('users')
    .where('age', '>=', 18, auto_convert_type=True)
    .sort_by('name', 'asc')
    .page(1)
    .per_page(20)
    .all())

if response.is_ok():
    data = response.get_data()
    print(f'Found {len(data)} users:')
    for doc in data:
        print(doc.get_result())
else:
    print(f'Error: {response.get_error()}')
```

The `auto_convert_type=True` ensures the `age` value is tagged for automatic type conversion (e.g., `18/a` in the query string). The `MongoApiResponseData` object supports `len()` for counting records.

#### Fetching a Single Document

Use `first()` (preferred over `first_or_none()` or `one()`) to retrieve the first matching document. Access the document with `get_result()`:

```python
response = (client
    .from_db('my_database')
    .from_collection('users')
    .where('name', '=', 'John Doe', auto_convert_type=False)
    .first())

if response.is_ok():
    data = response.get_data()
    print(data.get_result() or 'No document found')
else:
    print(f'Error: {response.get_error()}')
```

#### Fetching a Document by ID

Use `find_by_id()` to retrieve a document by its `_id` and access it with `get_result()`:

```python
response = (client
    .from_db('my_database')
    .from_collection('users')
    .find_by_id('507f1f77bcf86cd799439011'))

if response.is_ok():
    data = response.get_data()
    print(data.get_result() or 'No document found')
else:
    print(f'Error: {response.get_error()}')
```

#### Using `or_where` with `auto_convert_type`

Combine `where` and `or_where` for complex queries, using `all()` to fetch multiple documents:

```python
response = (client
    .from_db('my_database')
    .from_collection('users')
    .where('age', '>=', 18, auto_convert_type=True)
    .or_where('status', '=', 'active', auto_convert_type=False)
    .per_page(10)
    .all())

if response.is_ok():
    data = response.get_data()
    print(f'Found {len(data)} users:')
    for doc in data:
        print(doc.get_result())
else:
    print(f'Error: {response.get_error()}')
```

Here, `age` is tagged for conversion (`18/a`), while `status` is not (`active/n`), preserving the string value.

#### Grouped Queries with `group_by`

Group results by a field (e.g., `city`) and use `get_records()` to access records within each group:

```python
response = (client
    .from_db('my_database')
    .from_collection('users')
    .where('age', '>=', 18, auto_convert_type=True)
    .group_by('city')
    .inner_page(1)
    .inner_per_page(5)
    .all())

if response.is_ok():
    data = response.get_data()
    if data.has_grouped():
        for group in data:
            inner_pagination = group.get_inner_pagination()
            records = group.get_records()
            total_records = group.get_total_records()
            record_id = group.get_record_id()
            print(f'Group ID: {record_id or "unknown"}')
            print(f'Group: {group.get_data().get("city", "unknown")}')
            print(f'Total Records: {total_records[0] if total_records else 0}')
            print(f'Page {inner_pagination.get_current_page()}/{inner_pagination.get_total_pages()}')
            for record in records or []:
                print(f' - {record}')
    else:
        print('No grouped data found')
else:
    print(f'Error: {response.get_error()}')
```

The `MongoApiResponseData` class provides:
- `get_record_id()`: The `_id` of the group (e.g., the `city` value).
- `get_inner_pagination()`: A `MongoApiResponsePagination` object for inner pagination metadata.
- `get_records()`: The list of records in the group.
- `get_total_records()`: The total count of records in the group.

Use `inner_page` and `inner_per_page` to control pagination within groups. The class supports iteration for foreach loops and `len()` for counting records.

#### Counting Documents

Use `count()` to get the number of matching documents. Check `is_ok()` and call `get_count()`:

```python
response = (client
    .from_db('my_database')
    .from_collection('users')
    .where('age', '>=', 18, auto_convert_type=True)
    .count())

if response.is_ok():
    print(f'Total users: {response.get_count()}')
else:
    print(f'Error: {response.get_error()}')
```

#### Pagination Handling

Access pagination metadata for non-grouped or grouped queries:

```python
response = (client
    .from_db('my_database')
    .from_collection('users')
    .page(2)
    .per_page(15)
    .all())

if response.is_ok():
    pagination = response.get_pagination()
    print(f'Page {pagination.get_current_page()}/{pagination.get_total_pages()}')
    print(f'Next Page: {pagination.get_next_page()}')
    print(f'Previous Page: {pagination.get_prev_page()}')
    print(f'Items per page: {pagination.get_per_page()}')
    data = response.get_data()
    for doc in data:
        print(doc.get_result())
else:
    print(f'Error: {response.get_error()}')
```

For grouped queries, use `get_inner_pagination()` on `MongoApiResponseData` for per-group pagination, as shown in the `group_by` example.

#### Custom Select Queries

Execute custom MongoDB queries or aggregations, using `all()`-style result handling:

```python
# Custom query
custom_query = {'stats.timePlayed': {'$gte': 10000}}
response = (client
    .from_db('my_database')
    .from_collection('users')
    .execute_custom_query(custom_query))

if response.is_ok():
    data = response.get_data()
    for doc in data:
        print(doc.get_result())
else:
    print(f'Error: {response.get_error()}')

# Aggregation query
aggregate_query = [
    {'$match': {'stats.timePlayed': {'$gte': 10000}}},
    {'$group': {
        '_id': '$city',
        'totalTime': {'$sum': '$stats.timePlayed'},
        'avgTime': {'$avg': '$stats.timePlayed'}
    }},
    {'$sort': {'totalTime': -1}}
]
response = (client
    .from_db('my_database')
    .from_collection('users')
    .execute_custom_query(aggregate_query, aggregate=True))

if response.is_ok():
    data = response.get_data()
    for doc in data:
        print(doc.get_result())
else:
    print(f'Error: {response.get_error()}')
```

Use `aggregate=True` to execute as a pipeline query.

### Other CRUD Operations

#### Inserting Data

```python
payload = {'name': 'John Doe', 'age': 30}
response = client.from_db('my_database').from_collection('users').insert(payload)

if response.is_ok():
    print(f'Inserted document. Message: {response.get_message()}')
else:
    print(f'Error: {response.get_error()}')
```

#### Conditional Inserting

Use `insert_if()` to insert a document only if it matches the query conditions:

```python
payload = {'name': 'John Doe', 'age': 30}
response = (client
    .from_db('my_database')
    .from_collection('users')
    .where('name', '=', 'John Doe', auto_convert_type=False)
    .insert_if(payload))

if response.is_ok():
    print(f'Inserted document. Message: {response.get_message()}')
else:
    print(f'Error: {response.get_error()}')
```

#### Updating Data

```python
payload = {'age': 31}
response = (client
    .from_db('my_database')
    .from_collection('users')
    .where('name', '=', 'John Doe', auto_convert_type=False)
    .update(payload))

if response.is_ok():
    print(f'Updated documents. Message: {response.get_message()}')
else:
    print(f'Error: {response.get_error()}')
```

#### Updating by ID

Use `update_by_id()` to update a specific document by its `_id`:

```python
payload = {'age': 31}
response = (client
    .from_db('my_database')
    .from_collection('users')
    .update_by_id('507f1f77bcf86cd799439011', payload))

if response.is_ok():
    print(f'Updated document. Message: {response.get_message()}')
else:
    print(f'Error: {response.get_error()}')
```

#### Deleting Data

```python
response = (client
    .from_db('my_database')
    .from_collection('users')
    .where('age', '<', 18, auto_convert_type=True)
    .delete())

if response.is_ok():
    print(f'Deleted documents. Message: {response.get_message()}')
else:
    print(f'Error: {response.get_error()}')
```

#### Deleting by ID

Use `delete_by_id()` to delete a specific document by its `_id`:

```python
response = (client
    .from_db('my_database')
    .from_collection('users')
    .delete_by_id('507f1f77bcf86cd799439011'))

if response.is_ok():
    print(f'Deleted document. Message: {response.get_message()}')
else:
    print(f'Error: {response.get_error()}')
```

### Utility Methods

List databases or collections:

```python
db_response = client.list_databases()
if db_response.is_ok():
    print(db_response.get_databases())
else:
    print(f'Error: {db_response.get_error()}')

collection_response = client.list_tables_in_db('my_database')
if collection_response.is_ok():
    print(collection_response.get_tables())
else:
    print(f'Error: {collection_response.get_error()}')
```

Drop databases or collections:

```python
response = client.drop_database('my_database')
if response.is_ok():
    print(f'Dropped database. Message: {response.get_message()}')
else:
    print(f'Error: {response.get_error()}')

response = client.drop_collection('my_database', 'users')
if response.is_ok():
    print(f'Dropped collection. Message: {response.get_message()}')
else:
    print(f'Error: {response.get_error()}')
```

### Features

- **Fluent Select Queries**: Chain `where`, `or_where`, `group_by`, `sort_by`, with aliases (`all` preferred, `select`, `get`, `get_all`; `first` preferred, `first_or_none`, `one`) and `auto_convert_type` control.
- **Grouped Data Processing**: `MongoApiResponseData` provides `get_record_id`, `get_inner_pagination`, `get_records`, and `get_total_records` for grouped results, with iterator and length support.
- **Pagination Support**: `MongoApiResponsePagination` includes `get_current_page`, `get_total_pages`, `get_next_page`, `get_prev_page`, `get_last_page`, and `get_per_page`.
- **Retry Mechanism**: Handles transient network failures with exponential backoff via a `retry` decorator.
- **Type Safety**: Uses type hints and docstrings for better IDE support.
- **Flexible Querying**: Supports operators (`=`, `!=`, `<`, `>`, `like`, etc.), custom MongoDB queries, and pipeline aggregations.
- **ID-Based Operations**: Supports `find_by_id`, `update_by_id`, and `delete_by_id` for precise document manipulation.
- **Result Handling**: Use `get_result()` for single/multiple document data and `get_records()` for grouped query results.

## Error Handling

Responses are wrapped in `MongoApiResponse`, providing:
- `is_ok()`/`is_not_ok()`: Check success or failure.
- `get_error()`: Error message if failed.
- `get_status_code()`: HTTP status code (e.g., `400`, `401`, `429`, `500`).
- `get_data()`: Documents or grouped data as `MongoApiResponseData`.
- `get_message()`: Additional response message.
- `get_response()`: Raw API response payload.

Common error codes:
- `400`: Invalid query or payload.
- `401`: Authentication failure (invalid API key).
- `429`: Rate limit exceeded.
- `500`: Server error.

Example handling errors:

```python
response = client.from_db('my_database').from_collection('users').all()
if response.is_not_ok():
    print(f'Request failed with code {response.get_status_code()}: {response.get_error()}')
    if response.get_status_code() == 401:
        print('Please check your API key.')
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.