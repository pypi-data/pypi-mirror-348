"""Base event handler for IEEE 2030.5 client."""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

# Forward reference for type hints
import typing
if typing.TYPE_CHECKING:
    from ..client import IEEE2030Client

logger = logging.getLogger("gridappsd.ieee2030")


class IEEE2030EventHandler(ABC):
    """
    Abstract base class for IEEE 2030.5 event handlers.
    
    Extend this class and override methods to handle specific events
    from an IEEE 2030.5 server.
    """

    def on_connect(self, client: 'IEEE2030Client'):
        """Called when the client establishes a connection."""
        pass
    
    def on_disconnect(self, client: 'IEEE2030Client', reason: str = ""):
        """Called when the client disconnects."""
        pass
    
    def on_error(self, client: 'IEEE2030Client', error: Exception):
        """Called when an error occurs."""
        logger.error(f"Error: {error}", exc_info=True)
    
    def on_device_capability_changed(self, client: 'IEEE2030Client', capability: Dict):
        """Called when a device capability changes."""
        pass
    
    def on_end_device_event(self, client: 'IEEE2030Client', event: Dict):
        """Called when an end device event occurs."""
        pass
    
    def on_demand_response_event(self, client: 'IEEE2030Client', event: Dict):
        """Called when a demand response event occurs."""
        pass
    
    def on_metering_data(self, client: 'IEEE2030Client', data: Dict):
        """Called when metering data is received."""
        pass
    
    def on_subscription_update(self, client: 'IEEE2030Client', resource: str, data: Any):
        """Called when a subscribed resource is updated."""
        pass