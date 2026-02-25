Module 5 – Advanced Design Patterns Calculator

Nana Amponsah
IS601 – Python for Web API Development
Instructor: Prof. Kaw
Spring 2026

Overview

This project builds on previous modules by implementing advanced Object-Oriented Programming principles and design patterns within a structured calculator application. The purpose of this module was to go beyond basic functionality and focus on clean architecture, modular design, maintainability, and scalability.

In addition to performing calculations, the system supports history management, undo/redo functionality, configurable settings through environment variables, and data persistence using file operations. The goal was to apply professional software design concepts in a practical and working system.

Features
Basic Operations

Addition

Subtraction

Multiplication

Division

Advanced Operations

Power

Root

History Management

View calculation history

Clear history

Undo last operation

Redo previously undone operation

File Operations

Save calculation history to file

Load calculation history from file

Configuration Support

The calculator supports environment-based configuration, including:

Maximum history size

Automatic saving

Decimal precision

Default file encoding

Design Patterns Implemented

This project demonstrates the following design patterns:

Factory Pattern

Used to centralize the creation of operation objects, making the system easier to extend with new operations without modifying existing logic.

Strategy Pattern

Each operation (add, subtract, multiply, etc.) implements its own execution behavior while sharing a common interface.

Observer Pattern

The history component updates automatically when new calculations are performed.

Memento Pattern

Supports undo and redo functionality by saving and restoring application state.

Facade Pattern

The REPL (calculator interface) provides a simplified interface to interact with the internal system components.

These patterns improve modularity, separation of concerns, and scalability.

Installation Instructions

Clone the repository:
git clone https://github.com/n-amponsah/module5_is601.git
cd module5_is601

Set up a virtual environment:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Create a .env file in the project root:
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_DEFAULT_ENCODING=utf-8

Running the Application

Start the calculator:
python3 main.py

Use help inside the REPL to view available commands.

Running Tests

To run unit tests:
pytest

All tests pass successfully (99 tests)

Code Coverage

Coverage reports can be generated using:
pytest --cov=app --cov-report=term-missing

Current coverage: 82%

HTML coverage reports are generated in the htmlcov directory.

Reflection

This module strengthened my understanding of how OOP principles apply in real systems. Implementing design patterns helped structure the application in a more organized and scalable way. While some patterns required additional time to fully understand, applying them in a working project made their purpose clearer. This project demonstrates both functional implementation and architectural design.