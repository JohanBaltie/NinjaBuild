import os
import subprocess

from sublime import error_message, load_settings
from sublime_plugin import WindowCommand


class Ninja(WindowCommand):
    """
    Command to build using ninja.
    """

    def read_configuration(self):
        """
        Retrieve and override all the information mandatory or optional that
        will be used to create the quick panel and launch the build.
        """

        # retrieve the default settings
        settings = load_settings("ninja.sublime-settings")
        project = self.window.project_data()
        project_configuration = project.get("ninja")

        if (project_configuration is None):
            error_message("Ninja: ""ninja"" is not set in project.")
            return None

        def get(name):
            """
            Return the value taken from the project configuration or the
            default settings.
            """
            value = project_configuration.get(name,
                                              settings.get(name))

            if (value is None):
                error_string = ("Ninja: \"{0}\" not configured.").format(name)
                error_message(error_string)
            return value

        working_dir = project_configuration.get("working_dir")
        if not os.path.exists(working_dir):
            error_string = ("Ninja: "
                            "\"{0}\" does not exists").format(working_dir)
            error_message(error_string)
            return None

        return {
            "executable_name": get("executable_name"),
            "file_regex": get("file_regex"),
            "listing_command": get("listing_command"),
            "working_dir": working_dir }

    def list_targets(self, working_dir, listing_command):
        """
        List the targets ninja has to offer.
        """
        targets = list()
        listing_output = subprocess.check_output(listing_command,
                                                 cwd=working_dir)
        for target in str(listing_output, 'utf-8').splitlines():
            targets.append(target.split(':')[0])
        targets.sort()
        return targets

    def build_from_panel(self, panel, index, configuration):
        """
        Function called by the quick panels to start a build.
        """
        if (index == -1):
            return

        # Nope, there is something !
        currentBuild = panel[index]
        self.previousBuilds.append(currentBuild)
        command = [ configuration["executable_name"], panel[index] ]
        self.start_build(command,
                         configuration["working_dir"],
                         configuration["file_regex"])

    def start_build(self, command, working_dir, file_regex):
        """
        Start the build itself
        """
        build_system = {
            "cmd": command,
            "working_dir": working_dir,
            "file_regex": file_regex}
        self.window.run_command("show_panel",
                                {"panel": "output.exec"})
        output_panel = self.window.get_output_panel("exec")
        output_panel.settings().set("result_base_dir", build_system["working_dir"])
        print("Cmd: \"{Cmd}\"".format(Cmd=build_system))
        print("Result: {0}", self.window.run_command("exec", build_system))

    def run(self, build_all=False):
        """
        Command run call by the build system
        """
        configuration = self.read_configuration()

        if (configuration is None):
            return

        if build_all:
            self.start_build(configuration["executable_name"],
                             configuration["working_dir"],
                             configuration["listing_command"])
        else:
            panel = self.list_targets(configuration["working_dir"],
                                     configuration["listing_command"])
            if not hasattr(self, "previousBuilds"):
                self.previousBuilds = list()

            for previousBuild in self.previousBuilds:
                try:
                    panel.remove(previousBuild)
                except ValueError:
                    # When value was removed from list
                    pass
                panel.insert(0, previousBuild)
            self.window.show_quick_panel(panel,
                                        lambda index:
                                        self.build_from_panel(panel,
                                                              index,
                                                              configuration))
