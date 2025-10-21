from fastapi import APIRouter
from pydantic import BaseModel
from crewai import Crew, Task
from app.agents.simple_agent import SimpleAgent
from app.crews.product_crew import ProductCrew

router = APIRouter()


class ChatMessage(BaseModel):
    message: str


# @router.post("/chat")
# async def chat_with_agent(chat_message: ChatMessage):
#     try:
#         agent = SimpleAgent().create_agent()

#         task = Task(
#             description=f"""
#             User query: "{chat_message.message}"

#             Steps:
#             1. First, get all available products to understand what's available
#             2. Identify which product the user is asking about (if any)
#             3. Determine what information they want (production steps, time, cost, or general info)
#             4. Use the appropriate tools to get the requested information
#             5. Provide a clear, helpful response

#             If no specific product is mentioned, list available products.
#             If they ask about costs, time, or production steps, use the specific tools.
#             """,
#             agent=agent,
#             expected_output="A comprehensive and helpful response about NASA products based on the user's query",
#         )

#         crew = Crew(agents=[agent], tasks=[task], verbose=True)
#         response = crew.kickoff()
#         return {"response": str(response)}
#     except Exception as e:
#         return {"response": f"Error: {str(e)}"}


@router.post("/chat")
def chat_with_agent(chat_message: ChatMessage):
    crew = ProductCrew()
    result = crew.analyze_query(chat_message.message)
    return {"response": str(result)}
