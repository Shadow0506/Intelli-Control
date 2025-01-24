import ollama
from tool_info import tool_list
import tools
from pydantic import BaseModel
import json
import logging
import re

class validationOutput(BaseModel):
    isValid: int

def generate_chain_of_thought(user_query: str) -> str:
    chain_of_thought = ollama.chat(
        model="llama3.2:latest",
        messages=[
            {
                "role": "system",
                "content": "You are a chain of thought generator. Do not write anything other than the chain of thoughts. Do proper numbering of the steps. **Each step should use EXACTLY 1 tool**. Always Re-think if the chain of thought is sufficient to satisfy user intent."
            },
            {
                "role": "user",
                "content": f"User Query: {user_query}\ntools_available (**NO OTHER TOOL CAN BE USED**): {tool_list}"
            }
        ]
    )
    #  If any of the steps has the wrong path, fix it.
    chain_of_thought = ollama.chat(
        model="llama3.2:latest",
        messages=[
            {
                "role": "system",
                "content": "You are a path fixer and chain of thought steps order validator. If any of the steps need reordering to fulfill the user intent, do it. Otherwise, return the same chain of thought as is. Do not write anything other than the chain of thoughts. Do proper numbering of the steps. **Each step should use EXACTLY 1 tool**. Always mention the absolute path of everything, and drives should be written as E:\ etc."
            },
            {
                "role": "user",
                "content": f"User Query: {user_query}\nChain of Thought:\n{chain_of_thought}\nDo not use tools other than the ones written in the chain of thought."
            }
        ]
    )

    return chain_of_thought["message"].content

def validate_chain_of_thought(chain_of_thought: str, user_query: str) -> int:
    isValid = ollama.chat(
        model="llama3.2:latest",
        messages=[
            {
                "role": "system",
                "content": f"""
                You are a chain of thought validator.

                Try to answer the following questions:
                - Is the chain of thoughts enough to satisfy the user's intent?
                - Is the chain of thoughts calling any unwanted APIs?
                - Is the chain of thoughts using tools that are not present in available tools?

                Available Tools:
                {tool_list}
                
                Output Format:
                0: Chain of thought is not valid
                1: Chain of thought is valid

                Do NOT write anything other than 0 or 1
                """
            },
            {
                "role": "user",
                "content": f"""
                User Query: {user_query}
                Chain of thought: {chain_of_thought}
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
        messages=[
            {
                "role": "tool",
                "content": "You are a tool which calls the necessary API for the current step."
            },
            {
                "role": "user",
                "content": f"Current Step: {state}\nChain of thought:\n{chain_of_thought}\ntools available: {tool_list}\nUser = `bhavy`\nPreviously taken steps:\n{prev_steps}"
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

def validate_tools(user_query: str, tool_calls: list) -> int:
    isValid = ollama.chat(
        model="llama3.2:latest",
        messages=[
            {
                "role": "system",
                "content": """
                You are a tool validator.
                Output Format:
                0: Tool(s) is/are not valid
                1: Tool(s) is/are valid

                Return 1 IF AND ONLY IF, the user's intent is satisfied from start to end using all the tools in the same order as mentioned in Tool Calls
                """
            },
            {
                "role": "user",
                "content": f"""
                User Query: {user_query}
                Tool Calls: {tool_calls}
                """
            }
        ],
        format=validationOutput.model_json_schema()
    )

    return (json.loads(isValid["message"].content))["isValid"]

def execute_tools(tool_calls: list):
    pass

if __name__ == "__main__":
    # user_query = "Open E drive in file explorer, then create a folder named 'test'. then create a file named 'text.txt'. Then open the file."
    user_query = "Open youtube and play marshmello songs"

    print("--------------------------")
    print("Generating chain of thought...")
    print("--------------------------")
    chain_of_thought = generate_chain_of_thought(user_query)
    print("Generated chain of thought")
    print("--------------------------")

    counter: int = 0
    max_retries: int = 3

    print("Checking if Chain of Thought is valid...")
    while (counter < max_retries):
        is_cot_valid = validate_chain_of_thought(chain_of_thought, user_query)
        print(f"Valid Status: {is_cot_valid}")

        if (is_cot_valid):
            print("Chain of Thought is valid")
            break
        else:
            chain_of_thought = generate_chain_of_thought(f"User Query: {user_query}\nLast chain of thought which was invalid:\n{chain_of_thought}")

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
        are_tools_valid = validate_tools(user_query, tool_calls)
        print(f"Are tools valid: {are_tools_valid}")

        if (are_tools_valid):
            print("Tools are valid")
            break
        else:
            print("Retrieving new set of tools")
            tool_calls = []
            for state in range(1, total_steps+1):
                tool_calls.append(retrieve_correct_tools(chain_of_thought, state, total_steps, tool_calls))
    
        
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