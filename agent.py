from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import END, START
from langgraph.graph.state import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from IPython.display import Image,display
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["LANGSMITH_PROJECT"]="TestProject"
import os
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGSMITH_TRACING"]="true"

from langchain_tavily import TavilySearch
tavily=TavilySearch()

class State(TypedDict):
    messages: Annotated[list,add_messages]

# Make sure to run cell 0 before running this cell, as it imports ChatGroq and other dependencies.
def make_graph():
    def multiply(a:int,b:int)->int:
        """multiply a and b
        Args:
            a(int): 1st integer
            
            b(int): 2nd integer
        return:
            
            int: output_int    """
        return a*b
    llm = ChatGroq(model_name="llama3-8b-8192")
        
    tools=[tavily,multiply]
    llmwt=llm.bind_tools(tools)
    from langgraph.prebuilt import ToolNode
    from langgraph.prebuilt import tools_condition
    def tool_calling_llm(state:State):
        return {"messages":[llmwt.invoke(state["messages"])]}
    builder=StateGraph(State)
    builder.add_node("tool_calling_llm",tool_calling_llm)
    builder.add_node("tools",ToolNode(tools))



    builder.add_edge(START,"tool_calling_llm")
    builder.add_conditional_edges("tool_calling_llm",tools_condition)
    builder.add_edge("tools","tool_calling_llm")
    graph_builder=builder.compile()
    return graph_builder

tool_agent=make_graph()
