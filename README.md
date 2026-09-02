# Dice Roller

Dice Roller is a beginner-friendly terminal program that automatically rolls two dice and displays them as colorful ASCII art.

## Features

- Large `DICE ROLLER` title generated with the `art` library
- Rich panels, tables, borders, colors, animation, and menu layout
- Original ASCII dice faces displayed side-by-side
- Short rolling animation before each result
- Automatically roll two dice and calculate the total
- Lucky-roll, jackpot, and tough-luck messages
- No user input required

## Technologies/Libraries Used

- Python 3.9+
- `rich` for the terminal interface, panels, tables, colors, animation, and layout
- `colorama` for portable terminal color initialization, especially on Windows
- `art` for the large ASCII-art title
- Python standard library modules `random` and `time` for rolling and animation timing

## Project Structure

```text
DieGame/
├── dice.py
├── README.md
├── requirements.txt
└── run.py
```

## Requirements

- Python 3.9 or newer
- A terminal that supports standard text color codes
- Internet access the first time dependencies are installed

## Install Dependencies

From the project directory, run:

```bash
python -m pip install -r requirements.txt
```

On some systems, use `python3` instead of `python`.
## Run Locally

```bash
python dice.py
```

The program displays the dice and exits automatically. To install dependencies and run it in one step, use:

```bash
python run.py
```

## Build the Docker Image

From the project directory:

```bash
docker build -t dice-roller .
```

Use this minimal Dockerfile in the project directory:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY dice.py .
CMD ["python", "dice.py"]
```

## Run the Docker Container Interactively

```bash
docker run --rm -it dice-roller
```

The `-it` flags keep the container attached to your terminal so menu input works normally.

## Example Usage/Output

```text
How many dice? (1-6, or q to cancel) 3

Your Dice
 -----     -----     -----
| o o |   |     |   | o   |
|     |   |  o  |   |  o  |
| o o |   |     |   |   o |
 -----     -----     -----

Total: 10
A solid roll!
```

## Why Use `requirements.txt`?

`requirements.txt` records the external libraries required by the program in one portable, repeatable place. Developers, CI systems, and Docker builds can install the same dependencies with `python -m pip install -r requirements.txt`, reducing setup errors and making the project easier to share.
