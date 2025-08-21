import os
import shlex
import subprocess
import datetime

def run_and_log(project_name, command):
    if not project_name:
        print("No project selected.")
        return

    if not command.strip():
        print("Usage: export <command>")
        return

    # Create project export folder
    log_dir = os.path.join("projects", project_name, "exports")
    os.makedirs(log_dir, exist_ok=True)

    # File name = timestamp + first word of command
    tool_name = command.split()[0]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"{tool_name}_{timestamp}.log")

    try:
        # Run the command and capture output
        result = subprocess.run(
            shlex.split(command),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        # Save command + output
        with open(log_file, "w") as f:
            f.write(f"[{timestamp}] COMMAND: {command}\n")
            f.write("OUTPUT:\n")
            f.write(result.stdout)

        print(result.stdout)
        print(f"[+] Command & output saved: {log_file}")

    except FileNotFoundError:
        print(f"[!] Command not found: {command}")
