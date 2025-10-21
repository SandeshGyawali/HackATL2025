import os

from app.tools.simple_tools import GetAllProductsTool
from crewai import Agent, Task, Crew

# Test the tool directly
print("=== Direct tool test ===")
tool = GetAllProductsTool()
result = tool._run()
print(f"Direct result: {result}")

# Test with CrewAI agent
print("\n=== CrewAI agent test ===")
agent = Agent(
    role="Tester",
    goal="Test the get_all_products tool",
    backstory="You are testing tools",
    tools=[GetAllProductsTool()],
    verbose=True,
)

task = Task(
    description="Use the get_all_products tool to fetch products",
    agent=agent,
    expected_output="List of products",
)

crew = Crew(agents=[agent], tasks=[task], verbose=True)
crew_result = crew.kickoff()
print(f"Crew result: {crew_result}")
