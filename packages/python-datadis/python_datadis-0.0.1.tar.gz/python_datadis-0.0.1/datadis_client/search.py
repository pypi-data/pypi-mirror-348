"""
Search API endpoints for the Datadis client.
"""

from typing import Dict, Any, Optional


class SearchMixin:
    """Mixin for search-related API endpoints."""

    def api_search(
        self,
        start_date: str,
        end_date: str,
        page: int,
        page_size: int,
        measurement_type: str,
        community: str,
        distributor: Optional[str] = None,
        fare: Optional[str] = None,
        province_municipality: Optional[str] = None,
        postal_code: Optional[str] = None,
        economic_sector: Optional[str] = None,
        tension: Optional[str] = None,
        time_discrimination: Optional[str] = None,
        sort: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for consumption data by various parameters.

        Args:
            start_date: Start date in format YYYY/MM/dd.
            end_date: End date in format YYYY/MM/dd.
            page: Page number (starts from 0).
            page_size: Number of results per page (max 2000).
            measurement_type: Measurement point type (01-05).
            community: Community code (01-19).
            distributor: Optional distributor code.
            fare: Optional fare code.
            province_municipality: Optional province or municipality code.
            postal_code: Optional postal code.
            economic_sector: Optional economic sector code (1-4).
            tension: Optional tension code (E0-E6).
            time_discrimination: Optional time discrimination code.
            sort: Optional sort criteria.

        Returns:
            Dict[str, Any]: The search results.
        """
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "page": page,
            "pageSize": page_size,
            "measurementType": measurement_type,
            "community": community
        }

        optional_params = {
            "distributor": distributor,
            "fare": fare,
            "provinceMunicipality": province_municipality,
            "postalCode": postal_code,
            "economicSector": economic_sector,
            "tension": tension,
            "timeDiscrimination": time_discrimination,
            "sort": sort
        }

        for key, value in optional_params.items():
            if value is not None:
                params[key] = value

        return self._get("/api-public/api-search", params)

    def api_sum_search(
        self,
        start_date: str,
        end_date: str,
        page: int,
        page_size: int,
        measurement_type: str,
        community: str,
        distributor: Optional[str] = None,
        fare: Optional[str] = None,
        province_municipality: Optional[str] = None,
        postal_code: Optional[str] = None,
        economic_sector: Optional[str] = None,
        tension: Optional[str] = None,
        time_discrimination: Optional[str] = None,
        sort: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for summarized consumption data by various parameters.

        Args:
            start_date: Start date in format YYYY/MM/dd.
            end_date: End date in format YYYY/MM/dd.
            page: Page number (starts from 0).
            page_size: Number of results per page (max 2000).
            measurement_type: Measurement point type (01-05).
            community: Community code (01-19).
            distributor: Optional distributor code.
            fare: Optional fare code.
            province_municipality: Optional province or municipality code.
            postal_code: Optional postal code.
            economic_sector: Optional economic sector code (1-4).
            tension: Optional tension code (E0-E6).
            time_discrimination: Optional time discrimination code.
            sort: Optional sort criteria.

        Returns:
            Dict[str, Any]: The summarized search results.
        """
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "page": page,
            "pageSize": page_size,
            "measurementType": measurement_type,
            "community": community
        }

        optional_params = {
            "distributor": distributor,
            "fare": fare,
            "provinceMunicipality": province_municipality,
            "postalCode": postal_code,
            "economicSector": economic_sector,
            "tension": tension,
            "timeDiscrimination": time_discrimination,
            "sort": sort
        }

        for key, value in optional_params.items():
            if value is not None:
                params[key] = value

        return self._get("/api-public/api-sum-search", params)

    def api_search_auto(
        self,
        start_date: str,
        end_date: str,
        page: int,
        page_size: int,
        community: str,
        distributor: Optional[str] = None,
        self_consumption: Optional[str] = None,
        province: Optional[str] = None,
        sort: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for auto-consumption data by various parameters.

        Args:
            start_date: Start date in format YYYY/MM/dd.
            end_date: End date in format YYYY/MM/dd.
            page: Page number (starts from 0).
            page_size: Number of results per page (max 2000).
            community: Community code (01-19).
            distributor: Optional distributor code.
            self_consumption: Optional self-consumption code.
            province: Optional province code.
            sort: Optional sort criteria.

        Returns:
            Dict[str, Any]: The auto-consumption search results.
        """
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "page": page,
            "pageSize": page_size,
            "community": community
        }

        optional_params = {
            "distributor": distributor,
            "selfConsumption": self_consumption,
            "province": province,
            "sort": sort
        }

        for key, value in optional_params.items():
            if value is not None:
                params[key] = value

        return self._get("/api-public/api-search-auto", params)
