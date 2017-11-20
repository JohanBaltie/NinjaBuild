# Ninja
Build with *ninja* under *Sublime text*.

## What it provides

**ninja** build system allows to choose and build a given ninja target.

## Startup configuration

To activate it, select the **ninja** build system, you need a *Sublime* project that you will configure to have:

    "ninja":
    {
        # A mandatory path to the directory where you can launch ninja
        "working_dir": "path/to/projects/"
    }

After that your just have to press the build shortcut (**CTRL-B** or **F7**).

## Additional configuration

Here a more complete example of configuration:

    "ninja":
    {
        # Optional path to the ninja executable
        "executable_name": "path/to/ninja",

        # Command used to list the target
        "listing_command": [ "executable", "option" ],

        # Regexp to match error (see build system documentation)
        # Here is the default:
        "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$"

        # And still the mandatory path
        "working_dir": "path/to/projects/"
    }
