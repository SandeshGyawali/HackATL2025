from app.tools.simple_tools import GetAllProductsTool

tool = GetAllProductsTool()
result = tool._run()
print("Tool result:")
print(result)