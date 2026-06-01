# AI-leraning-helper
a homework done when learning the course The Mathematical Thinking of Artificial Intelligence


# AI Code Learning Assistant

An intelligent learning system that helps students understand code by analyzing knowledge points, explaining concepts, and providing interactive exercises.

## Quick Start

1. Double-click `??????????.bat` to run
2. Edit `code_input.txt` - paste your code there
3. Edit `highlight_input.txt` - paste confusing parts (optional)
4. Press Enter in the program
5. Enter your DeepSeek API Key

## Features

### Part 1: Code Analysis
- Analyzes your code to find programming knowledge points
- Compares highlighted vs full code to identify confusion areas

### Part 2: Knowledge Explanation
- Interactive learning for each knowledge point
- AI explains unfamiliar concepts with code examples

### Part 3: Practice Exercises
- Fill-in-the-blank exercises
- C++ code compilation and execution
- AI verification without revealing answers

## File Guide

| File | Purpose |
|------|---------|
| `??????????.bat` | Run this (double-click) |
| `code_input.txt` | Paste your complete code here |
| `highlight_input.txt` | Paste highlighted/confusing code (optional) |
| `exercise_answer.txt` | Auto-generated when doing exercises |
| `main.py` | Main program (don't edit) |

## Installation

If needed, the batch file will automatically install:
- Python 3.7+
- requests library (via pip)

## Workflow

```
Edit code_input.txt
        ??
Run ??????????.bat
        ??
Enter API Key
        ??
[Part 1: Analysis] ?? Identifies knowledge points
        ??
[Part 2: Explanation] ?? Interactive learning
        ??
[Part 3: Exercises] ?? Fill-in-blank practice
        ??
Complete!
```

## Project Structure

```
AI_learning_helper/
?????? main.py                    # Main program
?????? deepseek_api.py             # API interface
?????? prompt_engineering.py       # AI prompts
?????? code_analyzer.py           # Code analysis
?????? knowledge_explainer.py     # Knowledge teaching
?????? exercise_practice.py       # Exercise system
?????? requirements.txt            # Dependencies
?????? ??????????.bat            # Launcher (double-click this!)
?????? code_input.txt             # Your code goes here
?????? highlight_input.txt        # Highlighted code (optional)
?????? exercise_answer.txt        # Generated for exercises
?????? README.md                  # This file
```

## API Key Setup

1. Visit https://platform.deepseek.com/
2. Register an account
3. Get your API key
4. Enter it when prompted

## Notes

- Exercises currently support C++ only
- Requires g++ compiler for code execution
- All prompts and UI are in English
- API calls may incur costs
