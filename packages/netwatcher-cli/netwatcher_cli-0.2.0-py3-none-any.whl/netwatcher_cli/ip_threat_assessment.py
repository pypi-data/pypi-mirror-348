"""Module for IP Threat Assessment using IP-API responses."""

from loguru import logger
from pydantic import BaseModel

from .ip_api_client import IPApiResponse
from .rconn import ProcessInfo, RemoteConnection


class IPThreatAssessment(BaseModel):
    """Represents the result of a threat assessment for a single IP address."""

    ip_data: IPApiResponse
    is_suspicious: bool
    reasons: list[str]
    process_info: ProcessInfo | None = None

    @staticmethod
    def get_reasons(ip_data: IPApiResponse, country_code: str = "US") -> list[str]:
        """Analyzes the `IPApiResponse` and determines why an IP should be flagged.

        Args:
            ip_data (IPApiResponse): The response data for an individual IP.
            country_code (str): The user's expected country code (ISO 3166-1 alpha-2).

        Returns:
            list[str]: A list of reasons explaining why the IP is considered suspicious.
        """
        reasons: list[str] = []

        if ip_data.status != "success":
            reasons.append("Lookup failed")

        if ip_data.proxy:
            reasons.append("Proxy or VPN detected")

        if ip_data.hosting:
            reasons.append("Hosting provider or data center")

        if ip_data.mobile:
            reasons.append("Mobile network")

        if not ip_data.country_code:
            reasons.append("Missing IP origin country")
        elif ip_data.country_code != country_code:
            reasons.append(
                f"IP origin country ({ip_data.country_code}) is different from user's country ({country_code})"
            )

        return reasons

    @classmethod
    def from_batch_ip_data(
        cls,
        remote_conn_map: dict[str, RemoteConnection],
        responses: list[IPApiResponse],
        country_code: str = "US",
    ) -> list["IPThreatAssessment"]:
        """Converts a list of `IPApiResponse` instances into threat assessments.

        Args:
            remote_conn_map (dict[str, RemoteConnection]): Map from IP addresses to remote connection process info.
            responses (list[IPApiResponse]): A list of parsed IP-API response models.
            country_code (str, optional): The user's country code to compare against IP origins.

        Returns:
            list[IPThreatAssessment]: A list of enriched IP threat assessments.
        """
        ip_threat_assessments: list[IPThreatAssessment] = []

        for ip_data in responses:
            reasons = cls.get_reasons(ip_data, country_code)
            is_suspicious = bool(reasons)

            process_info = None
            if ip_data.query:
                remote_conn = remote_conn_map.get(ip_data.query)
                if remote_conn:
                    process_info = remote_conn.process_info
                else:
                    logger.debug(f"No remote connection found for IP {ip_data.query}")
            else:
                logger.debug(f"IPApiResponse missing query field: {ip_data}")

            ip_threat_assessments.append(
                cls(ip_data=ip_data, is_suspicious=is_suspicious, reasons=reasons, process_info=process_info)
            )

        logger.info(f"Created {len(ip_threat_assessments)} IP threat assessments")
        return ip_threat_assessments
