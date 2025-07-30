import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

class Shopify:
    def __init__(self):
        # Initialize with environment variables or default values
        self.shop_url = os.getenv('SHOP_URL')
        self.access_token = os.getenv('SHOPIFY_ACCESS_TOKEN')
        self.api_version = os.getenv('SHOPIFY_API_VERSION')
        
        # Set up headers
        self.headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }
        self.base_url = f"https://{self.shop_url}/admin/api/{self.api_version}"

    def get_products(self):
        """Get all products from the shop."""
        url = f"{self.base_url}/products.json"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def create_product(self, payload):
        """Create a new product in the shop."""
        url = f"{self.base_url}/products.json"
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    def update_product(self, product_id, payload):
        """Update an existing product."""
        url = f"{self.base_url}/products/{product_id}.json"
        response = requests.put(url, headers=self.headers, json=payload)
        return response.json()

    def delete_product(self, product_id):
        """Delete a product from the shop."""
        url = f"{self.base_url}/products/{product_id}.json"
        response = requests.delete(url, headers=self.headers)
        return response.status_code

    def get_orders(self):
        """Get all orders from the shop."""
        url = f"{self.base_url}/orders.json"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_order(self, order_id):
        """Get a specific order by ID."""
        url = f"{self.base_url}/orders/{order_id}.json"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_customers(self):
        """Get all customers from the shop."""
        url = f"{self.base_url}/customers.json"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def create_customer(self, payload):
        """Create a new customer in the shop."""
        url = f"{self.base_url}/customers.json"
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

