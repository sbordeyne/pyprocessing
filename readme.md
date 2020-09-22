# PyProcessing

Write and execute Processing code in pure python

## Installation

Using pip :

`pip install pyprocessing2`

From source :

`python3 setup.py install`

## Executing a sketch

`python3 -m pyprocessing run path/to/sketch.py`


## What is Processing?

"Processing is a flexible software sketchbook and a language for learning how to code within the context of the visual arts." By Processing.org

## What is PyProcessing?

PyProcessing's goal is to provide a framework to write (and run) processing-like code in Python. Processing is indeed a nice language, but Python provides many features that make the developer's life easier, such as comprehensions, easy monkey patching, and a plethora of third-party modules.

PyProcessing's intent is to be as transparent as possible for a developer used to Processing, with sketches that are exactly alike in both frameworks, albeit pythonized (variables and functions use `snake_case` instead of `camelCase`, for instance).

In the future, PyProcessing may even include a tool to "convert" an existing processing sketch to PyProcessing.

## Contributors

See [the AUTHORS.md file](../blob/master/AUTHORS.md)

See [the CONTRIBUTING.md file](../blob/master/CONTRIBUTING.md) for contributing guidelines.

## License

This project is published under the terms of the [MIT License](../blob/master/LICENSE)
