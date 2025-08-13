import ollama
from tool_info import tool_list
import tools
from pydantic import BaseModel
import json
import logging
import re
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.environ["GROQ_API_KEY"])



class validationOutput(BaseModel):
    isValid: int

def generate_chain_of_thought(user_query: str, prev_chain="") -> str:
    prompt_for_cot_generation = f"""
    Available Tools:
    - **open_app**: Opens the specified application by name. Only takes app name, **does NOT need path**, **Only opens a single app at a time**. Paramters: `app_name`
    - **close_app**: Closes the specified application by name. Only takes app name, doesn't need path. Paramters: `app_name`
    - **open_url**: Opens the specified URL in the default web browser. Only takes URL. Paramters: `url`
    - **create_directory**: Creates a new directory with the specified name. Requires absolute path. Paramters: `folder_name`, `folder_creating_path`
    - **delete_directory**: Deletes the specified directory if it exists.Requires absolute path. Paramters: `folder_path`
    - **open_directory**: Opens the specified directory path in the file explorer. Requires Absolute path. Paramters: `folder_path`
    - **open_file**: Opens the specified file with its default associated application. Requires Absolute path. Paramters: `file_path`
    - **create_file**: Creates a new empty file with the specified name. Requires Absolute path. Paramters: `file_path`
    - **delete_file**: Deletes the specified file if it exists. Requires Absolute path. Paramters: `file_path`
    - **save_file**: Saves the current file in use, typically for an application or editor. Simulates Ctrl+S keys. Paramters: None
    - **move_mouse_to_coordinates**: Moves the mouse cursor to the specified screen coordinates.. Prameters: `x`, `y`
    - **two_key_shortcuts**: Simulates pressing two keys simultaneously as a shortcut. Parameters: `key1`, `key2`
    - **web_scrape**: Takes the search query and returns the top 3 URLs from the web. Takes query as input. Parameters: `query`

    Choose the tools which might be required for the following user query: {user_query}

    Some things you should know:
    - I have spotify app to listen to music
    - Do not assume ANYTHING
    - To open youtube, use 'open_url' not `open_app`

    Rules for absolute paths:
    - Drives available: , C:, D:, E:
    - User - `bhavy`
    - only single forward slash should be used
    - If user says D drive or something similar, path must start with D:/

    FORMAT:
    tool_name(parameter=parameter_value, ...)
    Do NOT write anything other than that
    Always number your steps as '1.' and so on.
    One step should call one API only
    ---
    Previously failed chain of thoughts (if any):
    {prev_chain}
    """

    chain_of_thought = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a tool selector"
            },
            {
                "role": "user",
                "content": prompt_for_cot_generation
            }
        ],
    )

    return chain_of_thought.choices[0].message.content

def validate_chain_of_thought(chain_of_thought: str, user_query: str) -> int:
    isValid = ollama.chat(
        model="llama3.2:latest",
        # model="llama3.1:8b",
        messages=[
            {
                "role": "system",
                "content": f"""
                You are a chain of thought validator.

                Try to answer the following questions:
                - **Is the chain of thoughts using tools that are not present in available tools?**
                - Is the chain of thoughts enough to satisfy the user's intent?
                - Is the chain of thoughts calling any unwanted APIs?
                
                Output Format:
                0: Chain of thought is not valid
                1: Chain of thought is valid

                Do NOT write anything other than 0 or 1

                Available Tools:
                {tool_list}
                """
            },
            {
                "role": "user",
                "content": f"""
                User Query: {user_query}
                ------------------------
                Chain of thought:
                {chain_of_thought}
                """
            }
        ],
        format=validationOutput.model_json_schema()
    )

    # print(isValid["message"].content)
    # to_return = json.loads(isValid["message"].content)
    # print(f"{to_return["isValid"]}")

    return (json.loads(isValid["message"].content))["isValid"]

def retrieve_correct_tools(chain_of_thought: str, state: int, total_steps: int, prev_steps: list) -> list:
    response = ollama.chat(
        model="llama3.2:latest",
        # model="llama3.1:8b",
        messages=[
            {
                "role": "tool",
                "content": "You are a tool which calls the necessary API for the current step."
            },
            {
                "role": "user",
                "content": f"Current Step: {state}\nChain of thought:\n{chain_of_thought}\ntaken steps:\n{prev_steps}"
            }
        ],
        tools=tool_list
    )

    tool_calls = response["message"].tool_calls
    return tool_calls

def extract_tools(tool_calls: list):
    calls = [{"name": i['function'].name, "arguments": i["function"].arguments} for i in tool_calls]
    print(calls)
    print("\n\n")

    for i in calls:
        name = i['name']
        args = i['arguments']
        keys = args.keys()
        vals = args.values()
        # print(name, [i for i in keys], [j for j in vals])
        params = [i for i in keys]
        param_values = [j for j in vals]

        print(f"{name}({params[0]} = {param_values[0]})")

    return calls

def validate_tools(user_query: str, tool_calls: list, chain_of_thought: str) -> int:
    isValid = ollama.chat(
        model="llama3.2:latest",
        # model="llama3.1:8b",
        messages=[
            {
                "role": "system",
                "content": """
                You are a tool validator.

                Ask the following questions:
                - Are the tools used available in the list of tools
                - Does the chain of thought need to be changed or is it enough to try retrieving again?

                Output Format:
                0: Tool(s) is/are not valid
                1: Tool(s) is/are valid
                2: Chain of though needs to be regenerated

                Return 1 IF AND ONLY IF, the user's intent is satisfied from start to end using all the tools in the same order as mentioned in Tool Calls
                """
            },
            {
                "role": "user",
                "content": f"""
                User Query: {user_query}
                Tool Calls: {tool_calls}
                Chain of thought:
                {chain_of_thought}
                """
            }
        ],
        format=validationOutput.model_json_schema()
    )

    return (json.loads(isValid["message"].content))["isValid"]

def execute_tools(tool_calls: list):
    pass

if __name__ == "__main__":
    user_query = "Open E drive in file explorer, then create a folder named 'test'. then create a file named 'text.txt'. Then open the file."
    # user_query = "Open brave, then open whatsapp, then close brave"

    print("--------------------------")
    print("Generating chain of thought...")
    print("--------------------------")
    chain_of_thought = generate_chain_of_thought(user_query)
    print("Generated chain of thought")
    print("--------------------------")

    counter: int = 0
    max_retries: int = 3

    if (chain_of_thought.lower() == "query cannot be fulfilled"):
        print("Invalid Query: Cannot proceed further.")


    print("Checking if Chain of Thought is valid...")
    while (counter < max_retries):
        is_cot_valid = validate_chain_of_thought(chain_of_thought, user_query)
        print(f"Valid Status: {is_cot_valid}")

        if (is_cot_valid):
            print("Chain of Thought is valid")
            break
        else:
            chain_of_thought = generate_chain_of_thought(f"User Query: {user_query}", prev_chain=chain_of_thought)

        counter += 1

    print("--------------------------")
    print(f"Counter 1: {counter}")
    print("--------------------------")
    print(f"Chain of thought:\n{chain_of_thought}")
    print("--------------------------")
    
    steps = re.findall(r"^\d+\.", chain_of_thought, re.MULTILINE)
    total_steps: int = len(steps)

    print(f"Total Steps: {total_steps}")

    if (counter == max_retries):
        print("Could not generate a valid Chain of Thought")
    else:
        counter = 0
    
    print("Searching for correct tools...")

    tool_calls = []
    for state in range(1, total_steps+1):
        tool = (retrieve_correct_tools(chain_of_thought, state, total_steps, tool_calls))
        tool_calls.append(tool)

    print("Tools Found")
    print("--------------------------")
    print("Validating tools...")

    while (counter < max_retries):
        are_tools_valid = validate_tools(user_query, tool_calls, chain_of_thought)
        print(f"Are tools valid: {are_tools_valid}")

        if (are_tools_valid):
            print("Tools are valid")
            break
        elif are_tools_valid == 0:
            print("Retrieving new set of tools")
            tool_calls = []
            for state in range(1, total_steps+1):
                tool_calls.append(retrieve_correct_tools(chain_of_thought, state, total_steps, tool_calls))
        else:
            print("Regenerating chain of thought")
            chain_of_thought = generate_chain_of_thought(user_query)
        
        counter += 1

    print("--------------------------")
    print(f"Counter 2: {counter}")
    print(f"tool calls:\n{tool_calls}")
    print("--------------------------")

    if (counter == max_retries):
        print("Could not retrieve appropriate tools and/or their order to satisfy user query.")
    else:
        counter = 0
    
    execute_tools(tool_calls)