# Natural Numbers Interpretation

A Python application that interprets spoken Greek phone number digit sequences and identifies possible phone number combinations, validating them against predefined Greek phone number formats.

## Features

- Accepts space-separated digit groups (1–3 digits each).
- Expands Greek digit ambiguities into all possible number combinations.
- Validates each result against Greek phone number formats.
- Displays interpretations in a table with a `VALID` / `INVALID` result.
- Runs interactively, either locally or in Docker.

## Usage

Enter digit groups separated by spaces to see the possible phone number interpretations and their validation results.
Type 'q' or press Ctrl+C to quit.

## Rules
- Phone numbers strictly `10` or `14` digits
- If `10` digits: must start with `2` or `69`
- If `14` digits: must start with `00302` or `003069`
- Ambiguities in `GREEK`
- `Ambiguity 1`: 20 5 -> 205 or 25
- `Ambiguity 2`: 75 -> 75 or 705
- `Ambiguity 3`: 725 -> 725 or 700 20 5 or 700 25 or 720 5
- `Ambiguity 4`: 720 -> 720 or 700 20 or 72 (if next number is 1-9) or 700 2 (if next number is 1-9)
- `Ambiguity 5`: 702 -> 702 or 700 2
- `Ambiguity 6`: 700 -> 700 or 70 (if next number is 1-9) or 7 (if next number is 10-99)

## Assumptions
- 2 10 6 9 30 6 6 4 in GREEK should have 10 6 -> 16 or 106
- Some combinations are intentionally excluded because `11` and `12` cannot be split in Greek spoken numbers.

## Requirements

- **Language:** Python >=3.12
- **Dependencies:** pandas 3.1.0, pytest 9.1.1
- **Containerization:** Docker

## Run Locally

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python phone_number_interpretator.py
```

## Run Tests

Run the test suite using pytest:

```bash
pytest -v
```

## Build and Run with Docker

Build the Docker image:

```bash
docker build -t phone-number-app .

or

bash built_image.sh
```

Run the application:

```bash
docker run -it --rm phone-number-app

or

bash run_app.sh
```

Run the tests:

```bash
docker run --rm phone-number-app pytest -v

or

bash run_tests.sh
```

## Project Files

- `phone_number_interpretator.py` - Main application.
- `test_cases.py` - Automated tests.
- `requirements.txt` - Python dependencies and versions.
- `Dockerfile` - File for docker.