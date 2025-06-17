from asyncio import Event

from IPython.core.application import base_flags
from google import genai
from google.adk.agents import LlmAgent,SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from pathlib import Path
from typing import List, Generator

import json

from google.adk.tools.agent_tool import AgentTool
from google.cloud.aiplatform_v1beta1.types import session_service
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import zip_extractor,loadinggit

client = genai.Client(api_key="")
model_id = "models/gemini-2.5-flash-preview-04-17"





"""def traverse_directory(path: Path, level=0, base_path=None, skip_files=List[str]):

    if base_path is None:
        base_path = path

    indent = "    " * level
    prefix = "|--" if level > 0 else ""

    for item in sorted(path.iterdir()):
        if item.name.startswith('.'):
            continue  # Skip hidden files/folders

        relative_path = item.relative_to(base_path)

        with open('structure.txt', 'a') as f:
            f.write(f"{indent}{prefix} {relative_path}\n")
            f.close()


        if item.is_file()  and item.name not in skip_files:
            with open(item.absolute(), 'r') as file_in, open('content.txt', 'a') as file_out:
                data = file_in.read()
                file_out.write(f"\n \n Content of file {relative_path}:\n \n \n \n  {data} \n \n Content ends of file {relative_path} {'-'*40}\n")
                file_out.close()
                file_in.read()


        if item.is_dir():
            traverse_directory(item, level + 1, base_path)

# Set your root path here
root = Path("/home/ubuntu/PycharmProjects/PythonProject/A2A")
traverse_directory(root,skip_files=['structure.txt', 'content.txt',"uv.lock","directory_transverser.py","uv.lock","pyproject.toml","Agent.py"])"""




#base_agent = LlmAgent(
#    model=model_id,
#    name="DocumentationGenerator",
#    description="Generates documentation for a code base based on its file structure and content.",
#    instruction=f"You are a smart assistant for help user in writing documentation for the code base. User will provide the code base file structure and the content of each file. "
#                f"Carefully check the dependency between files and provide a proper documentation so it will be easy to understand for new users in future.",
#    tools = [zip_extractor.zip_extractor,loadinggit.download_github_repo_as_zip],
#)
#
#




documentor_agent = LlmAgent(
    model=model_id,
    name="DocumentationGenerator",
    description="Generates documentation for a code base based on its file structure and content.",
    instruction=f"You are a smart assistant for help user in writing documentation for the code base. User will provide the code base file structure and the content of each file. "
                f"Carefully check the dependency between files and provide a proper documentation so it will be easy to understand for new users in future.",
)



root_agent = LlmAgent(
    name= "DocumentationGeneratorAgent",
    description="An agent that generates documentation for a code base based on its file structure and content.",
    tools=[AgentTool(agent=documentor_agent)],
    #sub_agents=[base_agent,documentor_agent]
)



session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name="DocumentationGeneratorApp",
    session_service=session_service
)


USER_ID = "user_activities"
SESSION_ID = "session_activities"


async def execute(request):

    await session_service.create_session(
        app_name="document_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    prompt = (
        f"User is flying to {request['destination']} from {request['start_date']} to {request['end_date']}, "
        f"with a budget of {request['budget']}. Suggest 2-3 activities, each with name, description, price estimate, and duration. "
        f"Respond in JSON format using the key 'activities' with a list of activity objects."
    )

    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    async for event in runner.run_async(user_id= USER_ID,session_id=SESSION_ID,new_message = message):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            try:
                parsed = json.loads(response_text)
                if "activities" in parsed and isinstance(parsed["activities"], list):
                    return {"activities": parsed["activities"]}
                else:
                    print("'activities' key missing or not a list in response JSON")
                    return {"activities": response_text}  # fallback to raw text
            except json.JSONDecodeError as e:
                print("JSON parsing failed:", e)
                print("Response content:", response_text)
                return {"activities": response_text}  # fallback to raw text




