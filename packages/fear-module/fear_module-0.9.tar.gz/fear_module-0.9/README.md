# fear_module

![Python 3.8, 3.9, 3.10, 3.11, 3.12](https://img.shields.io/badge/Python-3.8|3.9|3.10|3.11|3.12-orange)

**fear_module** - this module is a Python library for creating troll applications!


**FEAR** - is an entertainment project. Be **careful** with him. **It is not subject to monetization**.


## Installation

Install the current version with [PyPI](https://github.com/Keker-dev/fear_module.git):

```bash
pip install fear_module
```

Or from Github:
```bash
pip install https://github.com/Keker-dev/fear_module.git
```

## Usage

```python
app = Fear(main_text="text", main_image="/path_to_image")

if __name__ == '__main__':
    app.run()
```

## Example

Add one scene.

```python
from fear_module import Fear

app = Fear(main_text="text", main_image="/path_to_image")
app.add_scene(
    name="FirstScene",
    text="text",
    image="/path_to_image",
    sound="/path_to_sound",
    button_text="click me",
)

if __name__ == '__main__':
    app.run()
```


## Contributing

Bug reports and/or pull requests are welcome


## License

The module is available as open source under the terms of the **MIT License**


