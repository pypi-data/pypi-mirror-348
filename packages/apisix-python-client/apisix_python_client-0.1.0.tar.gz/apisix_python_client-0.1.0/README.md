APISIX Python Client
A simple and easy-to-use Python client for Apache APISIX.

This client provides methods to interact with the APISIX Admin API, making it easy to manage routes, upstreams, SSL certificates, and consumers from your Python applications.

Installation
bash
pip install apisix-python-client
Usage
Initializing the client
python
from apisix_client import ApisixClient

# Initialize the client
client = ApisixClient(
    base_url='http://localhost:9080/apisix/admin',
    api_key='edd1c9f034335f136f87ad84b625c8f1'  # Replace with your actual API key
)
Working with Routes
python
# List all routes
routes = client.list_routes()
print(f"Total routes: {len(routes)}")

# Create a new route
route_config = {
    "uri": "/hello",
    "upstream": {
        "type": "roundrobin",
        "nodes": {
            "example.com:80": 1
        }
    }
}
new_route = client.create_route(route_config)
print(f"Created route with ID: {new_route.get('key')}")

# Get a specific route
route_id = "1"  # Replace with your actual route ID
route = client.get_route(route_id)
print(route)

# Update a route
updated_config = {
    "uri": "/hello",
    "upstream": {
        "type": "roundrobin",
        "nodes": {
            "example.com:80": 2
        }
    }
}
client.update_route(route_id, updated_config)

# Delete a route
client.delete_route(route_id)
Working with Upstreams
python
# List all upstreams
upstreams = client.list_upstreams()

# Create a new upstream
upstream_config = {
    "type": "roundrobin",
    "nodes": {
        "example.com:80": 1
    }
}
new_upstream = client.create_upstream(upstream_config)

# Get a specific upstream
upstream_id = "1"  # Replace with your actual upstream ID
upstream = client.get_upstream(upstream_id)

# Update an upstream
updated_upstream = {
    "type": "roundrobin",
    "nodes": {
        "example.com:80": 2,
        "backup.example.com:80": 1
    }
}
client.update_upstream(upstream_id, updated_upstream)

# Delete an upstream
client.delete_upstream(upstream_id)
Working with SSL Certificates
python
# List all SSL certificates
certificates = client.list_ssl()

# Create a new SSL certificate
ssl_config = {
    "cert": "...",  # Your certificate content
    "key": "...",   # Your key content
    "snis": ["example.com"]
}
new_ssl = client.create_ssl(ssl_config)

# Get a specific SSL certificate
ssl_id = "1"  # Replace with your actual SSL ID
ssl = client.get_ssl(ssl_id)

# Update an SSL certificate
updated_ssl = {
    "cert": "...",  # Your updated certificate content
    "key": "...",   # Your updated key content
    "snis": ["example.com", "www.example.com"]
}
client.update_ssl(ssl_id, updated_ssl)

# Delete an SSL certificate
client.delete_ssl(ssl_id)
Working with Consumers
python
# List all consumers
consumers = client.list_consumers()

# Create a new consumer
consumer_config = {
    "username": "john",
    "plugins": {
        "key-auth": {
            "key": "auth-one"
        }
    }
}
new_consumer = client.create_consumer(consumer_config)

# Get a specific consumer
username = "john"
consumer = client.get_consumer(username)

# Update a consumer
updated_consumer = {
    "username": "john",
    "plugins": {
        "key-auth": {
            "key": "auth-two"
        }
    }
}
client.update_consumer(username, updated_consumer)

# Delete a consumer
client.delete_consumer(username)
Development
Setup development environment
bash
# Clone the repository
git clone https://github.com/yourusername/apisix-python-client.git
cd apisix-python-client

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
Running tests
bash
pytest
License
This project is licensed under the MIT License - see the LICENSE file for details.

