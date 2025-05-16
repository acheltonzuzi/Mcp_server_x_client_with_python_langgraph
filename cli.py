# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
load_dotenv()
model = ChatOpenAI(model="gpt-4o")
memory = InMemorySaver()
config = {
    "configurable": {
        "thread_id": "1"  
    }
}
server_params = StdioServerParameters(
    command="python",
    # Make sure to update to the full absolute path to your math_server.py file
    args=["server.py"],
)

import asyncio

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)
            prompt="""
            Você é um assistente útil. Teu nome e Ashton e você é um assistente de programação. Você pode me ajudar a programar em Python e a resolver problemas de programação. Você também pode me ajudar a fazer cálculos matemáticos e a resolver problemas matemáticos
            """
            # Create and run the agent
            agent = create_react_agent(model, tools,prompt=prompt,checkpointer=memory)
            while True:
                # Get user input
                user_input = input("User: ")
                if user_input.lower() == "exit":
                    break

                # Send the input to the agent and get the response
                agent_response = await agent.ainvoke({"messages": user_input},config=config)
                messages = agent_response["messages"]
                # Procura a última mensagem da IA que tem conteúdo
                for msg in reversed(messages):
                    if isinstance(msg, BaseMessage) and msg.content:
                        print("Agente:", msg.content)
                        break
            # agent_response = await agent.ainvoke({"messages": "Adicione Achelton a lista de nomes"})
            # messages = agent_response["messages"]
            # # Procura a última mensagem da IA que tem conteúdo
            # for msg in reversed(messages):
            #     if isinstance(msg, BaseMessage) and msg.content:
            #         print("Agente:", msg.content)
            #         break

# Run the main function
asyncio.run(main())
