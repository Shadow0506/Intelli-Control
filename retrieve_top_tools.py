import ollama
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.environ["GROQ_API_KEY"])
user_query = "Open E drive, then create a folder named test, then create a file text.txt inside it, then open the file. Then save the file then close the file then delete the folder"
# user_query = "Hi, I was thinking of listening to some songs"
prompt = f"""
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
"""

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "system",
            "content": "You are a tool selector"
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
)

# response = ollama.chat(
#     model="llama3.1:8b",
#     messages=[
#         {
#             "role": "tool",
#             "content": "You are a tool selector"
#         },
#         {
#             "role": "user",
#             "content": prompt
#         }
#     ],
# )

print("Groq output:")
print(response.choices[0].message.content)
prev_chain = ""

cot = ollama.chat(
    model="llama3.2:latest",
    messages=[
        {
            "role": "system",
            "content": """You are a chain of thought generator. 
            Do not write anything other than the chain of thoughts. 
            Do proper numbering of the steps. 
            **Each step should use EXACTLY 1 tool**. 
            Always Re-think if the chain of thought is sufficient to satisfy user intent.
            You do not need to use `open_app` API to use the `open_url` API.
            Return 'Query cannot be fulfilled' if there is even ONE things that cannot be fulfilled using the available tools."""
        },
        {
            "role": "user",
            "content": """User Query: "Hi, I was thinking of listening to some songs"
            -------------------
            tools_available (**NO OTHER TOOL CAN BE USED**): 
            {
            "name": "open_app",
            "description": "Opens the specified application by name.",
            "parameters": {
                "app_name": "str - The name of the application to open."
            }
            },
            {
            "name": "close_app",
            "description": "Closes the specified application by name.",
            "parameters": {
                "app_name": "str - The name of the application to close."
            }
            },
            {
            "name": "open_url",
            "description": "Opens the specified URL in the default web browser.",
            "parameters": {
                "url": "str - The URL to open."
            }
            }
            
            OUTPUT FORMAT:
            Strictly return only the name of the API and the parameter to give
            - Assume that your response is going straight to the API so do not write anything unnecessary"""
        }
    ]
)

print("Chain of thought:")
print(cot["message"].content)