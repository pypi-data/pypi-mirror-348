# Vaarhaft FraudScanner SDK

A modern, async-friendly Python SDK for interacting with the Vaarhaft FraudScanner API.


### Pre-requisites

In order to use the Vaarhaft FraudScanner API, you need to have an API key. You can obtain one by [requesting it here](https://www.vaarhaft.com/get-api-access).


## Installation

```bash
pip install vaarhaft-fraudscanner
```

## Examples

### Basic Usage

```python
import os
import asyncio

from vaarhaft.fraudscanner import FraudScannerClient


async def example_usage():
    """Run a basic example of using the FraudScanner SDK."""
    # Set an output directory for attachments
    output_dir = os.path.join(os.path.dirname(__file__), "..", "attachments")

    async with FraudScannerClient(api_key="your_api_key_here", attachments_output_dir=output_dir) as client:
        # Send a request to the FraudScanner API
        response = await client.send(
            file_path="/path/to/your/file.zip",
            case_number="My Case Number 123",
            issue_date="2023-10-01",
        )
        
        # Access metainformation about the request
        print(f"Status code: {response.status_code}")
        print(f"Request duration: {response.duration:.2f} seconds")
        
        # Access the raw JSON response
        print(f"Raw JSON response: {response.raw_json}")
        
        # Access textual information about received attachments
        print(f"Attachments: {response.attachments}")
        
        # Access response level fields regarding the overall response, such as the session ID
        print(f"Session ID: {response.sessionId}")
        
        # Access the processed 'Files' results
        for filename, file in response.Files:
            print(f"Filename: {filename}")
            print(f"The file's suspicion-level: {file.suspicion_level}")
        
        # Access all items in the response
        for id_tuple, item in response.get_all_items():
            print(f"Item in file {id_tuple.file_name} with id {id_tuple.item_uuid}: Suspicion level = {item.suspicion_level}")



if __name__ == "__main__":
    asyncio.run(example_usage())
```


## API Reference

### `FraudScannerClient`

The main client for interacting with the FraudScanner API. Can be used as a context manager (**async with**; see example above).

```python
client = FraudScannerClient(api_key="your_api_key", attachments_output_dir="attachments")
```

#### Parameters

- `api_key` (str): The API key for authenticating with the FraudScanner API.
- `attachments_output_dir` (str): Directory to save attachments to.

#### Methods

- `send(case_number, file_path, issue_date=None, contact_email=None)`: Send a request to the FraudScanner API. Returns a `FraudScannerResponse` object.

### `FraudScannerResponse`

The response from the FraudScanner API.

#### Properties

- `Files`: A dictionary of filename to file result pairs. Contains the main results of the analyses. Refer to the [API documentation](https://docs.vaarhaft.com/) for details on the structure of the results.
- `raw_json`: The raw JSON data from the response.
- `attachments`: A dictionary mapping filenames to their paths on disk.
- `status_code`: The HTTP status code of the response.
- `duration`: The duration of the request in seconds.
- `suspicion_level`: The overall suspicion level of the request.
- `caseNumber`: The case number for the analysis.
- `sessionId`: The session ID for the request.
- `modelVersions`: The versions of the models used for analysis.

#### Methods

- `get_all_items(type=None)`: Get all items from the response, optionally filtered by type (image/document).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.