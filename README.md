# Hooshek

Hooshek is a command-line interface tool for managing sports competitions, primarily focused on cross-country skiing. It assists in registering athletes, assigning bib numbers, and generating final rankings based on categories.

## Installation

1. **Install _uv_**<br>
    _uv_ is a Python package and dependency manager. Install it from [https://docs.astral.sh](https://docs.astral.sh/uv/reference/installer/).

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
    If not found, install Python with
    ```bash
    $ uv python install
    ```

4. **Install project dependencies**
    ```bash
    $ uv sync --locked
    ```

## Usage

1. **Set project variable**<br>
    _uv_ uses a project in _UV_PROJECT_ environment variable.
    ```bash
    $ export UV_PROJECT=`pwd`
    ```

2. **Copy the test folder**<br>
    The easiest way to start is to copy one of the existing test folders.
    ```bash
    $ cp -r ${UV_PROJECT}/tests/data/2025-skuhrovska-lyze my-folder
    $ cd my-folder
    ```

3. **Generate the start list**
    ```bash
    $ uv run --no-sync hooshek startlist
    ```
    Check the generated start list at start.yaml and start.txt.

4. **Generate the results**
    ```bash
    $ uv run --no-sync hooshek results
    ```
    Check the generated results at results.yaml and results.txt.

5. **Modify the input and re-run**<br>
   Modify the input files event.yaml, clubs.yaml, athletes.yaml and finish.yaml as needed.
   Run startlist, results scripts as above to get the updates.

## Development

1. **Install all dependency groups**
    ```bash
    $ uv sync --locked --all-groups
    ```

2. **Verify the installation**
    ```bash
    $ uv run pytest
    ```

3. **Run lint, format, type checks and all tests**
    ```bash
    $ make check
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
