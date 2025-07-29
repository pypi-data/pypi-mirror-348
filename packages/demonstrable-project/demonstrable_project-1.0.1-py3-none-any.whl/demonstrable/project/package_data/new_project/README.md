# ${project_name}

${project_description}


# Project Structure

${project_dirname}
├── .venv/           - Directory containing the Demonstrable tools
├── README.md        - This file
├── pyproject.toml   - Project metadata and dependencies
├── recipe.yaml      - A demonstrable-deca recipe file
└── uv.lock          - A lock file for reproducible builds


# Accessing the Command-Line Tools

To gain easy access to the command-line tools of Demonstrable, you can
activate the environment containing them with the following command in your
terminal from within the project directory:

    cd ${project_dirname}
    source .venv/bin/activate

Activating the environment adds the various Demonstrable tools to your PATH,
in the current terminal session, allowing you to run them directly from the
command line.

# Next Steps

In your preferred order, you can:

- Create a narrative script with the `demonstrable-script-editor` command.

- Create slides with the `visning new-slide` command.

- Edit the `recipe.yaml` file to add your own dependencies and build
  steps (instructions inside).

With these in place, you can build your project with the
`demonstrable-deca build` command.
