from crewai.tools import tool
import requests
import json

BASE_URL = "http://127.0.0.1:8000"


@tool("Get all available products")
def get_all_products() -> str:
    """Fetch all available products from the backend API"""
    try:
        response = requests.get(f"{BASE_URL}/product", timeout=10)
        response.raise_for_status()
        products = response.json()
        return json.dumps(products, indent=2)
    except requests.exceptions.ConnectionError:
        return "Connection failed. Available products: NASA Advanced Lithium-Sulfur Battery (product_3), NASA Portable Solar Charging Array (product_4), NASA Carbon Fiber Composite Panel (product_5)"
    except Exception as e:
        return f"Error: {str(e)}. Available products: NASA Advanced Lithium-Sulfur Battery (product_3), NASA Portable Solar Charging Array (product_4), NASA Carbon Fiber Composite Panel (product_5)"


@tool("Get production steps for a specific product")
def get_production_steps(product_id: str) -> str:
    """Fetch all production steps for a specific product"""
    try:
        response = requests.get(f"{BASE_URL}/production-step/{product_id}", timeout=10)
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Error fetching production steps for {product_id}: {str(e)}"


@tool("Get estimated time for a specific product")
def get_time_estimate(product_id: str) -> str:
    """Fetch estimated time to manufacture the product"""
    try:
        response = requests.get(f"{BASE_URL}/estimate/time/{product_id}", timeout=10)
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Error fetching time estimate for {product_id}: {str(e)}"


@tool("Get estimated cost for a specific product")
def get_cost_estimate(product_id: str) -> str:
    """Fetch cost estimate for a specific product"""
    try:
        response = requests.get(f"{BASE_URL}/estimate/cost/{product_id}", timeout=10)
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Error fetching cost estimate for {product_id}: {str(e)}"


def get_all_products2() -> str:
    """Fetch all available products from the backend API"""
    try:
        response = requests.get(f"{BASE_URL}/product", timeout=10)
        response.raise_for_status()
        products = response.json()
        return json.dumps(products, indent=2)
    except requests.exceptions.ConnectionError:
        return "Connection failed. Available products: NASA Advanced Lithium-Sulfur Battery (product_3), NASA Portable Solar Charging Array (product_4), NASA Carbon Fiber Composite Panel (product_5)"
    except Exception as e:
        return f"Error: {str(e)}. Available products: NASA Advanced Lithium-Sulfur Battery (product_3), NASA Portable Solar Charging Array (product_4), NASA Carbon Fiber Composite Panel (product_5)"
