from asyncio import Event

from IPython.core.application import base_flags
from google import genai
from google.adk.agents import LlmAgent,SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from pathlib import Path
from typing import List, Generator

from google.cloud.aiplatform_v1beta1.types import session_service

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




base_agent = LlmAgent(
    model=model_id,
    name="DocumentationGenerator",
    description="Generates documentation for a code base based on its file structure and content.",
    instruction=f"You are a smart assistant for help user in writing documentation for the code base. User will provide the code base file structure and the content of each file. "
                f"Carefully check the dependency between files and provide a proper documentation so it will be easy to understand for new users in future.",
    tools = [zip_extractor.zip_extractor,loadinggit.download_github_repo_as_zip],
)






documentor_agent = LlmAgent(
    model=model_id,
    name="DocumentationGenerator",
    description="Generates documentation for a code base based on its file structure and content.",
    instruction=f"You are a smart assistant for help user in writing documentation for the code base. User will provide the code base file structure and the content of each file. "
                f"Carefully check the dependency between files and provide a proper documentation so it will be easy to understand for new users in future.",
)



final_agent = SequentialAgent(
    name= "DocumentationGeneratorAgent",
    description="An agent that generates documentation for a code base based on its file structure and content.",
    sub_agents=[base_agent,documentor_agent]
)


root_agent = final_agent



# Simplified view of Runner's main loop logic
def run(new_query) -> Generator[Event]:
    # 1. Append new_query to session event history (via SessionService)
    session_service.append_event(session, Event(author='user', content=new_query))

    # 2. Kick off event loop by calling the agent
    agent_event_generator = root_agent.run_async(context)

    async for event in agent_event_generator:
        # 3. Process the generated event and commit changes
        session_service.append_event(session, event) # Commits state/artifact deltas etc.
        # memory_service.update_memory(...) # If applicable
        # artifact_service might have already been called via context during agent run

        # 4. Yield event for upstream processing (e.g., UI rendering)
        yield event
        # Runner implicitly signals agent generator can continue after yielding

