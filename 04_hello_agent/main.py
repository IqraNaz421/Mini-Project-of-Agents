# from agents import Agent, OpenAIChatCompletionsModel,AsyncOpenAI, Runner, set_tracing_disabled
# from dotenv import load_dotenv
# import os
# import chainlit as cl

# load_dotenv()

# OPENROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
# BASE_URL = "https://openrouter.ai/api/v1"
# MODEL = "deepseek/deepseek-chat-v3-0324:free"

# client = AsyncOpenAI(
#     api_key=OPENROUTER_API_KEY,
#     base_url=BASE_URL
# )

# set_tracing_disabled(disabled=True)


# # This agent will use the custom LLM provider
# agent = Agent(
#     name="Assistant",
#     instructions="You are a helpful assistant to answer any question.",
#     model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
# )

# @cl.on_chat_start
# async def start():
#     cl.user_session.set("history", [])
#     await cl.Message(content="Hello! How can I help you today?").send()

   
# @cl.on_message
# async def handle_message(message:cl.Message):
#     history = cl.user_session.get("history")
#     history.append({"role": "user", "content": message.content})
#     result = await Runner.run(
#         starting_agent=agent,
#         input=history
#     )
#     history.append({"role": "assistant", "content": result.final_output})
#     cl.user_session.set("history", history)
#     await cl.Message(content=result.final_output).send()















# import os
# import chainlit as cl
# import httpx
# from dotenv import load_dotenv

# # Load API key from .env file
# load_dotenv()
# API_KEY = os.getenv("OPENROUTER_API_KEY")
# print("Loaded API Key:", API_KEY)  # Check if key is None

# @cl.on_message
# async def main(message: cl.Message):
#     # Extract user message text
#     user_text = message.content

#     # Prepare headers and payload
#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json",
#     }

#     data = {
#         "model": "openai/gpt-3.5-turbo",  # You can change model if needed
#         "messages": [
#             {"role": "user", "content": user_text}
#         ],
#     }

#     # Send request to OpenRouter
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             "https://openrouter.ai/api/v1/chat/completions",
#             headers=headers,
#             json=data
#         )

#     # Handle response
#     if response.status_code == 200:
#         reply = response.json()["choices"][0]["message"]["content"]
#     else:
#         reply = f"❌ API Error! Status code: {response.status_code}"

#     # Send reply to user
#     await cl.Message(content=reply).send()









import os
import chainlit as cl
import httpx
from dotenv import load_dotenv

load_dotenv()  # Loads .env file from current directory

API_KEY = os.getenv("OPENROUTER_API_KEY")
print(f"Loaded API Key: {API_KEY}")  # Debug output

@cl.on_message
async def main(message: cl.Message):
    user_text = message.content

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_text}],
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
        )

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
    else:
        reply = f"❌ API Error! Status code: {response.status_code}"

    await cl.Message(content=reply).send()
