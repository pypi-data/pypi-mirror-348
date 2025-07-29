"""
GridAppSD IEEE 2030.5 Client

A comprehensive client for IEEE 2030.5 (Smart Energy Profile 2.0) servers
with persistent connection handling and extensible event processing.
"""

from abc import ABC
import logging
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
from enum import Enum
import urllib.parse
import uuid
import asyncio
import xml.etree.ElementTree as ET

import httpx

from .exceptions import (
    IEEE2030Error,
    AuthenticationError,
    ConnectionError,
    ResourceError,
    ParseError
)
from .handlers.base import IEEE2030EventHandler
from .utils.xml_parser import parse_xml, element_to_dict

# Set up logging
logger = logging.getLogger("gridappsd.ieee2030")


class ContentType(Enum):
    """Supported content types for IEEE 2030.5 communications."""
    XML = "application/xml"
    JSON = "application/json"
    EXI = "application/exi"  # Efficient XML Interchange


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


class ConnectionManager:
    """
    Manages persistent HTTP connections to IEEE 2030.5 servers with 
    automatic retries, timeouts, and connection pooling using httpx.
    """
    
    def __init__(
        self, 
        cert_path: Optional[str] = None, 
        key_path: Optional[str] = None,
        ca_cert_path: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        retry_backoff: float = 0.5
    ):
        """
        Initialize the connection manager.
        
        Args:
            cert_path: Path to client certificate file
            key_path: Path to client private key file
            ca_cert_path: Path to CA certificate file for server verification
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            retry_backoff: Backoff factor for retries
        """
        self.cert_path = cert_path
        self.key_path = key_path
        self.ca_cert_path = ca_cert_path
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff
        
        # HTTPX client configuration
        client_kwargs = {
            "timeout": timeout,
            "follow_redirects": True,
        }
        
        # Configure TLS certificates if provided
        if cert_path and key_path:
            client_kwargs["cert"] = (cert_path, key_path)
        
        if ca_cert_path:
            client_kwargs["verify"] = ca_cert_path
        
        # Create persistent client
        self.client = httpx.Client(**client_kwargs)
        
        # Create async client - don't use the same transport!
        # For AsyncClient, we don't specify the transport directly
        self.async_client = httpx.AsyncClient(**client_kwargs)
    
    def request(
        self, 
        method: str, 
        url: str, 
        data: Optional[Union[Dict, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        content_type: ContentType = ContentType.JSON
    ) -> httpx.Response:
        """
        Make an HTTP request to the IEEE 2030.5 server.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            url: URL to request
            data: Data to send, if any
            headers: Additional headers
            content_type: Content type to use
            
        Returns:
            Response from the server
        
        Raises:
            ConnectionError: If connection fails
            AuthenticationError: If authentication fails
            ResourceError: If resource not found or access denied
        """
        if headers is None:
            headers = {}
        
        # Set content type header
        headers["Accept"] = content_type.value
        if data and "Content-Type" not in headers:
            headers["Content-Type"] = content_type.value
        
        try:
            # Make the request with automatic retries
            response = self.client.request(
                method, 
                url, 
                content=data,
                headers=headers,
            )
            
            # Handle common errors
            if response.status_code == 401 or response.status_code == 403:
                raise AuthenticationError(f"Authentication failed: {response.status_code} - {response.text}")
            elif response.status_code == 404:
                raise ResourceError(f"Resource not found: {url}")
            elif response.status_code >= 400:
                raise ResourceError(f"Request failed: {response.status_code} - {response.text}")
            
            return response
            
        except httpx.HTTPError as e:
            raise ConnectionError(f"Connection failed: {str(e)}")
    
    async def async_request(
        self, 
        method: str, 
        url: str, 
        data: Optional[Union[Dict, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        content_type: ContentType = ContentType.JSON
    ) -> httpx.Response:
        """
        Make an asynchronous HTTP request to the IEEE 2030.5 server.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            url: URL to request
            data: Data to send, if any
            headers: Additional headers
            content_type: Content type to use
            
        Returns:
            Response from the server
        
        Raises:
            ConnectionError: If connection fails
            AuthenticationError: If authentication fails
            ResourceError: If resource not found or access denied
        """
        if headers is None:
            headers = {}
        
        # Set content type header
        headers["Accept"] = content_type.value
        if data and "Content-Type" not in headers:
            headers["Content-Type"] = content_type.value
        
        try:
            # Make the request with automatic retries
            response = await self.async_client.request(
                method, 
                url, 
                content=data,
                headers=headers,
            )
            
            # Handle common errors
            if response.status_code == 401 or response.status_code == 403:
                raise AuthenticationError(f"Authentication failed: {response.status_code} - {response.text}")
            elif response.status_code == 404:
                raise ResourceError(f"Resource not found: {url}")
            elif response.status_code >= 400:
                raise ResourceError(f"Request failed: {response.status_code} - {response.text}")
            
            return response
            
        except httpx.HTTPError as e:
            raise ConnectionError(f"Connection failed: {str(e)}")
    
    def close(self):
        """Close the connection and release resources."""
        if self.client:
            self.client.close()
        
        # Close async client if event loop is running
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.async_client.aclose())
            else:
                asyncio.run(self.async_client.aclose())
        except Exception as e:
            logger.debug(f"Error closing async client: {e}")


class IEEE2030Client:
    """
    Client for IEEE 2030.5 (Smart Energy Profile 2.0) servers with persistent
    connections and extensible event handling.
    """
    
    def __init__(
        self, 
        base_url: str,
        event_handler: IEEE2030EventHandler,
        cert_path: Optional[str] = None, 
        key_path: Optional[str] = None,
        ca_cert_path: Optional[str] = None,
        content_type: ContentType = ContentType.JSON,
        poll_interval: int = 60
    ):
        """
        Initialize the IEEE 2030.5 client.
        
        Args:
            base_url: Base URL of the IEEE 2030.5 server
            event_handler: Event handler instance
            cert_path: Path to client certificate file
            key_path: Path to client private key file
            ca_cert_path: Path to CA certificate file
            content_type: Preferred content type for communication
            poll_interval: Polling interval in seconds for subscription updates
        """
        self.base_url = base_url.rstrip("/")
        self.event_handler = event_handler
        self.content_type = content_type
        self.poll_interval = poll_interval
        self.subscriptions = {}
        self._polling_task = None
        self._stopping = False
        
        # Create connection manager
        self.connection = ConnectionManager(
            cert_path=cert_path,
            key_path=key_path,
            ca_cert_path=ca_cert_path
        )
    
    def connect(self) -> bool:
        """
        Establish initial connection to the server and retrieve device capability.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Attempt to access the root resource to verify connection
            response = self.connection.request("GET", self.base_url)
            
            # Notify of successful connection
            self.event_handler.on_connect(self)
            logger.info(f"Connected to IEEE 2030.5 server: {self.base_url}")
            
            return True
            
        except Exception as e:
            self.event_handler.on_error(self, e)
            logger.error(f"Failed to connect to IEEE 2030.5 server: {e}")
            return False
    
    async def async_connect(self) -> bool:
        """
        Asynchronously establish initial connection to the server.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Attempt to access the root resource to verify connection
            logger.info(f"Attempting async connection to {self.base_url}")
            response = await self.connection.async_request("GET", self.base_url)
            
            # Notify of successful connection
            logger.info(f"Successfully connected to IEEE 2030.5 server: {self.base_url}")
            self.event_handler.on_connect(self)
            
            return True
            
        except Exception as e:
            self.event_handler.on_error(self, e)
            logger.error(f"Failed to connect to IEEE 2030.5 server: {e}", exc_info=True)
            return False
        
    def disconnect(self):
        """Disconnect from the server and clean up resources."""
        try:
            self.stop_polling()
            self.connection.close()
            self.event_handler.on_disconnect(self, "Client disconnected")
            logger.info("Disconnected from IEEE 2030.5 server")
        except Exception as e:
            self.event_handler.on_error(self, e)
            logger.error(f"Error during disconnect: {e}")
    
    def get_device_capability(self) -> Dict:
        """
        Get the device capability from the server.
        
        Returns:
            Device capability information
        """
        response = self.connection.request("GET", f"{self.base_url}/dcap")
        return self._parse_response(response)
    
    def get_end_device(self, device_id: Optional[str] = None) -> Dict:
        """
        Get end device information.
        
        Args:
            device_id: Optional device ID. If None, returns all devices.
            
        Returns:
            End device information
        """
        url = f"{self.base_url}/edev"
        if device_id:
            url = f"{url}/{device_id}"
        
        response = self.connection.request("GET", url)
        return self._parse_response(response)
    
    def get_metering(self, device_id: str) -> Dict:
        """
        Get metering information for a specific device.
        
        Args:
            device_id: Device ID
            
        Returns:
            Metering information
        """
        url = f"{self.base_url}/edev/{device_id}/mup"
        response = self.connection.request("GET", url)
        return self._parse_response(response)
    
    def get_demand_response_program(self, program_id: Optional[str] = None) -> Dict:
        """
        Get demand response program information.
        
        Args:
            program_id: Optional program ID. If None, returns all programs.
            
        Returns:
            Demand response program information
        """
        url = f"{self.base_url}/drp"
        if program_id:
            url = f"{url}/{program_id}"
        
        response = self.connection.request("GET", url)
        return self._parse_response(response)
    
    def get_demand_response_events(self, program_id: str) -> List[Dict]:
        """
        Get demand response events for a specific program.
        
        Args:
            program_id: Program ID
            
        Returns:
            List of demand response events
        """
        url = f"{self.base_url}/drp/{program_id}/dre"
        response = self.connection.request("GET", url)
        return self._parse_response(response)
    
    def create_subscription(self, resource_uri: str, expiration_seconds: int = 86400) -> Dict:
        """
        Create a subscription for a resource.
        
        Args:
            resource_uri: URI of the resource to subscribe to (relative to base URL)
            expiration_seconds: Subscription expiration time in seconds
            
        Returns:
            Subscription information
        """
        # Normalize resource URI to be relative to base URL
        if resource_uri.startswith(self.base_url):
            resource_uri = resource_uri[len(self.base_url):]
        resource_uri = resource_uri.lstrip("/")
        
        # Construct subscription request
        subscription_data = {
            "subscribedResource": resource_uri,
            "notificationURI": "http://localhost",  # Placeholder, we'll use polling
            "encoding": self.content_type.value,
            "duration": expiration_seconds
        }
        
        # Convert to appropriate format based on content type
        if self.content_type == ContentType.JSON:
            data = json.dumps(subscription_data)
        else:  # XML is the default fallback
            root = ET.Element("Subscription")
            ET.SubElement(root, "subscribedResource").text = resource_uri
            ET.SubElement(root, "notificationURI").text = "http://localhost"
            ET.SubElement(root, "encoding").text = self.content_type.value
            ET.SubElement(root, "duration").text = str(expiration_seconds)
            data = ET.tostring(root, encoding="utf-8")
        
        # Create subscription
        url = f"{self.base_url}/sub"
        response = self.connection.request(
            "POST", 
            url, 
            data=data,
            content_type=self.content_type
        )
        
        # Parse response and store subscription
        subscription_info = self._parse_response(response)
        subscription_id = self._extract_id_from_uri(response.headers.get("Location", ""))
        
        if subscription_id:
            self.subscriptions[subscription_id] = {
                "resource": resource_uri,
                "expires": datetime.now() + timedelta(seconds=expiration_seconds),
                "last_checked": datetime.now()
            }
        
        return subscription_info
    
    def delete_subscription(self, subscription_id: str) -> bool:
        """
        Delete a subscription.
        
        Args:
            subscription_id: ID of the subscription to delete
            
        Returns:
            True if deleted successfully
        """
        url = f"{self.base_url}/sub/{subscription_id}"
        
        try:
            self.connection.request("DELETE", url)
            if subscription_id in self.subscriptions:
                del self.subscriptions[subscription_id]
            return True
        except ResourceError:
            return False
    
    def check_subscription(self, subscription_id: str) -> Dict:
        """
        Check a subscription for updates.
        
        Args:
            subscription_id: ID of the subscription to check
            
        Returns:
            Updated resource data if available
        """
        if subscription_id not in self.subscriptions:
            raise ResourceError(f"Subscription not found: {subscription_id}")
        
        # Get the resource URI
        resource_uri = self.subscriptions[subscription_id]["resource"]
        url = f"{self.base_url}/{resource_uri}"
        
        # Check if resource has been updated
        response = self.connection.request("GET", url)
        data = self._parse_response(response)
        
        # Update last checked timestamp
        self.subscriptions[subscription_id]["last_checked"] = datetime.now()
        
        # Notify handler of subscription update
        self.event_handler.on_subscription_update(self, resource_uri, data)
        
        return data
    
    def start_polling(self):
        """Start background polling for subscription updates."""
        if self._polling_task is None:
            self._stopping = False
            loop = asyncio.get_event_loop()
            self._polling_task = loop.create_task(self._polling_loop())
            logger.info("Started polling for subscription updates")
    
    def stop_polling(self):
        """Stop background polling for subscription updates."""
        if self._polling_task:
            self._stopping = True
            # Wait for polling to stop gracefully
            if self._polling_task.done():
                self._polling_task = None
            logger.info("Stopped polling for subscription updates")
    
    async def _polling_loop(self):
        """Background task that polls for subscription updates."""
        while not self._stopping:
            try:
                # Check all active subscriptions
                for sub_id, sub_info in list(self.subscriptions.items()):

                    # Renew if about to expire
                    renewal_check = datetime.now() > sub_info["expires"] - timedelta(minutes=5)
                    print(f"Subscription {sub_id}, Expires: {sub_info['expires']}, Should renew: {renewal_check}")
                    # Renew if about to expire
                    if renewal_check:
                        try:
                            # Try to recreate the subscription
                            self.create_subscription(
                                sub_info["resource"], 
                                expiration_seconds=24*60*60
                            )
                            logger.info(f"Renewed subscription: {sub_id}")
                        except Exception as e:
                            logger.error(f"Failed to renew subscription {sub_id}: {e}")
                    
                    # Check for updates
                    try:
                        # Use async version of check_subscription
                        await self._async_check_subscription(sub_id)
                    except Exception as e:
                        logger.error(f"Error checking subscription {sub_id}: {e}")
                
                # Wait for next poll interval
                await asyncio.sleep(self.poll_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in polling loop: {e}")
                await asyncio.sleep(self.poll_interval)
    
    async def _async_check_subscription(self, subscription_id: str) -> Dict:
        """
        Asynchronously check a subscription for updates.
        
        Args:
            subscription_id: ID of the subscription to check
            
        Returns:
            Updated resource data if available
        """
        if subscription_id not in self.subscriptions:
            raise ResourceError(f"Subscription not found: {subscription_id}")
        
        # Get the resource URI
        resource_uri = self.subscriptions[subscription_id]["resource"]
        url = f"{self.base_url}/{resource_uri}"
        
        # Check if resource has been updated
        response = await self.connection.async_request("GET", url)
        data = self._parse_response(response)
        
        # Update last checked timestamp
        self.subscriptions[subscription_id]["last_checked"] = datetime.now()
        
        # Notify handler of subscription update
        self.event_handler.on_subscription_update(self, resource_uri, data)
        
        return data
    
    def _parse_response(self, response: httpx.Response) -> Any:
        """
        Parse response from server based on content type.
        
        Args:
            response: Response object
            
        Returns:
            Parsed response data
        """
        content_type = response.headers.get("Content-Type", "")
        
        if not response.content:
            return {}
        
        try:
            if "json" in content_type:
                return response.json()
            elif "xml" in content_type:
                return self._parse_xml(response.content)
            elif "exi" in content_type:
                # Note: EXI parsing would require additional libraries
                raise ParseError("EXI parsing not implemented")
            else:
                # Try to parse as JSON first, fall back to XML
                try:
                    return response.json()
                except:
                    return self._parse_xml(response.content)
        except Exception as e:
            raise ParseError(f"Failed to parse response: {str(e)}")
    
    def _parse_xml(self, xml_content: bytes) -> Dict:
        """
        Parse XML content into a dictionary.
        
        Args:
            xml_content: XML content as bytes
            
        Returns:
            Dictionary representation of XML
        """
        try:
            root = ET.fromstring(xml_content)
            return {root.tag: self._element_to_dict(root)}
        except Exception as e:
            raise ParseError(f"Failed to parse XML: {str(e)}")
    
    def _element_to_dict(self, element: ET.Element) -> Dict:
        """
        Convert XML element to dictionary.
        
        Args:
            element: XML element
            
        Returns:
            Dictionary representation
        """
        result = {}
        
        # Add attributes
        for key, value in element.attrib.items():
            result[f"@{key}"] = value
        
        # Add children
        for child in element:
            child_dict = self._element_to_dict(child)
            
            if child.tag in result:
                # If this tag already exists, convert to list or append
                if isinstance(result[child.tag], list):
                    result[child.tag].append(child_dict)
                else:
                    result[child.tag] = [result[child.tag], child_dict]
            else:
                result[child.tag] = child_dict
        
        # Add text content
        if element.text and element.text.strip():
            if len(result) == 0:
                return element.text.strip()
            else:
                result["#text"] = element.text.strip()
        
        return result
    
    def _extract_id_from_uri(self, uri: str) -> str:
        """
        Extract ID from a URI.
        
        Args:
            uri: URI string
            
        Returns:
            Extracted ID
        """
        if not uri:
            return ""
        
        # Extract the last part of the URI path
        parsed = urllib.parse.urlparse(uri)
        path_parts = parsed.path.rstrip("/").split("/")
        return path_parts[-1] if path_parts else ""