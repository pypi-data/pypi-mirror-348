# Python Datadis API Client

A Python client library to interact with the [Datadis API](https://www.datadis.es/private-api).

Datadis is the Spanish electricity distributor's data access platform that allows users to retrieve information about their electricity consumption and contracts.

## Installation

```bash
pip install datadis-client
```

## Usage

### Authentication

```python
from datadis_client import create_client

# Method 1: Create the client and authenticate in one step
client = create_client(username="YOUR_NIF", password="YOUR_PASSWORD")

# Method 2: Create the client and authenticate separately
from datadis_client import DatadisClient
client = DatadisClient(username="YOUR_NIF", password="YOUR_PASSWORD")
client.authenticate()
```

### Getting supplies

```python
# Get all supplies associated with your account
supplies = client.get_supplies()

# Get supplies for a specific distributor
supplies = client.get_supplies(distributor_code="0123")

# Get supplies for an authorized NIF
supplies = client.get_supplies(authorized_nif="AUTHORIZED_NIF")
```

### Getting contract details

```python
# Get contract details for a specific CUPS
contract = client.get_contract_detail(
    cups="ES0021000000000000AA1F",
    distributor_code="0123"
)
```

### Getting consumption data

```python
# Get hourly consumption data for a specific period
consumption = client.get_consumption_data(
    cups="ES0021000000000000AA1F",
    distributor_code="0123",
    start_date="2023/01",
    end_date="2023/02",
    measurement_type="0",  # 0 for hourly, 1 for quarter-hourly
    point_type="5"
)

# Access consumption readings
for reading in consumption.get('timeCurve', []):
    date = reading.get('date')
    time = reading.get('time')
    consumption_kwh = reading.get('consumptionKWh')
    print(f"{date} {time}: {consumption_kwh} kWh")
```

### Other available methods

The client provides access to all Datadis API endpoints:

- `get_max_power` - Get maximum power data
- `get_reactive_data` - Get reactive energy data
- `get_distributors_with_supplies` - Get distributors with supplies
- `api_search` - Search for consumption data by parameters
- `api_sum_search` - Search for summarized consumption data
- `api_search_auto` - Search for auto-consumption data

## Examples

Check the `examples` directory for complete usage examples.

## Development

### Setting up a development environment

Clone the repository and install development dependencies:

```bash
git clone https://github.com/agaliste/python-datadis.git
cd python-datadis
pip install -e ".[dev]"
```

### Running tests

Run the unit tests with pytest:

```bash
pytest tests/test_auth.py tests/test_consumption.py tests/test_supplies.py tests/test_search.py
```

Run tests with coverage:

```bash
pytest --cov=datadis_client
```

Generate coverage reports:

```bash
pytest --cov=datadis_client --cov-report=html
```

### Running integration tests

Integration tests make actual API calls to Datadis and **require** valid credentials. These tests verify that the client works correctly with the real Datadis API.

1. Create a `.env` file in the project root with your Datadis credentials:

   ```
   # Datadis API credentials (required)
   DATADIS_USERNAME=your_nif_here
   DATADIS_PASSWORD=your_password_here

   # Test data (optional)
   # If not provided, tests will auto-discover a CUPS from your account
   TEST_CUPS=ES0021000000000000XXXX
   TEST_DISTRIBUTOR_CODE=0000
   TEST_POINT_TYPE=5
   ```

2. Run the integration tests using the provided scripts:

   ```bash
   # Unix/macOS
   ./run_tests.sh

   # Windows
   run_tests.bat
   ```

   Or run them directly:

   ```bash
   pytest tests/test_integration.py -v
   ```

   If you don't provide specific TEST_CUPS values, the integration tests will automatically use the first CUPS found in your account.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
