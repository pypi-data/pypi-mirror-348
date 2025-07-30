import unittest
from unittest import mock
from apisix_client import ApisixClient

class TestApisixClient(unittest.TestCase):
    def setUp(self):
        self.client = ApisixClient(
            base_url="http://localhost:9080/apisix/admin",
            api_key="test-key"
        )
    
    @mock.patch("requests.get")
    def test_list_routes(self, mock_get):
        # Mock the response
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            "node": {
                "nodes": [
                    {"key": "route1", "value": {"uri": "/test1"}},
                    {"key": "route2", "value": {"uri": "/test2"}}
                ]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.list_routes()
        
        # Validate
        self.assertEqual(len(result), 2)
        mock_get.assert_called_once_with(
            "http://localhost:9080/apisix/admin/routes",
            headers={"Content-Type": "application/json", "X-API-KEY": "test-key"}
        )
    
    @mock.patch("requests.post")
    def test_create_route(self, mock_post):
        # Mock the response
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            "key": "route1",
            "value": {"uri": "/test"}
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Call the method
        route_config = {"uri": "/test", "upstream": {"type": "roundrobin", "nodes": {"example.com:80": 1}}}
        result = self.client.create_route(route_config)
        
        # Validate
        self.assertEqual(result["key"], "route1")
        mock_post.assert_called_once_with(
            "http://localhost:9080/apisix/admin/routes",
            headers={"Content-Type": "application/json", "X-API-KEY": "test-key"},
            json=route_config
        )
    
    @mock.patch("requests.get")
    def test_get_route(self, mock_get):
        # Mock the response
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            "key": "route1",
            "value": {"uri": "/test"}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.get_route("route1")
        
        # Validate
        self.assertEqual(result["key"], "route1")
        mock_get.assert_called_once_with(
            "http://localhost:9080/apisix/admin/routes/route1",
            headers={"Content-Type": "application/json", "X-API-KEY": "test-key"}
        )
    
    @mock.patch("requests.put")
    def test_update_route(self, mock_put):
        # Mock the response
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            "key": "route1",
            "value": {"uri": "/updated"}
        }
        mock_response.raise_for_status.return_value = None
        mock_put.return_value = mock_response
        
        # Call the method
        route_config = {"uri": "/updated"}
        result = self.client.update_route("route1", route_config)
        
        # Validate
        self.assertEqual(result["key"], "route1")
        mock_put.assert_called_once_with(
            "http://localhost:9080/apisix/admin/routes/route1",
            headers={"Content-Type": "application/json", "X-API-KEY": "test-key"},
            json=route_config
        )
    
    @mock.patch("requests.delete")
    def test_delete_route(self, mock_delete):
        # Mock the response
        mock_response = mock.Mock()
        mock_response.json.return_value = {"deleted": "success"}
        mock_response.raise_for_status.return_value = None
        mock_delete.return_value = mock_response
        
        # Call the method
        result = self.client.delete_route("route1")
        
        # Validate
        self.assertEqual(result["deleted"], "success")
        mock_delete.assert_called_once_with(
            "http://localhost:9080/apisix/admin/routes/route1",
            headers={"Content-Type": "application/json", "X-API-KEY": "test-key"}
        )


if __name__ == "__main__":
    unittest.main()