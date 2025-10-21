from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import json


class ProductInput(BaseModel):
    """Input for product tools"""

    pass


class ProductIdInput(BaseModel):
    """Input for product ID tools"""

    product_id: str = Field(..., description="The product ID to query")


class GetAllProductsTool(BaseTool):
    name: str = "get_all_products"
    description: str = "Get all available NASA products"
    args_schema: Type[BaseModel] = ProductInput

    def _run(self) -> str:
        try:
            response = requests.get("http://127.0.0.1:8000/product", timeout=30)
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
        except Exception as e:
            return f"Error fetching products: {str(e)}"


class GetProductionStepsTool(BaseTool):
    name: str = "get_production_steps"
    description: str = "Get production steps for a specific product"
    args_schema: Type[BaseModel] = ProductIdInput

    def _run(self, product_id: str) -> str:
        try:
            response = requests.get(f"http://127.0.0.1:8000/production-step/{product_id}", timeout=30)
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
        except Exception as e:
            return f"Error fetching production steps for {product_id}: {str(e)}"


class GetTimeEstimateTool(BaseTool):
    name: str = "get_time_estimate"
    description: str = "Get time estimate for manufacturing a specific product"
    args_schema: Type[BaseModel] = ProductIdInput

    def _run(self, product_id: str) -> str:
        try:
            response = requests.get(f"http://127.0.0.1:8000/estimate/time/{product_id}", timeout=30)
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
        except Exception as e:
            return f"Error fetching time estimate for {product_id}: {str(e)}"


class GetCostEstimateTool(BaseTool):
    name: str = "get_cost_estimate"
    description: str = "Get cost estimate for manufacturing a specific product"
    args_schema: Type[BaseModel] = ProductIdInput

    def _run(self, product_id: str) -> str:
        try:
            response = requests.get(f"http://127.0.0.1:8000/estimate/cost/{product_id}", timeout=30)
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
        except Exception as e:
            return f"Error fetching cost estimate for {product_id}: {str(e)}"
