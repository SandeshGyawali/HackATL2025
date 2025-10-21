from crewai import Agent
from app.tools.direct_tools import DirectGetAllProductsTool, DirectGetTimeEstimateTool

class SimpleAgent:
    def create_agent(self):
        return Agent(
            role="NASA Product Assistant",
            goal="Help users with NASA product information",
            backstory="You are an expert NASA product specialist.",
            tools=[
                DirectGetAllProductsTool(), 
                DirectGetTimeEstimateTool()
            ],
            verbose=True
        )