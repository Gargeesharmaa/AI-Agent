import os
from uuid import uuid4
from dotenv import load_dotenv
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
# Import the modern pre-built agent creator from langgraph instead of langchain
from langgraph.prebuilt import create_react_agent

from models import model
from objects import Answer
from prompts import agent_system_prompt
from tools import (
    calculate_right_refund,
    get_today_date,
    get_user_purchase_history,
    issue_refund_ticket,
)

load_dotenv()
agent = create_react_agent(
    model=model,
    prompt=agent_system_prompt,
    tools=[calculate_right_refund, get_user_purchase_history, issue_refund_ticket, get_today_date],
    checkpointer=InMemorySaver()
)

def run_conversation():
    config = {"configurable": {"thread_id": str(uuid4())}}

    text = "I would like to request a refund"
    print(f"User: {text}")
    current_input = {"messages": [HumanMessage(content=text)]}
    conversation = True

    while conversation:
        response = agent.invoke(current_input, config=config)

        messages = response.get("messages", [])
        if not messages:
            print("No response received.")
            break
            
        last_message = messages[-1]
        ai_text = last_message.content
        print(f"\nAgent: {ai_text}")

        if "done" in ai_text.lower() or "ticket issued" in ai_text.lower():
            conversation = False
        else:
            user_input = input("\nReply: ")
            if user_input.strip().lower() in ['exit', 'quit', 'bye']:
                conversation = False
            else:
                # Append the new user turn to the incremental graph execution step
                current_input = {"messages": [HumanMessage(content=user_input)]}

    print("\nThe job is done!")

if __name__ == "__main__":
    run_conversation()
