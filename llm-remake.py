import ollama
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv
from tool_info import tool_list
import subprocess
from tools import *

load_dotenv()
MODEL_NAME = "llama-3.1-8b-instant"
client = Groq(api_key=os.environ["GROQ_API_KEY"])
class Moderation(BaseModel):
    isExplicit: int
    explicitWord: str

class Validation(BaseModel):
    isValid: int

# Will do later
def moderation(text: str) -> int:
    prompt = f"""
User query: {text}
------
Output Format:
There are two variables in the provided format
- isExplicit: 0 or 1 (0 means that the text is **NOT** explicit)
- explicitWord: The word that is explicit in the text. Leave empty if there is no explicit content
"""
    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "system",
                "content": "You are a text moderation system for explicit texts."
            },
            {
                "role": "user",
                "content:": prompt
            }
        ],
        # format=Moderation.model_json_schema(),
    )
    # response = json.loads(response["message"].content)

    print(response)

# --------------------------
def generate_cot(user_query: str) -> str:
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": """You are a Chain of Thought (COT) generator for user queries.
Available Tools:
- **open_app**: Opens the specified application by name.
- **close_app**: Closes the specified application by name.
- **open_url**: Opens the specified URL in the default web browser.
- **create_directory**: Creates a new directory with the specified name.
- **delete_directory**: Deletes the specified directory if it exists.
- **open_directory**: Opens the specified directory path in the file explorer.
- **open_file**: Opens the specified file with its default associated application.
- **create_file**: Creates a new empty file with the specified name.
- **delete_file**: Deletes the specified file if it exists.
- **save_file**: Saves the current file in use, typically for an application or editor. Simulates Ctrl+S keys.
- **move_mouse_to_coordinates**: Moves the mouse cursor to the specified screen coordinates.
- **two_key_shortcuts**: Simulates pressing two keys simultaneously.
- **web_scrape**: Takes the search query and returns the top 3 URLs from the web.

**Do NOT use any other tools**

*Rules for paths*
- Always use full absolute paths
- Use single forward slash only
- Drives available: E:/, D:/, C:/

Some things you should know:
- I have spotify app to listen to music
- Do not assume ANYTHING
- To open youtube, use 'open_url' not `open_app`
- I use windows

**IF ANY OF THE USER INTENT CANNOT BE SATISFIED WITH THE AVAILABLE TOOLS, RESPONSE WITH 'Query cannot be fulfilled'**"""
            },
            {
                "role": "user",
                "content": user_query
            }
        ],
    )

    return response.choices[0].message.content

def validate_cot(cot: str, user_query: str, required_tool_info: list) -> bool:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a Chain of Thought (COT) validator for user queries."""
            },
            {
                "role": "user",
                "content": f"""
Chain of Though:
{cot}

User Query: {user_query}

Info about the tools used:
{required_tool_info}
---
Response with `0` without further reasoning if even one of the following conditions is not true:
- **Is the chain of thoughts using tools that are not present in available tools?**
- Is the chain of thoughts enough to satisfy the user's intent?
- Is the chain of thoughts calling any unwanted APIs?
---

Output Format:
0: If the chain of thought is **NOT** valid.
1: If the chain of thought is valid.

---
Respond with zero if:
- The chain of thoughts is using tools that are not present in: tool_names = ["open_app", "close_app", "open_url", "create_directory", "delete_directory", "open_directory", "open_file", "create_file", "delete_file", "save_file", "move_mouse_to_coordinates", "two_key_shortcuts", "web_scrape"]
- You think any of the API calls is unreasonable and there are unnecessary API calls that do not satisfy the user's intent.
---
Some things you should know:
- I have spotify app to listen to music
- Do not assume ANYTHING
- To open youtube, use 'open_url' not `open_app`
- I use windows
"""
            }
        ],
        temperature=0,
        max_completion_tokens=1
    )

    return response.choices[0].message.content

def rewrite_tools(cot: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": """You will be given a chain of thought, you have to rewrite just the names of the APIs separated by newlines used in that chain of thought, Nothing else. 
                **IMPORTANT: Do not use any symbols such as *,', ", ; ,: etc.
                Also, do not use your own knowledge to change the names of the tools or anything like that, strictly follow the chain of thought"""
            },
            {
                "role": "user",
                "content": f"chain of thought: {cot}"
            }
        ]
    )

    print("Rewriting tools")
    print(response.choices[0].message.content)
    return response.choices[0].message.content
# --------------------------

# Later
def create_execution_plan(cot: str, tools_retrieved: list, user_query: str):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": """You are an Execution Plan generator for Chain of Thoughts (COT).
                **Do not write anything before or after the execution plan. It should be such that I can directly call the functions one by one on the terminal without changing anything"""
            },
            {
                "role": "user",
                "content": f"""
Here is the chain of thought:
{cot}

Tools to be used along with their parameters:
{tools_retrieved}

User Query: {user_query}

Output Format:
The tool name along with their parameters ONLY.
<tool_name>(<parameter1> = <parameter1_value>, <parameter2> = <parameter2_value>, ...)
Do NOT write anything else.
The tool calls should be such that they can be directly executed in a script.
"""
            }
        ],
    )

    return response.choices[0].message.content

def run_command(command):
    try:
        choice = input(f"Do you want to run the command `{command}` (y/n): ")
        if (choice.lower() == 'y'):
            result = eval(command)
            print(result)
        else:
            print("Process terminated")
    except Exception as e:
        print(f"There was an error in running the command `{command}`: {e}")

if __name__ == "__main__":
    query = "Could you open E drive and then create a folder named test there."
    chain_of_thought = generate_cot(query)
    print("Generated COT")
    print(chain_of_thought)
    print("-----------------------")
    
    tools_retrieved = rewrite_tools(chain_of_thought)
    print("Rewrote tools")
    print("-----------------------")

    required_tools = tools_retrieved.split("\n")
    print(f"Required tools: {required_tools}")
    required_tool_info = []

    for i in range(len(required_tools)):
        try:
            required_tool_info.append(tool_list[required_tools[i]])
        except Exception as e:
            print(f"Error while retrieving `{required_tools[i]}`: {e}")
    print(required_tool_info)

    is_valid = validate_cot(chain_of_thought, query, required_tool_info)
    print(f"isValid?: {is_valid}")
    print("-----------------------")

    exec_plan = create_execution_plan(chain_of_thought, required_tool_info, query)
    print("-----------------------")
    print("Execution Plan")
    print(exec_plan)

    tool_calls = exec_plan.split("\n")
    print(tool_calls)
    # run_on_terminal("dir")

    for i in tool_calls:
        run_command(i)