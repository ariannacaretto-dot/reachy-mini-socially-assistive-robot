# reachy-mini-socially-assistive-robot
A Python-based Socially Assistive Robot prototype designed to support social interaction and cognitive stimulation among older adults.

## Overview

This project was developed by a team of four students as part of a university course in Human-Computer Interaction (HCI).

The goal was to explore how a **Socially Assistive Robot (SAR)** could support social interaction and cognitive stimulation among older adults living in residential care facilities.

Using Reachy Mini and Python, we developed a prototype featuring interactive activities and adaptive dialogue designed to encourage engagement while respecting users' preferences and autonomy.

## Features

The prototype includes:

- **Personalized interaction:** greetings and dialogue adapted to the user's responses.
- **Word categorization game:** a cognitive activity based on identifying word categories, with hints and feedback.
- **Music quiz:** users match songs with their singers and can share memories associated with the music.
- **Expressive movements:** Reachy uses programmed head and antenna movements to accompany the interaction.
- **User autonomy:** users can change activities or stop the interaction at any time.

## Technologies

- Python
- Reachy Mini
- Reachy Mini recorded movements and emotions libraries

## Testing

The prototype was tested with an older participant, Concetta, using a simulator. The interaction took place through the terminal: the participant read Reachy's text responses and entered her replies using the keyboard.

## Project files

- `hello_reachy.py` – Python implementation of the prototype.
- `requirements.txt` – project dependencies.
- `presentation.pdf` – university project presentation.

## Running the project

1. Set up the Reachy Mini simulation environment.
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Python script:

   ```bash
   python hello_reachy.py
   ```

*Note: The prototype uses terminal-based text input and output. It does not implement speech recognition or voice-based conversation.*

## Context

University project | Human-Computer Interaction | 2025–2026

Developed collaboratively by a team of four students.
