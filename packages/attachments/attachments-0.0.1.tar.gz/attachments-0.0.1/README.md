# Attachments

A basic Python library for handling version file types and providing them to llms as a mixt of images and text.

## Installation

```bash
pip install attachments
```

## Usage

```python
from attachments import Attachments

attachments = Attachments("path/to/attachments.pptx", "path/to/attachments.pdf")

attachments.render()

``` 