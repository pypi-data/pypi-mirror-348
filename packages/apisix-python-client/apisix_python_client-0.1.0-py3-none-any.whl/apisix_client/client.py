import requests
import json
from typing import Dict, List, Optional, Union, Any

class ApisixClient:
    """
    A simple Python client for Apache APISIX.
    
    This client provides methods to interact with the APISIX Admin API.
    """
    
    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the APISIX client.
        
        Args:
            base_url: The base URL of the APISIX Admin API (e.g., 'http://localhost:9080/apisix/admin')
            api_key: The API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': api_key
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        Make an HTTP request to the APISIX Admin API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request data (for POST/PUT)
            
        Returns:
            API response as a dictionary
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=self.headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Error connecting to APISIX: {str(e)}")
    
    #
    # Routes API
    #
    
    def list_routes(self) -> List[Dict]:
        """List all routes"""
        response = self._make_request('GET', '/routes')
        return response.get('node', {}).get('nodes', [])
    
    def get_route(self, route_id: str) -> Dict:
        """Get a route by ID"""
        return self._make_request('GET', f'/routes/{route_id}')
    
    def create_route(self, route_config: Dict) -> Dict:
        """Create a new route"""
        return self._make_request('POST', '/routes', data=route_config)
    
    def update_route(self, route_id: str, route_config: Dict) -> Dict:
        """Update an existing route"""
        return self._make_request('PUT', f'/routes/{route_id}', data=route_config)
    
    def delete_route(self, route_id: str) -> Dict:
        """Delete a route"""
        return self._make_request('DELETE', f'/routes/{route_id}')
    
    #
    # Upstream API
    #
    
    def list_upstreams(self) -> List[Dict]:
        """List all upstreams"""
        response = self._make_request('GET', '/upstreams')
        return response.get('node', {}).get('nodes', [])
    
    def get_upstream(self, upstream_id: str) -> Dict:
        """Get an upstream by ID"""
        return self._make_request('GET', f'/upstreams/{upstream_id}')
    
    def create_upstream(self, upstream_config: Dict) -> Dict:
        """Create a new upstream"""
        return self._make_request('POST', '/upstreams', data=upstream_config)
    
    def update_upstream(self, upstream_id: str, upstream_config: Dict) -> Dict:
        """Update an existing upstream"""
        return self._make_request('PUT', f'/upstreams/{upstream_id}', data=upstream_config)
    
    def delete_upstream(self, upstream_id: str) -> Dict:
        """Delete an upstream"""
        return self._make_request('DELETE', f'/upstreams/{upstream_id}')
    
    #
    # SSL API
    #
    
    def list_ssl(self) -> List[Dict]:
        """List all SSL certificates"""
        response = self._make_request('GET', '/ssl')
        return response.get('node', {}).get('nodes', [])
    
    def get_ssl(self, ssl_id: str) -> Dict:
        """Get an SSL certificate by ID"""
        return self._make_request('GET', f'/ssl/{ssl_id}')
    
    def create_ssl(self, ssl_config: Dict) -> Dict:
        """Create a new SSL certificate"""
        return self._make_request('POST', '/ssl', data=ssl_config)
    
    def update_ssl(self, ssl_id: str, ssl_config: Dict) -> Dict:
        """Update an existing SSL certificate"""
        return self._make_request('PUT', f'/ssl/{ssl_id}', data=ssl_config)
    
    def delete_ssl(self, ssl_id: str) -> Dict:
        """Delete an SSL certificate"""
        return self._make_request('DELETE', f'/ssl/{ssl_id}')
    
    #
    # Consumer API
    #
    
    def list_consumers(self) -> List[Dict]:
        """List all consumers"""
        response = self._make_request('GET', '/consumers')
        return response.get('node', {}).get('nodes', [])
    
    def get_consumer(self, username: str) -> Dict:
        """Get a consumer by username"""
        return self._make_request('GET', f'/consumers/{username}')
    
    def create_consumer(self, consumer_config: Dict) -> Dict:
        """Create a new consumer"""
        return self._make_request('POST', '/consumers', data=consumer_config)
    
    def update_consumer(self, username: str, consumer_config: Dict) -> Dict:
        """Update an existing consumer"""
        return self._make_request('PUT', f'/consumers/{username}', data=consumer_config)
    
    def delete_consumer(self, username: str) -> Dict:
        """Delete a consumer"""
        return self._make_request('DELETE', f'/consumers/{username}')