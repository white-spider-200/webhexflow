import cmd
import os
from modules.recon import (
    ffuf,
    ffuf_subs,
    whatweb,
    webanalyze,
    nmap_http
)
from modules.utils import export_cmd  # <-- New import

PROJECTS_DIR = "projects"

class WebHexflowShell(cmd.Cmd):
    intro = "Welcome to WebHexflow — type 'help'.\n"
    prompt = "webhexflow$ "
    current_project = None

    def preloop(self):
        os.makedirs(PROJECTS_DIR, exist_ok=True)

    def update_prompt(self):
        self.prompt = f"webhexflow({self.current_project})$ " if self.current_project else "webhexflow$ "

    def do_list(self, arg):
        """List all saved projects"""
        projects = os.listdir(PROJECTS_DIR)
        if not projects:
            print("No projects found.")
            return
        for i, p in enumerate(projects):
            print(f"{i}: {p}")

    def do_use(self, arg):
        """Select a project by name or index"""
        projects = os.listdir(PROJECTS_DIR)
        if arg.isdigit():
            idx = int(arg)
            if 0 <= idx < len(projects):
                arg = projects[idx]
            else:
                print("Index out of range.")
                return
        path = os.path.join(PROJECTS_DIR, arg)
        os.makedirs(path, exist_ok=True)
        self.current_project = arg
        self.update_prompt()
        print(f"Using {arg}")

    def do_recon(self, arg):
        """
        Run recon commands:
          subs         Subdomain discovery (ffuf_subs)
          dirs         Directory discovery (ffuf)
          fingerprint  Web server & tech fingerprinting (whatweb, webanalyze, nmap_http)
        """
        if not self.current_project:
            print("No project selected.")
            return

        cmd = arg.strip().lower()
        if cmd == "subs":
            ffuf_subs.run(self.current_project)

        elif cmd == "dirs":
            ffuf.run(self.current_project)

        elif cmd == "fingerprint":
            whatweb.run(self.current_project)
            webanalyze.run(self.current_project)
            nmap_http.run(self.current_project)

        else:
            print("Usage: recon [subs|dirs|fingerprint]")

    def do_export(self, arg):
        """
        Run a command and save its output to the current project's export log.
        Example:
            export sqlmap -u "http://example.com"
        """
        export_cmd.run_and_log(self.current_project, arg)

    def do_exit(self, arg):
        """Exit the tool"""
        print("Bye.")
        return True

    do_EOF = do_exit  # Ctrl+D

if __name__ == "__main__":
    WebHexflowShell().cmdloop()

