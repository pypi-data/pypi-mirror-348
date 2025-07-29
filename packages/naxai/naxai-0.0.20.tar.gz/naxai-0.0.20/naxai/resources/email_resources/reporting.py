"""
Email reporting resource for the Naxai SDK.

This module provides access to email reporting functionality, including metrics analysis
and URL click tracking to help users understand email campaign performance and recipient
engagement. It serves as a container for more specialized reporting resources.
"""

from .reporting_resources.metrics import MetricsResource
from .reporting_resources.clicked_urls import ClickedUrlsResource

class ReportingResource:
    """ reporting resource for email resource"""

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/reporting"

        self.metrics = MetricsResource(client, self.root_path)
        self.cliqued_urls = ClickedUrlsResource(client, self.root_path)
