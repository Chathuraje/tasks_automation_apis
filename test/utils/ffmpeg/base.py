import subprocess
from pathlib import Path

def run_ffmpeg_command(command: str):
    """
    Helper function to run FFmpeg commands.

    Args:
        command (str): The full FFmpeg command to be executed.

    This function uses the `subprocess.run` method to execute the provided FFmpeg command in the shell. 
    If an error occurs during execution, it catches the exception and prints an error message.
    """
    try:
        # Run the FFmpeg command
        result = subprocess.run(command, shell=True)
        print(f"FFmpeg command executed successfully: {command}")
        return result
    except subprocess.CalledProcessError as e:
        # Handle errors during FFmpeg execution
        print(f"Error executing FFmpeg command: {e}")
        print(f"Command that failed: {command}")
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error: {e}")
