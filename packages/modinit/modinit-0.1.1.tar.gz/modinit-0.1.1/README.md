# modinit

**modinit** is a Python package that helps you quickly scaffold AI model training repositories with a standardized, best-practice structure. It saves you time and ensures consistency across your machine learning projects.

## Why use modinit?

- **Instant project setup:** Get started with a ready-to-use directory structure in seconds.
- **Best practices built-in:** Follows common conventions for organizing data, code, configs, and tests.
- **Docstring templates:** All generated Python files include helpful docstrings.
- **Easy to use:** Simple command-line interface.

## Demo

![modinit demo](demo/modinit.gif)

## Installation

```bash
pip install modinit
```

## Usage

To create a new project, run:

```bash
modinit my-project
```

This will generate a new directory called `my-project` with a recommended structure for AI/ML projects.

### Example

Below is a real example of using `modinit` to create a project called `voice-rumba`:

```bash
$ pip install modinit
$ modinit voice-rumba
Successfully created project: voice-rumba
To get started, navigate to the project directory:
  cd voice-rumba
```

The generated structure looks like this:

```
voice-rumba/
├── README.md
├── .gitignore
├── configs/
│   └── config.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   └── interim/
├── main.py
├── notebooks/
│   └── prototype.ipynb
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── data.py
│   ├── evaluate.py
│   ├── model.py
│   ├── train.py
│   └── utils.py
└── tests/
    ├── __init__.py
    ├── test_data.py
    ├── test_model.py
    └── test_train.py
```

## Features

- Creates a well-structured project directory for AI model training
- Follows best practices for machine learning project organization
- Includes helpful docstrings in all generated files
- Simple command-line interface

## Development

To contribute to this project:

1. Clone the repository
2. Create a virtual environment
3. Install development dependencies: `pip install -e ".[dev]"`
4. Make your changes
5. Run tests: `pytest`

## License

MIT