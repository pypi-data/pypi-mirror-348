# SpokenPy

SpokenPy is an **open-source voice-driven programming interface** built for accessibility and inclusivity. It's ideal for blind users, differently-abled coders, and anyone who prefers to code by speaking.

## Features

- Voice-to-code translation using natural commands
- Inclusive: no fixed keywords (uses partial match, like "if greater" or "loop over list")
- Text-to-speech responses
- Simple CLI: `spokenpy`
- Extensible with custom voice-command mappings
- MIT Licensed

## Installation

```bash
pip install spokenpy
```

## Usage

Run the CLI:
```bash
spokenpy
```

Speak commands like:

- "print hello world"
- "if greater"
- "for loop"
- "while loop"
- "define function"
- "try except"
- "create class"

## Adding New Voice Commands

Edit `keywords.json` to map new phrases to Python code snippets.

## Accessibility First

- Designed for blind users
- Text-to-speech for feedback
- CLI-based (no mouse needed)
- Clear logs for screen readers

## PyPI Publishing

To release to PyPI:

```bash
pip install build twine
python -m build
twine upload dist/*
```

## License

MIT License – Free for personal and commercial use.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)