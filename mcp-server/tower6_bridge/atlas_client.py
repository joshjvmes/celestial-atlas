"""
Atlas API Client - Tower 6 MCP Bridge

Connects to the Celestial Atlas API (local or Railway).
"""
from __future__ import annotations

import httpx
from typing import Dict, Any


class AtlasClient:
    """HTTP client for Celestial Atlas API"""

    def __init__(self, base_url: str, timeout_s: float = 20.0):
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s

    async def _request(self, method: str, path: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make HTTP request to Atlas API"""
        url = self.base_url + path
        async with httpx.AsyncClient(timeout=self.timeout_s) as client:
            r = await client.request(method, url, params=params)
            r.raise_for_status()
            return r.json()

    async def get_atlas_by_date(self, date: str) -> Dict[str, Any]:
        """
        Get constellation data for a specific date.

        Args:
            date: Date string in YYYY-MM-DD format

        Returns:
            Complete Atlas payload with constellation data
        """
        return await self._request("GET", "/atlas", params={"date": date})

    async def get_atlas_by_coordinate(self, S: int, L: int, P: int) -> Dict[str, Any]:
        """
        Get constellation by Sky Address coordinates.

        Args:
            S: Solar Month (1-11)
            L: Lunar Month (1-13)
            P: Prime Day (1-7)

        Returns:
            Complete Atlas payload for the given coordinates
        """
        return await self._request("GET", "/atlas/coordinate", params={"S": S, "L": L, "P": P})

    async def get_today(self) -> Dict[str, Any]:
        """Get today's constellation"""
        return await self._request("GET", "/atlas/today")

    async def get_gates(self) -> Dict[str, Any]:
        """Get all 7 Spiral Gate definitions"""
        return await self._request("GET", "/atlas/gates")

    async def get_solar_keys(self) -> Dict[str, Any]:
        """Get all 11 Solar Key Signatures"""
        return await self._request("GET", "/atlas/keys")

    async def get_lunar_patterns(self) -> Dict[str, Any]:
        """Get all 13 Lunar Pattern Types"""
        return await self._request("GET", "/atlas/patterns")
