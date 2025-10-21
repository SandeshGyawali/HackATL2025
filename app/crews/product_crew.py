from crewai import Crew, Task
from app.agents.product_identifier_agent import ProductIdentifierAgent
from app.agents.query_analyzer_agent import QueryAnalyzerAgent


class ProductCrew:
    def __init__(self):
        self.identifier_agent = ProductIdentifierAgent().create_agent()
        self.analyzer_agent = QueryAnalyzerAgent().create_agent()

    def analyze_query(self, user_query: str):
        # Task 1: Identify the product
        identify_task = Task(
            description=f"""
            Analyze this user query: "{user_query}"
            
            Your job:
            1. Get all available products using the get_all_products tool
            2. Identify which specific product the user is asking about
            3. If no specific product is mentioned, list all available products
            4. Extract the product ID and name for the next agent
            
            Output the identified product information clearly.
            """,
            agent=self.identifier_agent,
            expected_output="Product identification with product ID and name, or list of all products if none specified",
        )

        # Task 2: Analyze intent and provide detailed response
        analyze_task = Task(
            description=f"""
            Based on the product information from the previous task and the user query: "{user_query}"
            
            Your job:
            1. Determine what specific information the user wants:
               - Production steps/breakdown
               - Time estimation
               - Cost estimation
               - General product information
            2. Use the appropriate tools to fetch the requested data
            3. Provide a comprehensive, helpful response
            
            If the user asks about multiple aspects, provide all relevant information.
            """,
            agent=self.analyzer_agent,
            expected_output="A detailed, helpful response answering the user's specific question about the NASA product",
        )

        crew = Crew(
            agents=[self.identifier_agent, self.analyzer_agent],
            tasks=[identify_task, analyze_task],
            verbose=True,
        )

        try:
            result = crew.kickoff()
            return result
        except Exception as e:
            return f"I'm having trouble processing your request. We have NASA Advanced Lithium-Sulfur Battery, NASA Portable Solar Charging Array, and NASA Carbon Fiber Composite Panel available. Error: {str(e)}"
