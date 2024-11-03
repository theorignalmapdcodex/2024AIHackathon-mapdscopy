# Import relevant functionality
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from langchain_openai import ChatOpenAI
import os

# Create the agent
memory = MemorySaver()

from typing import Annotated, List
from langchain_core.tools import tool

from app import main as get_response


def current_datetime() -> str:
    """Get the current datetime in the format of 'YYYY-MM-DD HH:MM:SS. Use it when you want to know the current time.'"""
    from datetime import datetime

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def memeory_recall(
    query: Annotated[str, "the content user want to recall"],
    start_datetime: Annotated[
        str,
        "the start datetime of the time range, in the format of 'YYYY-MM-DD HH:MM:SS'",
    ],
    end_datetime: Annotated[
        str,
        "the end datetime of the time range, in the format of 'YYYY-MM-DD HH:MM:SS'",
    ],
) -> int:
    """Get response by query from memory (what the user seen in the past) of a user. Most time user want to get some information that can not be found in the internet. The accuracy of the result depends on the accuracy of the time range."""
    print("start_datetime", start_datetime)
    print("end_datetime", end_datetime)
    result = get_response(query)
    return result[0]


@tool
def create_calendar_event() -> int:
    """Create a calendar event based on the poster, this tool will use the smart glasses image to do the calendar event creation."""

    return "The calendar event has been created successfully."


@tool
def search_person_info(
    query: Annotated[str, "the content user want to query"],
) -> int:
    """search personal information for people the user is currently talking about, this tool will use the smart glasses image to do the search."""

    return "This is a person named Jon. He is a software engineer at Google."


model = ChatOpenAI(model="gpt-4")
search = TavilySearchResults(max_results=2)
tools = [search, memeory_recall, create_calendar_event, search_person_info]
agent_executor = create_react_agent(
    model,
    tools,
    checkpointer=memory,
    state_modifier=f"Current datetime is '{current_datetime()}'",
)

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
# for chunk in agent_executor.stream(
#     {"messages": [HumanMessage(content="hi im bob! and i live in sf")]}, config
# ):
#     print(chunk)
# print("----")

# for chunk in agent_executor.stream(
#     {"messages": [HumanMessage(content="whats the weather where I live?")]}, config
# ):
#     print(chunk)
# print("----")

for chunk in agent_executor.stream(
    {
        "messages": [
            HumanMessage(
                content="How many participats in the last year? I think last night there is a intro video for it."
            )
        ]
    },
    config,
):
    print(chunk)
    print("----")
print("========================================")
for chunk in agent_executor.stream(
    {
        "messages": [
            HumanMessage(
                content="This activity is so great, add this poster event to my calendar."
            )
        ]
    },
    config,
):
    print(chunk)
    print("----")
print("========================================")
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="I don't remember his name, please tell me.")]},
    config,
):
    print(chunk)
    print("----")
