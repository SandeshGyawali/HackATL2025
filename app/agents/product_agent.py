from crewai import Agent
from app.tools.product_tools import (
    get_all_products,
    get_production_steps,
    get_time_estimate,
    get_cost_estimate
)

class ProductAgent:
    def create_agent(self):
        return Agent(
            role="Product Information Specialist",
            goal="Identify products and provide accurate information about manufacturing data",
            backstory="You are an expert in NASA product manufacturing with deep knowledge of production processes, costs, and timelines.",
            tools=[
                get_all_products,
                get_production_steps,
                get_time_estimate,
                get_cost_estimate
            ],
            verbose=True
        )