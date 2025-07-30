"""
Integration tests for the Datadis client.

These tests require valid Datadis credentials to be set as environment variables.
To use these tests, create a .env file with the following variables:

    DATADIS_USERNAME=your_nif_here
    DATADIS_PASSWORD=your_password_here
    TEST_CUPS=ES0021000000000000XXXX
    TEST_DISTRIBUTOR_CODE=0000
    TEST_POINT_TYPE=5
    TEST_START_DATE=2023/01
    TEST_END_DATE=2023/02

Then run the tests with pytest:
    pytest tests/test_integration.py -v

Note: These tests make actual API calls to the Datadis API.
"""

import os
import pytest
from datetime import datetime, timedelta
from dotenv import load_dotenv
from datadis_client import create_client


# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
DATADIS_USERNAME = os.getenv("DATADIS_USERNAME")
DATADIS_PASSWORD = os.getenv("DATADIS_PASSWORD")

# Test data
TEST_CUPS = os.getenv("TEST_CUPS")
TEST_DISTRIBUTOR_CODE = os.getenv("TEST_DISTRIBUTOR_CODE")
TEST_POINT_TYPE = os.getenv("TEST_POINT_TYPE")
TEST_START_DATE = os.getenv("TEST_START_DATE")
TEST_END_DATE = os.getenv("TEST_END_DATE")

# Use current and previous month if dates not provided
if not TEST_START_DATE or not TEST_END_DATE:
    now = datetime.now()
    last_month = now - timedelta(days=30)
    TEST_START_DATE = last_month.strftime("%Y/%m")
    TEST_END_DATE = now.strftime("%Y/%m")


def check_credentials():
    """Check if credentials are available and valid."""
    if not DATADIS_USERNAME or not DATADIS_PASSWORD:
        pytest.fail("Datadis credentials not set in environment variables. Add them to the .env file.")
    if DATADIS_USERNAME == "your_nif_here" or DATADIS_PASSWORD == "your_password_here":
        pytest.fail("Please update the .env file with your actual Datadis credentials.")


@pytest.fixture(scope="session")
def client():
    """Create an authenticated Datadis client that persists across all tests."""
    check_credentials()
    try:
        client = create_client(DATADIS_USERNAME, DATADIS_PASSWORD)
        return client
    except Exception as e:
        pytest.fail(f"Failed to authenticate with Datadis: {str(e)}")


class TestIntegration:
    """Integration tests for the Datadis client."""

    def test_authenticate(self, client):
        """Test that authentication works."""
        assert client.token is not None, "Authentication failed, token is None"

    def test_get_supplies(self, client):
        """Test getting supplies."""
        supplies = client.get_supplies()
        assert "supplies" in supplies, "Failed to get supplies"
        assert isinstance(supplies["supplies"], list), "Supplies is not a list"
        print(f"Found {len(supplies['supplies'])} supplies")

    def test_get_contract_detail(self, client):
        """Test getting contract details."""
        if not TEST_CUPS or not TEST_DISTRIBUTOR_CODE:
            pytest.skip("Test CUPS or distributor code not provided in .env file")

        contract = client.get_contract_detail(
            cups=TEST_CUPS,
            distributor_code=TEST_DISTRIBUTOR_CODE
        )
        assert "contract" in contract, "Failed to get contract details"

    def test_get_consumption_data(self, client):
        """Test getting consumption data."""
        if not TEST_CUPS or not TEST_DISTRIBUTOR_CODE or not TEST_POINT_TYPE:
            pytest.skip("Test CUPS, distributor code, or point type not provided in .env file")

        consumption = client.get_consumption_data(
            cups=TEST_CUPS,
            distributor_code=TEST_DISTRIBUTOR_CODE,
            start_date=TEST_START_DATE,
            end_date=TEST_END_DATE,
            measurement_type="0",  # Hourly data
            point_type=TEST_POINT_TYPE
        )
        assert "timeCurve" in consumption, "Failed to get consumption data"
        print(f"Found {len(consumption.get('timeCurve', []))} consumption readings")

    def test_get_distributors_with_supplies(self, client):
        """Test getting distributors with supplies."""
        distributors = client.get_distributors_with_supplies()
        assert "distExistenceUser" in distributors, "Failed to get distributors with supplies"
        if "distributorCodes" in distributors.get("distExistenceUser", {}):
            codes = distributors["distExistenceUser"]["distributorCodes"]
            print(f"Found {len(codes)} distributors with supplies: {', '.join(codes)}")

    def test_auto_discover_cups_and_details(self, client):
        """Test automatic discovery of CUPS and details from the account."""
        # Skip test discovery if TEST_CUPS already provided
        if TEST_CUPS and TEST_DISTRIBUTOR_CODE:
            pytest.skip("Using provided CUPS and distributor code")

        # Get supplies
        supplies = client.get_supplies()
        assert "supplies" in supplies, "Failed to get supplies"
        assert len(supplies["supplies"]) > 0, "No supplies found for this account"

        # Get details for the first supply
        supply = supplies["supplies"][0]
        cups = supply["cups"]
        distributor_code = supply["distributorCode"]
        point_type = supply["pointType"]

        print(f"\nAuto-discovered supply:")
        print(f"CUPS: {cups}")
        print(f"Distributor Code: {distributor_code}")
        print(f"Point Type: {point_type}")

        # Get contract details
        contract = client.get_contract_detail(cups, distributor_code)
        assert "contract" in contract, "Failed to get contract details"

        # Get consumption data
        consumption = client.get_consumption_data(
            cups=cups,
            distributor_code=distributor_code,
            start_date=TEST_START_DATE,
            end_date=TEST_END_DATE,
            measurement_type="0",  # Hourly data
            point_type=str(point_type)
        )
        assert "timeCurve" in consumption, "Failed to get consumption data"
        print(f"Found {len(consumption.get('timeCurve', []))} consumption readings for auto-discovered CUPS")
