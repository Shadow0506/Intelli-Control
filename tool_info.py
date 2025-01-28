tool_list = {
    "open_app": {
        "tool_name": "open_app",
        "description": "Opens the specified application by name.",
        "parameters": {
            "app_name": "str - The name of the application to open. Do NOT include path or extension."
        }
    },
    "close_app": {
        "tool_name": "close_app",
        "description": "Closes the specified application by name.",
        "parameters": {
            "app_name": "str - The name of the application to close. Do NOT include path or extension."
        }
    },
    "open_url": {
        "tool_name": "open_url",
        "description": "Opens the specified URL in the default web browser.",
        "parameters": {
            "url": "str - The URL to open."
        }
    },
    "create_directory": {
        "tool_name": "create_directory",
        "description": "Creates a new directory with the specified name.",
        "parameters": {
            "folder_name": "str - The name of the folder to create.",
            "folder_creation_path": "str - The ABSOLUTE path where the new folder is to be created"
        }
    },
    "delete_directory": {
        "tool_name": "delete_directory",
        "description": "Deletes the specified directory if it exists.",
        "parameters": {
            "folder_PATH": "str - The ABSOLUTE path of the folder to remove."
        }
    },
    "open_directory": {
        "tool_name": "open_directory",
        "description": "Opens the specified directory path in the file explorer.",
        "parameters": {
            "folder_path": "str - The ABSOLUTE path of the folder to open."
        }
    },
    "open_file": {
        "tool_name": "open_file",
        "description": "Opens the specified file with its default associated application.",
        "parameters": {
            "file_path": "str - The ABSOLUTE path of the file to open."
        }
    },
    "create_file": {
        "tool_name": "create_file",
        "description": "Creates a new empty file with the specified name.",
        "parameters": {
            "file_name": "str - The name of the file to create.",
            "file_path": "str - The ABSOLUTE path of the file to create."
        }
    },
    "delete_file": {
        "tool_name": "delete_file",
        "description": "Deletes the specified file if it exists.",
        "parameters": {
            "file_path": "str - The ABSOLUTE path of the file to delete."
        }
    },
    "save_file": {
        "tool_name": "save_file",
        "description": "Saves the current file in use, typically for an application or editor.",
        "parameters": {}
    },
    "move_mouse_to_coordinates": {
        "tool_name": "move_mouse_to_coordinates",
        "description": "Moves the mouse cursor to the specified screen coordinates.",
        "parameters": {
            "x": "float - The x-coordinate to move the mouse to.",
            "y": "float - The y-coordinate to move the mouse to."
        }
    },
    "two_key_shortcuts": {
        "tool_name": "two_key_shortcuts",
        "description": "Simulates pressing two keys simultaneously as a shortcut.",
        "parameters": {
            "key1": "str - The first key in the shortcut.",
            "key2": "str - The second key in the shortcut."
        }
    },
    "web_scrape": {
        "tool_name": "web_scrape",
        "description": "Takes the search query and returns the top 3 URLs from the web.",
        "parameters": {
            "query": "str - The search query to scrape the web for."
        }
    }
}