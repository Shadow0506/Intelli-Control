import subprocess
import logging
import os
import shutil

# def run_terminal_command(command: str):
#     try:
#         result = subprocess.run(command, shell=True, capture_output=True, text=True)
#         # logging.info(f"Shell command ran successfully")
#         return result.stdout
#     except Exception as e:
#         print(f"Could not run command: {e}")

# Works fine
def make_dir(folder_name: str) -> None:
    try:
        os.makedirs(folder_name, exist_ok=True)
        os.chdir(folder_name)
    except Exception as e:
        print(f"Could not execute command: {e}")

def remove_dir(folder_name: str) -> bool:
    try:
        if folder_name in os.listdir():
            os.rmdir(folder_name)
        else:
            print("Folder not found")
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

if __name__ == "__main__":
    # print(run_terminal_command(input("Enter command: ")))
    # make_dir("test_folder")
    # make_dir("test_folder_2")
    # make_dir("test_folder_3")
    remove_dir("test_folder")