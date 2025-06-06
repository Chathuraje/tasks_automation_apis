import subprocess


async def run_ffmpeg_command(command: list[str]) -> str:
    """
    Runs the ffmpeg command and returns the output.

    Args:
        command (list[str]): The ffmpeg command to run.

    Returns:
        str: The output of the ffmpeg command.
    """

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
