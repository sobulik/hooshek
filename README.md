# Hooshek

Hooshek is a command-line interface (CLI) tool for managing sports competitions, primarily focused on cross-country skiing. It assists in registering athletes, assigning bib numbers, and generating final rankings based on categories.

## Installation

1. **Make sure Python is installed**<br>
    Many environments come with pre-installed Python.
    ```bash
    $ python3 --version
    Python 3.13.5
    ```
    If you see an error or Python version is lower than 3.9, install Python 3.9 or above using your OS package manager. Alternatively, obtain it from [python.org](https://www.python.org/downloads/).

2. **Install PDM**<br>
    PDM is a Python package and dependency manager. Install it from [pdm-project.org](https://pdm-project.org/en/latest/).

3. **Clone the repository**
    ```bash
    git clone https://github.com/sobulik/hooshek.git
    cd hooshek
    ```

4. **Install dependencies**
    ```bash
    pdm install
    ```

5. **Verify the installation**
    ```bash
    pdm test
    ```

<!--
## Setup competition

1. **Configure the `event.yaml` file with your competition details:**

    ```yaml
    version: "1.0"
    name: Skuhrovská Steeplechase
    date: 2024-09-21
    encoding_print: "utf_8_sig"
    mass: true
    races:
      - age_min: 0
        age_max: 3
        sex: f
        name: Pulkyně
        distance: 100m
    ```

    The `mass` field is used to indicate whether the competition is a mass start.


2. **Register athletes by adding them to the `athletes.yaml` file manually:**

    ```yaml
    athletes:
    -   born: 2021
        name: Jiří
        sex: m
        surname: Kubsch
        club: SOSK
    ```
    By specifying the `id` field, you can manually assign a bib number to the athlete.

3. **Register athletes by importing them from Czech Ski Association csv file:**

    ```bash
    python register.py --file ./athletes.csv
    ```

## Basic Commands

### Create start list

Create start list of the competition by assigning categories and bib numbers to athletes and create start list.

```bash
python start.py
```

### Create final rankings

 1. Enter results of the athlets into finish.yaml file.
    ```yaml
    - {id: "J1", time: "00:00:48.6"}
    ```
 2. Run the `finish.py` command to generate the final rankings in txt, csv and json formats. The txt format is the default output format. Use --format option to specify the output format.

```bash
python finish.py
```
-->

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
