"""
Supplies and contract data API endpoints for the Datadis client.
"""

from typing import Dict, Any, Optional


class SuppliesMixin:
    """Mixin for supplies and contract-related API endpoints."""

    def get_supplies(
        self,
        authorized_nif: Optional[str] = None,
        distributor_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get the list of supplies associated with the authenticated user.

        Args:
            authorized_nif: Optional authorized NIF to get supplies for.
            distributor_code: Optional distributor code to filter supplies.

        Returns:
            Dict[str, Any]: The supplies data.
        """
        params = {}

        if authorized_nif:
            params["authorizedNif"] = authorized_nif

        if distributor_code:
            params["distributorCode"] = distributor_code

        return self._get("/api-private/api/get-supplies-v2", params)

    def get_contract_detail(
        self,
        cups: str,
        distributor_code: str,
        authorized_nif: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get contract details for a specific CUPS.

        Args:
            cups: The CUPS for which to retrieve contract details.
            distributor_code: Code of distributor, obtained from get_supplies request.
            authorized_nif: Optional authorized NIF to get data for.

        Returns:
            Dict[str, Any]: The contract details.
        """
        params = {
            "cups": cups,
            "distributorCode": distributor_code
        }

        if authorized_nif:
            params["authorizedNif"] = authorized_nif

        return self._get("/api-private/api/get-contract-detail-v2", params)

    def get_distributors_with_supplies(
        self,
        authorized_nif: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get the list of distributors with supplies for the authenticated user.

        Args:
            authorized_nif: Optional authorized NIF to get distributors for.

        Returns:
            Dict[str, Any]: The distributors data.
        """
        params = {}

        if authorized_nif:
            params["authorizedNif"] = authorized_nif

        return self._get("/api-private/api/get-distributors-with-supplies-v2", params)
