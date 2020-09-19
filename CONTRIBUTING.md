# Contributing.md

* Project page: https://github.com/Dogeek/PyProcessing
* Email me: simon.bordeyne@gmail.com

## Code contributions

The easiest code contributions are, in order from the easiest to the hardest :

1. Write documentation. Since `Processing` and `PyProcessing` are so similar, the functions retain their prototypes and behaviors, so the documentation is similar

2. Manually test, and open issues for bugs that arise. This project is still in beta and incomplete, bugs are expected.

3. Port basic functions from processing to this project. The functions must behave exactly as they do in processing, but *pythonized*, meaning that extensive use of keyword arguments and tuple unpacking is expected (python doesn't allow for function overloading)

4. Port more advanced features of processing over, especially functions that affect rendering (2D or 3D)

5. Create new renderers for PyProcessing.

6. Fix existing bugs. The issue tracker is [here](https://github.com/Dogeek/PyProcessing/issues)


## How to contribute

- Fork and clone your fork of this repository

- Add a remote pointing to this repository `git remote add dogeek https://github.com/Dogeek/pyprocessing.git`

- Create a new branch per feature contributed

- Open a Pull Request for that feature. Make sure to regularly rebase your feature branch onto the master repository `git pull --rebase dogeek master`

- Wait for the review.

Once enough of your contributions have been merged into the master branch, you will be invited to the core contributors, and be granted write access to the repo.

Remember to add your name and github profile to the AUTHORS.md file, for your first contribution. This change must be in a separate commit from your contribution (but in the same pull request).

## Tour of the project

The project is split into 3 parts : the renderers, the library and the CLI.

### Renderers

So far, there is only one renderer, `TkRenderer` which renders the sketch into a `tkinter` window. Renderers are tasked with the sole purpose of rendering the sketch. Rendering is kept separate from the library in order to be able to choose which backend to use for rendering (kivy, tkinter, pyqt, wxPython, pygame, pyglet or as a webserver). Some features of Processing may not work with some renderers, this should be included in the documentation.

### Library

The library is home to every function port from `Processing`. The library mostly interacts with the `PyProcessing` singleton, which in turns pass on the relevant information to the renderers attached to it.

### CLI

`PyProcessing` has a command-line interface accessible from `pyprocessing.__main___`. That CLI is responsible for handling all of the tools and commands required to run and use `PyProcessing`. Running the code is done through an instance of `pyprocessing.runner.Runner`, which is responsible for dynamically importing the sketch, calling its `setup()` function, and passing information to the `PyProcessing` object.
