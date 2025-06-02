import chainlit as cl
import os
from dotenv import load_dotenv
import litellm
import logging
import re
import json 


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('travel_agency_chatbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

litellm.telemetry = False 
load_dotenv()
API_KEY = os.getenv("OPENROUTERGLOBAL_API_KEY")


MODEL = "openrouter/google/gemini-2.5-flash-preview-05-20"

if not API_KEY:
    raise ValueError("Please set the OPENROUTER_API_KEY environment variable.")
if not MODEL:
    raise ValueError("Please set the MODEL environment variable.")

BASE_URL = "https://openrouter.ai/api/v1"
PROVIDER = "openrouter"

litellm.register_model({
    MODEL: {
        "api_base": BASE_URL,
        "api_key": API_KEY,
        "provider": PROVIDER
    }
})


travel_agency_kb = {
    "booking policy": "Bookings can be made online via our website or by calling our support team. A confirmation email with your itinerary will be sent within 24 hours.",
    "cancellation policy": "Cancellations made 14 days prior to departure are eligible for a full refund. Partial refunds may apply for cancellations within 7-13 days. Check our 'Cancellations' page for details.",
    "refund status": "Refunds are processed within 5-10 business days after cancellation approval. You'll receive an email confirmation once processed.",
    "payment methods": "We accept all major credit/debit cards (Visa, MasterCard), bank transfers, and secure online payment gateways. Some packages offer installment plans.",
    "booking status": "Track your booking status using the booking reference number sent in your confirmation email. Contact us if you can't find it.",
    "travel package availability": "Our website displays real-time availability for tours and packages. Sign up for alerts on the package page if your preferred date is unavailable.",
    "account login issue": "If you can't log into your account, use the 'Forgot Password' link to reset your password. Contact support if the issue persists.",
    "discounts and promotions": "Subscribe to our newsletter or follow our social media for exclusive deals on travel packages and seasonal promotions!",
    "customer support": "For specific booking issues, travel queries, or other concerns, email us at **support@travelagency.com** or call **0300-0000000** (Mon-Fri, 9 AM - 5 PM PKT).",
    "travel insurance": "Travel insurance is recommended and can be purchased during booking. Coverage details are available on our website's 'Insurance' section."
}


def search_travel_agency_kb(query: str) -> str:
    """
    Searches the travel agency's knowledge base for information about bookings,
    cancellations, payments, travel packages, or customer support.
    """
    logger.info(f"Searching travel agency KB for: '{query}'")
    query_lower = query.lower()
    found_answers = []

    for key, value in travel_agency_kb.items():
        if key in query_lower or any(word in query_lower for word in key.split()):
            found_answers.append(value)
    
    if found_answers:
        return "\n\n".join(found_answers) + "\n\nIs there anything else I can assist you with for your travel plans?"
    else:
        return "I couldn't find information about that. For specific booking details or further assistance, please contact our support team:\n\n* **Email:** `support@travelagency.com`\n* **Phone:** `0300-0000000`"


class TravelAgencyChatbotAgent:
    def __init__(self, name: str, instructions: str, model: str, tools_list: list):
        self.name = name
        self.instructions = instructions
        self.model = model
        self._callable_tools = {
            "search_travel_agency_kb": search_travel_agency_kb
        }
        self.litellm_tools_config = tools_list
        logger.info(f"Agent '{self.name}' initialized with {len(self._callable_tools)} tools.")

    async def generate_response(self, messages: list[dict]) -> str:
        try:
            response = await litellm.acompletion(
                model=self.model,
                messages=messages,
                api_key=API_KEY,
                api_base=BASE_URL,
                tools=self.litellm_tools_config,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=300 
            )

            message_response = response.choices[0].message
            content = message_response.content

            if hasattr(message_response, "tool_calls") and message_response.tool_calls:
                tool_call = message_response.tool_calls[0]
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                if func_name in self._callable_tools:
                    tool_output = self._callable_tools[func_name](**args)
                    
                    messages.append(message_response)
                    messages.append({
                        "role": "tool",
                        "name": func_name,
                        "content": tool_output
                    })
                    
                    follow_up_response = await litellm.acompletion(
                        model=self.model,
                        messages=messages,
                        api_key=API_KEY,
                        api_base=BASE_URL,
                        tools=self.litellm_tools_config,
                        tool_choice="auto",
                        temperature=0.7,
                        max_tokens=300
                    )
                    content = follow_up_response.choices[0].message.content
                else:
                    content = "Sorry, I couldn't process that. Can you please rephrase?"
            
            return content if content else "Hmm, I'm not sure how to answer that. Can you try asking in another way?"

        except litellm.exceptions.BadRequestError as e:
            logger.error(f"LiteLLM BadRequestError: {e.response.text}", exc_info=True)
            return f"I'm experiencing a temporary issue. Please try again shortly."
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)
            return f"Oops! Something unexpected happened. Please try again or contact our support team."


search_kb_tool_schema = {
    "type": "function",
    "function": {
        "name": "search_travel_agency_kb",
        "description": "Finds information about travel-related topics like bookings, cancellations, refunds, payment methods, booking status, travel package availability, discounts, or how to contact customer support.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The customer's question about travel bookings, packages, or policies (e.g., 'how to cancel my trip', 'what are the payment options', 'is this tour available')."}
            },
            "required": ["query"]
        }
    }
}

travel_agency_chatbot_agent = TravelAgencyChatbotAgent(
    name="TravelAgencyChatbot",
    instructions=f"""You are a helpful, concise, and friendly AI chatbot for a travel agency. Your main goal is to answer common customer queries about travel bookings, packages, policies, and assist with general travel questions.

    **Key Guidelines:**
    1.  **Greeting:** Start with a warm, travel-inspired greeting.
    2.  **Concise Answers:** Provide direct, brief answers.
    3.  **Tool Usage:** Use `search_travel_agency_kb` to find information for customer questions.
    4.  **Direct to Support:** If you can't find a direct answer, or if the query requires specific booking details, politely direct the customer to email `support@travelagency.com` or call `0300-0000000`.
    5.  **No Direct Actions:** You cannot process bookings, cancel trips, or access customer accounts. Guide users to relevant policies or human support.
    6.  **Tone:** Professional, approachable, and enthusiastic about travel.
    """,
    model=MODEL,
    tools_list=[search_kb_tool_schema]
)

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("messages", [
        {"role": "system", "content": travel_agency_chatbot_agent.instructions},
        {"role": "assistant", "content": "Hello, traveler! Welcome to our travel agency. How can I help you plan your next adventure today?"}
    ])
    await cl.Message(content="""
**Hello! Welcome to Our Travel Agency.** ✈️

I'm your AI assistant, here to help with questions about:
* **Travel Bookings & Itineraries**
* **Cancellations & Refunds**
* **Payment Methods**
* **Booking Status**
* **Travel Package Availability**
* **Discounts & Promotions**
* **Customer Support**
* **Travel Insurance**

What can I assist you with for your journey today?
"""
    ).send()

@cl.on_message
async def main(message: cl.Message):
    messages = cl.user_session.get("messages")
    messages.append({"role": "user", "content": message.content})
    
    try:
        logger.info(f"Processing message: '{message.content}'")
        
        agent_response_content = await travel_agency_chatbot_agent.generate_response(messages)
        
        messages.append({"role": "assistant", "content": agent_response_content})
        
        await cl.Message(content=agent_response_content).send()

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        error_message = f"""**Oops! Something went wrong.**
Please try asking again. If the issue persists, reach our support team directly:
* **Email:** `support@travelagency.com`
* **Phone:** `0300-0000000`
"""
        await cl.Message(content=error_message).send()