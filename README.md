# CAN Message Generator

## Description
This program was made by and for the Solar Car Team at UVA. This program generates simulated CAN Messages. 

## Installation 

1. Clone this repo onto your machine
2. `cd` into the project folder
3. Create a python virtual environment (`py -m venv .venv`) and activate it (`.\.venv\Scripts\activate`)
    - you may need to use `python` or `python3` instead of `py`
    - on Mac, run `source ./.venv/bin/activate` to activate the virtual environment
4. Install cantools (`pip install cantools`)

## Use

**Setting up the Config file**

A JSON file must be created. It contains a dictionary (outer dictionary) of dictionaries (inner dictionaries). The keys to the outer dictionary are CAN message names (like `ECUMotorCommands`); its value is an inner dictionary. The inner dictionary contains key-value pairs for signals of the CAN message and their value (like `"throttle": 25`). Signals left undefined will be assumed to be 0.

The value of a signal will be re-evaluated for every message generated. The value can be dynamically set by using a python expression in a string for a signal's value; the expression can contain these elements:
1. `math` package functions.
2. `random` package functions (random was imported as `rand`)
3. `i`, which is the iteration number of the current message

See `config_example.json` for an example. 



**Running the Program**

After completing the steps in *Installation*, run `py main.py path number`
- replace `path` with the path of the Config JSON file
- replace `number` with the number of messages to be created; can use scientific notation (like `1e3`)
- the output is stored in `out.txt`
