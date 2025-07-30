"""
Consumption data API endpoints for the Datadis client.
"""

from typing import Dict, Any, Optional


class ConsumptionMixin:
    """Mixin for consumption-related API endpoints."""

    def get_consumption_data(
        self,
        cups: str,
        distributor_code: str,
        start_date: str,
        end_date: str,
        measurement_type: str,
        point_type: str,
        authorized_nif: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get consumption data for a specific CUPS.

        Args:
            cups: The CUPS for which to retrieve consumption data.
            distributor_code: Code of distributor, obtained from get_supplies request.
            start_date: Start date in format YYYY/MM.
            end_date: End date in format YYYY/MM.
            measurement_type: "0" for hourly data, "1" for quarter-hourly data.
            point_type: Point type code, obtained from get_supplies request.
            authorized_nif: Optional authorized NIF to get data for.

        Returns:
            Dict[str, Any]: The consumption data.
        """
        params = {
            "cups": cups,
            "distributorCode": distributor_code,
            "startDate": start_date,
            "endDate": end_date,
            "measurementType": measurement_type,
            "pointType": point_type
        }

        if authorized_nif:
            params["authorizedNif"] = authorized_nif

        return self._get("/api-private/api/get-consumption-data-v2", params)

    def get_max_power(
        self,
        cups: str,
        distributor_code: str,
        start_date: str,
        end_date: str,
        authorized_nif: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get maximum power data for a specific CUPS.

        Args:
            cups: The CUPS for which to retrieve max power data.
            distributor_code: Code of distributor, obtained from get_supplies request.
            start_date: Start date in format YYYY/MM.
            end_date: End date in format YYYY/MM.
            authorized_nif: Optional authorized NIF to get data for.

        Returns:
            Dict[str, Any]: The maximum power data.
        """
        params = {
            "cups": cups,
            "distributorCode": distributor_code,
            "startDate": start_date,
            "endDate": end_date
        }

        if authorized_nif:
            params["authorizedNif"] = authorized_nif

        return self._get("/api-private/api/get-max-power-v2", params)

    def get_reactive_data(
        self,
        cups: str,
        distributor_code: str,
        start_date: str,
        end_date: str,
        authorized_nif: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get reactive energy data for a specific CUPS.

        Args:
            cups: The CUPS for which to retrieve reactive data.
            distributor_code: Code of distributor, obtained from get_supplies request.
            start_date: Start date in format YYYY/MM.
            end_date: End date in format YYYY/MM.
            authorized_nif: Optional authorized NIF to get data for.

        Returns:
            Dict[str, Any]: The reactive energy data.
        """
        params = {
            "cups": cups,
            "distributorCode": distributor_code,
            "startDate": start_date,
            "endDate": end_date
        }

        if authorized_nif:
            params["authorizedNif"] = authorized_nif

        return self._get("/api-private/api/get-reactive-data-v2", params)
