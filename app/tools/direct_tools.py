from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import urllib.request
import json

class ProductInput(BaseModel):
    pass

class ProductIdInput(BaseModel):
    product_id: str = Field(..., description="The product ID to query")

class DirectGetAllProductsTool(BaseTool):
    name: str = "get_all_products"
    description: str = "Get all available NASA products"
    args_schema: Type[BaseModel] = ProductInput

    def _run(self) -> str:
        try:
            with urllib.request.urlopen("http://127.0.0.1:8000/product", timeout=5) as response:
                data = json.loads(response.read().decode())
                return json.dumps(data, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"

class DirectGetTimeEstimateTool(BaseTool):
    name: str = "get_time_estimate"
    description: str = "Get time estimate for a specific product"
    args_schema: Type[BaseModel] = ProductIdInput

    def _run(self, product_id: str) -> str:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:8000/estimate/time/{product_id}", timeout=5) as response:
                data = json.loads(response.read().decode())
                return json.dumps(data, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"