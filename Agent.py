from IPython.core.application import base_flags
from google import genai
from google.adk.agents import LlmAgent,ParallelAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from pathlib import Path
from typing import List

client = genai.Client(api_key="")
model_id = "models/gemini-2.5-flash-preview-04-17"





def traverse_directory(path: Path, level=0, base_path=None, skip_files=List[str]):
    """
    Traverse the directory and print all files and directories in a tree format.
    """
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
traverse_directory(root,skip_files=['structure.txt', 'content.txt',"uv.lock","directory_transverser.py","uv.lock","pyproject.toml","Agent.py"])




base_agent = LlmAgent(
    model=model_id,
    name="DocumentationGenerator",
    description="Generates documentation for a code base based on its file structure and content.",
    instruction=f"You are a smart assistant for help user in writing documentation for the code base. User will provide the code base file structure and the content of each file. "
                f"Carefully check the dependency between files and provide a proper documentation so it will be easy to understand for new users in future.",
    tools = [traverse_directory],
)



def web_search_model() -> str:
    #print(query)
    #model = genai.GenerativeModel('models/gemini-2.5-flash-preview-04-17')

    with open('structure.txt','r') as file:
        structure = file.read()
        file.close()

    with open('content.txt','r') as file:
        content = file.read()
        file.read()
        file.close()

    try:
        response = client.models.generate_content(
            model=model_id,
            contents=[
                {
                    "role" : "model" , "parts": [{"text": f"You are a smart assistant for help user in writing documentation for the code base. User will provide the code base file structure and the content of each file. "
                                                          f"Carefully check the dependency between files and provide a proper documentation so it will be easy to understand for new users in future."
                                                          }]
                },
                {
                     "role" : "user" , "parts": [{"text": f"Here is the file structure of the code base:\n{structure}\n \nAnd here is the content of each file:\n{content}\n\nNow, please provide a detailed documentation for the code base."}]
                }
            ]
        )
        return response.text
    except Exception as e:
        raise Exception(f'Web search not working')



data = web_search_model()
print(data)
