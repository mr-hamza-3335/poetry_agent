from dotenv import load_dotenv
import os
from agents import AsyncOpenAI, RunConfig, OpenAIChatCompletionsModel

load_dotenv()
gemini_api_key= os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("API KEY is not set")

external_client= AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)
config= RunConfig(
    model=model,
    model_provider=external_client
)