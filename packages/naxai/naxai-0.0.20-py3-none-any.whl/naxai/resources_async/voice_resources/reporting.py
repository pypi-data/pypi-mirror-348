"""
Asynchronous voice reporting resource for the Naxai SDK.

This module serves as a container for specialized asynchronous voice call reporting resources,
providing access to comprehensive metrics and analytics for different call types. It includes
resources for analyzing outbound calls, inbound calls, and call transfers, enabling users to
monitor and optimize their voice communication performance in a non-blocking manner suitable
for high-performance asynchronous applications.
"""

from naxai.resources_async.voice_resources.reporting_resources.outbound import OutboundResource
from naxai.resources_async.voice_resources.reporting_resources.inbound import InboundResource
from naxai.resources_async.voice_resources.reporting_resources.transfer import TransferResource

class ReportingResource:
    """ reporting resource for voice resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/reporting/metrics"
        self.outbound: OutboundResource = OutboundResource(self._client, self.root_path)
        self.inbound: InboundResource = InboundResource(self._client, self.root_path)
        self.transfer: TransferResource = TransferResource(self._client, self.root_path)
