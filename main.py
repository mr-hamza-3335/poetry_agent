from agents import Agent, Runner, trace
from dotenv import load_dotenv
import asyncio
from connect import config

load_dotenv()

urdu_poetry_agent= Agent(
    name="urdu_poetry_agent",
    instructions="""
You are an Urdu poetry agent. Your task is to answer poetry-related queries in beautiful Urdu.
Reply only if the question is related to Urdu poetry (ghazals, shayari, etc.).
""",
)

english_poetry_agent=Agent(
    name="english_poetry_agent",
    instructions="""
You are an English poetry agent. Your task is to provide English poems, quotes, or literary poetic responses.
Handle queries related to classic or modern English poetry.
""",
)

motivational_poetry_agent=Agent(
    name="motivational_poetry_agent",
    instructions="""
You are a motivational poetry agent. Respond with inspiring poetic lines or short verses that uplift or motivate.
Only respond if the user asks for motivational or inspiring poetry.
""",
)

parent_poetry_agent= Agent(
    name="parent_poetry_agent",
    instructions="""
You are a parent poetry agent. Your job is to route the user's poetry request to the correct sub-agent.

- If the user asks about Urdu poetry or shayari, hand off to the Urdu Poetry Agent.
- If the user asks for English poetry, hand off to the English Poetry Agent.
- If the user is looking for motivation, uplifting lines, or inspiring poems, hand off to the Motivational Poetry Agent.

If the query is not related to poetry, deny the request.
""",
    handoffs=[urdu_poetry_agent, english_poetry_agent, motivational_poetry_agent]
)
async def main():
    with trace("Poetry Agent Session"):
        result =await Runner.run(
            parent_poetry_agent,
            """ give me motivational poetry for business  """,
            run_config=config

        )
        print(result.final_output)
        print("last_agent ===>", result.last_agent.name)

if __name__ == "__main__":
    import sys
    if sys.platform == 'win32':
        import asyncio.proactor_events
        orig_close = asyncio.proactor_events._ProactorBasePipeTransport.__del__

        def silent_del(self):
            try:
                orig_close(self)
            except RuntimeError as e:
                if "Event loop is closed" not in str(e):
                    raise
        asyncio.proactor_events._ProactorBasePipeTransport.__del__ = silent_del

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
    