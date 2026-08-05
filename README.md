# Hooshek

Hooshek is a command-line interface tool for managing sports competitions, primarily focused on cross-country skiing. It assists in registering athletes, assigning bib numbers, and generating final rankings based on categories.

## Installation

1. **Install uv**<br>
    uv is a Python package and dependency manager. Install it from [https://docs.astral.sh](https://docs.astral.sh/uv/reference/installer/).

2. **Clone the repository**
    ```bash
    $ git clone https://github.com/sobulik/hooshek.git
    $ cd hooshek
    ```

3. **Make sure Python is installed**<br>
    Many environments come with pre-installed Python.
    ```bash
    $ uv python find
    ```
    If you see an error, install Python with
    ```bash
    $ uv python install
    ```

4. **Install project dependencies**
    ```bash
    $ uv sync --all-groups
    ```

5. **Verify the installation**
    ```bash
    $ uv run pytest
    ```

## Usage

1. **Copy the test folder**
    The easiest way to start is to copy one of the existing test folders.
    ```bash
    $ cp -r tests/data/2025-skuhrovska-lyze my-folder
    $ cd my-folder
    ```

2. **Generate the start list**
    ```bash
    $ uv run --project <PROJECT_PATH> <PROJECT_PATH>/src/hooshek/start.py
    ```
    Check the generated start list at start.yaml and start.txt.

3. **Generate the results**
    ```bash
    $ uv run --project <PROJECT_PATH> <PROJECT_PATH>/src/hooshek/finish.py
    ```
    Check the generated results at results.yaml and results.txt.

4. **Modify the input and re-run**
   Modify the input files event.yaml, clubs.yaml, athletes.yaml and finish.yaml as needed.
   Run start.py, finish.py scripts as above to get the updates.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
