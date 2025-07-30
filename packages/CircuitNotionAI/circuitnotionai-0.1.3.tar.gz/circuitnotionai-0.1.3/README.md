# CircuitNotionAI

A Python client for the CircuitNotion AI API.

## Installation

```bash
pip install CircuitNotionAI
```

## Usage

```python
from CircuitNotionAI import CNAI

# Initialize client
client = CNAI.Client(api_key="your_api_key")

# Generate content
response = client.models.generate_content(
    model="circuit-2-turbo",
    contents="explain simply how to beat procrastination",
    temperature=0.7,
    max_tokens=200
)
print(response.txt)
```

## License

MIT License
```

3. Move your existing code:
- Move CircuitNotionAI.py into the CircuitNotionAI directory and rename it to `__init__.py`

4. Create a build and upload to PyPI:
```bash
python -m pip install --upgrade build
```
```bash
python -m build
```
```bash
python -m pip install --upgrade twine
```
```bash
python -m twine upload dist/*
```

When running the final upload command, you'll need to enter your PyPI username and password.

5. Additional files you might want to add:
```markdown:CircuitNotionAI-package/LICENSE
MIT License

Copyright (c) 2025 CircuitNotionAI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...
```

The directory structure should look like this:
```
CircuitNotionAI-package/
├── CircuitNotionAI/
│   └── __init__.py
├── tests/
├── setup.py
├── README.md
└── LICENSE
```

After uploading, users can install your package using:
```bash
pip install CircuitNotionAI
