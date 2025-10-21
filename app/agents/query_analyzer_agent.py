from crewai import Agent
from app.tools.simple_tools import GetProductionStepsTool, GetTimeEstimateTool, GetCostEstimateTool

class QueryAnalyzerAgent:
    def create_agent(self):
        return Agent(
            role="Query Analyzer and Responder",
            goal="Analyze what specific information the user wants and provide detailed answers using product data",
            backstory="You are an expert at understanding user intent and providing precise, helpful responses about NASA product manufacturing details.",
            tools=[GetProductionStepsTool(), GetTimeEstimateTool(), GetCostEstimateTool()],
            verbose=True
        )