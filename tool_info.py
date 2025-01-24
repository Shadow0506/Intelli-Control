tool_list = [
    {
      "name": "create_directory",
      "description": "Creates a new directory with the specified name.",
      "parameters": {
        "folder_name": "str - The name of the folder to create.",
        "folder_creating_path": "str - The path where the new folder is to be created"
      },
      "required": ["folder_name", "folder_path"],
      "defaults": {
        "folder_name": "NoFolderNameFound",
        "folder_path": "E:\\"
      },
      "keywords": ["create directory", "make folder", "new directory", "filesystem"]
    },
    {
      "name": "delete_directory",
      "description": "Deletes the specified directory if it exists.",
      "parameters": {
        "folder_name": "str - The name of the folder to remove."
      },
      "required": ["folder_name"],
      "keywords": ["delete directory", "remove folder", "filesystem", "delete"]
    },
    {
      "name": "open_directory",
      "description": "Opens the specified directory path in the file explorer.",
      "parameters": {
        "folder_path": "str - The path of the folder to open."
      },
      "required": ["folder_name"],
      "keywords": ["open directory", "open folder", "file explorer", "navigate"]
    },
    {
      "name": "open_file",
      "description": "Opens the specified file with its default associated application.",
      "parameters": {
        "file_name": "str - The name or path of the file to open."
      },
      "required": ["file_name"],
      "keywords": ["open file", "file explorer", "launch file", "default application"]
    },
    {
      "name": "create_file",
      "description": "Creates a new empty file with the specified name.",
      "parameters": {
        "file_name": "str - The name or path of the file to create."
      },
      "required": ["file_name"],
      "keywords": ["create file", "new file", "file system", "generate file"]
    },
    {
      "name": "delete_file",
      "description": "Deletes the specified file if it exists.",
      "parameters": {
        "file_name": "str - The name or path of the file to delete."
      },
      "required": ["file_name"],
      "keywords": ["delete file", "remove file", "filesystem", "delete"]
    },
    {
      "name": "save_file",
      "description": "Saves the current file in use, typically for an application or editor.",
      "parameters": {},
      "required": [],
      "keywords": ["save file", "store file", "save changes", "editor"]
    },
    {
      "name": "move_mouse_to_coordinates",
      "description": "Moves the mouse cursor to the specified screen coordinates.",
      "parameters": {
        "x": "float - The x-coordinate to move the mouse to.",
        "y": "float - The y-coordinate to move the mouse to."
      },
      "required": [],
      "defaults": {
        "x": 0,
        "y": 0
      },
      "keywords": ["mouse movement", "cursor position", "move mouse", "coordinates"]
    },
    {
      "name": "two_key_shortcuts",
      "description": "Simulates pressing two keys simultaneously as a shortcut.",
      "parameters": {
        "key1": "str - The first key in the shortcut.",
        "key2": "str - The second key in the shortcut."
      },
      "required": ["key1", "key2"],
      "keywords": ["keyboard shortcut", "key combination", "hotkeys", "simulate keys"]
    }
]  