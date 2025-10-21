from crewai import Agent
from app.tools.simple_tools import GetAllProductsTool

class ProductIdentifierAgent:
    def create_agent(self):
        return Agent(
            role="Product Identifier",
            goal="Identify which NASA product the user is asking about and gather all relevant product data",
            backstory="You are a specialist in identifying NASA products from user queries and collecting comprehensive product information.",
            tools=[GetAllProductsTool()],
            verbose=True
        )