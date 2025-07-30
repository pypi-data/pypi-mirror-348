"""Rich UI module for displaying IP threat assessments in the terminal."""

from datetime import datetime
from pathlib import Path

from loguru import logger
from rich.console import Console
from rich.table import Table

from .ip_api_client import IPApiResponse
from .ip_threat_assessment import IPThreatAssessment
from .rconn import ProcessInfo


class IPTableRenderer:
    """Renderer for displaying IP threat assessments in a Rich-formatted terminal table."""

    def __init__(self, html_dir: Path | None = None, max_cmdline_display: int = 5):
        """Initialize the renderer.

        Args:
            html_dir (Path | None, optional): Optional directory location for which to write an HTML report. Defaults to
                `None`.
            max_cmdline_display (int, optional): Number of command line arguments to display in the table for the
                process.
        """
        self.html_path: Path | None = None
        self.max_cmdline_display: int = 5

        if html_dir:
            html_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            self.html_path = html_dir / f"netwatcher-{timestamp}.html"
            self.console = Console(record=True)
        else:
            self.console = Console(record=False)

    @staticmethod
    def get_geolocation(ip_data: IPApiResponse) -> str:
        """Create a formatted geolocation string from IP data.

        Args:
            ip_data (IPApiResponse): IP geolocation and ownership data.

        Returns:
            str: Human-readable location string.
        """
        parts = [ip_data.city, ip_data.region]
        city_region = ", ".join([p for p in parts if p])
        zip_part = ip_data.zip or ""
        country = ip_data.country or ""

        return f"{city_region} {zip_part}".strip() + f"\n{country}" if country else city_region

    @staticmethod
    def get_ownership(ip_data: IPApiResponse) -> str:
        """Format ownership and network identity fields.

        Args:
            ip_data (IPApiResponse): IP geolocation and ownership data.

        Returns:
            str: Ownership summary with ISP, org, ASN, and reverse DNS information.
        """
        ownership_parts = [
            ("ISP", ip_data.isp),
            ("Organization", ip_data.org),
            ("AS", ip_data.as_),
            ("AS Name (RIR)", ip_data.asname),
            ("Reverse DNS", ip_data.reverse),
        ]
        return "\n".join(f"- {label}: {value}" for label, value in ownership_parts if value)

    def format_cmdline(self, args: list[str]) -> str:
        """Truncates the command line arguments for the process.

        Args:
            args (list[str]): Commands line arguments for the process.

        Returns:
            str: Truncated command line arguments for the process.
        """
        if not args:
            return ""

        if len(args) > self.max_cmdline_display:
            return " ".join(args[: self.max_cmdline_display]) + " …"
        return " ".join(args)

    def get_process_info(self, process_info: ProcessInfo | None = None) -> str:
        """Format ownership and network identity fields.

        Args:
            process_info (ProcessInfo | None, optional): Information about a locally running process. Defaults to
                `None`.

        Returns:
            str: Summary of process information.
        """
        if process_info is None:
            return ""

        cmdline_str = self.format_cmdline(process_info.cmdline) if process_info.cmdline else None

        process_info_parts = [
            ("Executable Path", process_info.exe),
            ("Command Line", cmdline_str),
            ("Process Name", process_info.name),
            ("PID", process_info.pid),
            ("Parent Name", process_info.parent_name),
            ("Parent PID", process_info.parent_pid),
        ]
        return "\n".join(f"- {label}: {value}" for label, value in process_info_parts if value is not None)

    def build_table(self, assessments: list[IPThreatAssessment]) -> Table:
        """Build a Rich table from a list of assessments.

        Args:
            assessments (List[IPThreatAssessment]): The data to populate the table with.

        Returns:
            Table: A Rich-formatted table object.
        """
        table = Table(title="IP Threat Assessment", show_lines=True, expand=True)
        table.add_column("IP", style="cyan")
        table.add_column("Geolocation")
        table.add_column("Ownership")
        table.add_column("Threat Level", style="bold")
        table.add_column("Assessment", style="red", overflow="fold")
        table.add_column("Process Info", style="magenta", overflow="fold")

        for assessment in assessments:
            ip = assessment.ip_data.query or ""
            geolocation = self.get_geolocation(assessment.ip_data)
            ownership = self.get_ownership(assessment.ip_data)
            threat_level = "[yellow]Suspicious" if assessment.is_suspicious else "[green]Clean"
            reasons = "\n".join(f"- {r}" for r in assessment.reasons) or ""
            process_info = self.get_process_info(assessment.process_info)

            table.add_row(ip, geolocation, ownership, threat_level, reasons, process_info)

        return table

    def render(self, assessments: list[IPThreatAssessment]) -> None:
        """Render a list of IP threat assessments as a Rich table.

        Args:
            assessments (list[IPThreatAssessment]): List of threat assessments to display.
        """
        if self.html_path:
            logger.info(f"Preparing to save HTML report to: {self.html_path}")

        table = self.build_table(assessments)
        self.console.print(table)

        if self.html_path:
            self.console.save_html(str(self.html_path), clear=True)
