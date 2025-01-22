import subprocess
import logging
import os
import shutil
import pyautogui
import time

# def run_terminal_command(command: str):
#     try:
#         result = subprocess.run(command, shell=True, capture_output=True, text=True)
#         # logging.info(f"Shell command ran successfully")
#         return result.stdout
#     except Exception as e:
#         print(f"Could not run command: {e}")

# Works fine whether folder exists or not
def make_dir(folder_name: str) -> None:
    try:
        if (folder_name not in os.listdir()):
            os.makedirs(folder_name, exist_ok=True)
            os.chdir(folder_name)
        else:
            print(f"Folder '{folder_name}' already exists in the path: {os.getcwd()}")
    except Exception as e:
        print(f"Could not execute command: {e}")

# Works well with empty as well as non-empty directories and whether folder exists or not
def remove_dir(folder_name: str) -> None:
    try:
        if folder_name in os.listdir():
            os.rmdir(folder_name)
        else:
            print(f"Folder '{folder_name}' does not exist in the path: {os.getcwd()}")
    except WindowsError as e:
        if (str(e) == f"[WinError 145] The directory is not empty: '{folder_name}'"):
            os.chdir(folder_name)
            choice = input(f"Folder is not empty, it contains the following contents:\n{os.listdir()}\nDo you want to delete it along with it's contents? (yes/no): ")
            os.chdir("..")
            if (choice.lower() == "yes"):
                shutil.rmtree(folder_name)
                print("Directory removed successfully")
            else:
                print("Directory removal cancelled")
    except Exception as e:
        print(f"Could not remove folder: {e}")

# Works fine whether directory exists or not
def open_dir(folder_path: str) -> None:
    try:
        os.startfile(folder_path)
        os.chdir(folder_path)
    except Exception as e:
        if (str(e) == f"[WinError 2] The system cannot find the file specified: '{folder_path}'"):
            choice = input(f"Folder '{folder_path}' does not exist in the path: {os.getcwd()}\nDo you want to create it? (yes/no): ")
            if (choice.lower() == "yes"):
                os.makedirs(folder_path, exist_ok=True)
                os.startfile(folder_path)
                os.chdir(folder_path)
                print("Folder created successfully.")
            else:
                print("Folder creation cancelled")
        else:
            print(f"Could not open directory: {e}")

# Works whether file exists or not
def open_file(file_name: str) -> None:
    try:
        os.startfile(file_name)
    except WindowsError as e:
        if (str(e) == f"[WinError 2] The system cannot find the file specified: '{file_name}'"):
            choice = input(f"File '{file_name}' does not exist in the path: {os.getcwd()}\nDo you want to create it? (yes/no): ")
            if (choice.lower() == "yes"):
                with open(file_name, 'w') as f:
                    f.write('')
                print("File created successfully.")
                os.startfile(file_name)
            else:
                print("File creation cancelled")
    except Exception as e:
        print(f"Could not open file: {e}")

# Works fine whether file with the name exists or not
def create_file(file_name: str) -> None:
    try:
        if (file_name not in os.listdir()):
            with open(file_name, 'w') as f:
                f.close()
        else:
            choice = input(f"File '{file_name}' already exists in the path: {os.getcwd()}\nDo you want to override it? (yes/no): ")
            if (choice.lower() == 'yes'):
                with open(file_name, 'w') as f:
                    f.close()
                print("File created successfully")
            else:
                print("File creation cancelled")
    except Exception as e:
        print(f"Error creating file: {e}")

# Works fine whether file exists or not
def delete_file(file_name: str) -> None:
    try:
        os.remove(file_name)
    except Exception as e:
        if (str(e) == f"[WinError 2] The system cannot find the file specified: '{file_name}'"):
            print(f"File '{file_name} does not exits in the path: {os.getcwd()}")
        else:
            print(f"Could not delete {file_name}: {e}")

# Ofcourse works fine
def save_file() -> None:
    try:
        time.sleep(1)
        pyautogui.hotkey('ctrl', 's')
    except Exception as e:
        print(f"Error while pressing Ctrl + S: {e}")

def move_mouse_to_coordinates(x: float, y: float, h: float, w: float) -> None:
    pass

# Works with 2 second delay so that the shortcut works as expected even when applications take time to open
def two_key_shortcuts(key1: str, key2: str) -> None:
    """
    This function is used to simulate shortcuts on Windows that require two keys to be pressed simultaneuosly.

    Args:
    key1: Key which is to be pressed first
    key2: Key which is to be pressed second
    """
    time.sleep(2)
    try:
        pyautogui.hotkey(key1.lower(), key2.lower())
    except Exception as e:
        print(f"Error while performing shortcut {key1} + {key2}: {e}")

if __name__ == "__main__":
    pass
    # print(run_terminal_command(input("Enter command: ")))
    # open_dir("E:\\")
    # open_dir("test_folder")
    # make_dir("test_folder")
    # make_dir("test_folder2")
    # remove_dir("test_folder")
    # open_file("new.txt")
    # delete_file("new.txt")
    # create_file('new.txt')