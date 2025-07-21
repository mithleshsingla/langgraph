from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import os
from dotenv import load_dotenv
load_dotenv()
import asyncio
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
from langchain_groq import ChatGroq

async def main():
    client=MultiServerMCPClient(
        {
            "Math":{
                "command":"python",
                "args":["mathserver.py"],
                "transport":"stdio",
            },
            "weather":{
                "url":"http://localhost:8000/mcp",
                "transport":"streamable-http",
            }
        }
    )

    tools=await client.get_tools()    
    model = ChatGroq( model_name="llama3-8b-8192")
    agent=create_react_agent(model,tools)
    ma_re=await agent.invoke({"messages":[{"role":"user","content":"(2+3)*22"}]})

    print("math_res",ma_re['messages'][-1].content)

asyncio.run(main())    

