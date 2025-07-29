![pylint workflow](https://github.com/DrMicrobit/dm-streamvalve/actions/workflows/pylint.yml/badge.svg)
![pytest workflow](https://github.com/DrMicrobit/dm-streamvalve/actions/workflows/pytest.yml/badge.svg)

# dm-ollamalib

Python package: helper functions to parse Ollama options from a string. Also show available options.

Nothing stellar, but these functionalities are somehow missing from the Ollama Python package.

# Installation
If you haven't done so already, please install [uv](https://docs.astral.sh/uv/) as this Python package and project manager basically makes all headaches of Python package management go away in an instant.

Simply do `uv add dm-ollamalib` and you are good to go.

In case you want to work with the GitHub repository (e.g., because testing out a branch or similar), do
`uv add git+https://github.com/DrMicrobit/dm-ollamalib`.

# Usage
Three function are provided:
1. two helper functions that return as string a list of Ollama options, their type, and if available a short description
2. a parsing function that parses a string and returns a dictionary compatible for use with Ollama

## Functions to describe Ollama options
Both functions return a string.

> [!NOTE]
> For name and type of the options, dm-ollamalib uses information directly from the [Ollama Python library](https://github.com/ollama/ollama-python), which must be installed, e.g. via `uv add ollama`.
> That is, the strings returned are dynamically generated and adapted to the version of the Ollama Python library you have installed.

1. **help_overview()**: returns a string showing name and type of supported Ollama options. String will look like this:
```
                numa : bool
             num_ctx : int
           num_batch : int
...
```

2. **help_long:()**: returns a string showing name, type and description of supported Ollama options. The string will look like this:

```
numa : bool
This parameter seems to be new, or not described in docs as of January 2025.
dm_ollamalib does not know it, sorry.

num_ctx : int
Sets the size of the context window used to generate the next token.
(Default: 2048)
...
```

> [!IMPORTANT]
> As no description texts for options are present in the Ollama Python library, they were copied into dm-ollamalib by hand from descriptions either from the [Ollama docs for model files](https://github.com/ollama/ollama/blob/main/docs/modelfile.md) on GitHub or the [Ollama Python library package](https://pypi.org/project/ollama-python/) on PyPi. Note that some options have no description online at all, dm-ollamalib will tell you that.


## Function to parse strings representing Ollama options
`to_ollama_options()` transforms a string (or an Iterable of strings) with semicolon separated Ollama options to a dict compatible with Ollama.

The Python Ollama library wants the Ollama options as correct Python types in a dict, i.e., one cannot use strings. This functions transforms any string with
Ollama options into a dict with correct types.

Ollama uses a TypedDict, the dict[str, Any] returned by this function is compatible.

Arguments:
- **options : str | Iterable[str]**  
E.g. "num_ctx=8092;temperature=0.8" or ["num_ctx=8092","temperature=0.8"]

Exceptions raised:
- **ValueError** for
    - unrecognised Ollama options
    - conversion errors of a string to required type (int, float, bool), e.g. "num_ctx=NotAnInt"
    - incomplete options (e.g. "num_ctx=" or "=8092")
    - unknown Ollama options
- **RuntimeError**
    - if Ollama Python library has unexpected parameter types not handled by this function (should not happen, except if Ollama devs implemented something new)

# Usage examples

```python
from dm_ollamalib.parse_options import help_long, help_overview, to_ollama_options

print(help_overview())
print(help_long())

print(to_ollama_options("top_p=0.9;temperature=0.8"))
print(to_ollama_options(["top_p=0.9", "temperature=0.8"]))
```

The first two lines will print the generated help texts for the options present in the Ollama Python package. The two subsequent lines show how to parse options from one or several strings coming from, e.g. command line.

The dictionary returned by `to_ollama_options()` can be used directly in calls to Ollama. E.g.

```python
import ollama
from dm_ollamalib.optionhelper import to_ollama_options

op = to_ollama_options("top_p=0.9;temperature=0.8")
ostream = ollama.chat(
    model="llama3.1",
    options=op,          # the options parsed from string
    ...
)
```
> [!IMPORTANT]
> For the code above to work, you need to have (1) [Ollama](https://ollama.com) installed and running, the *llama3.1* model installed in Ollama (`ollama pull llama3.1`), and (3) your Python project needs to have the Ollama Python module installed via, e.g., `uv add ollama`.


# Notes
The GitHub repository comes with all files I currently use for Python development across multiple platforms. Notably:

- configuration of the Python environment via `uv`: pyproject.toml and uv.lock
- configuration for linter and code formatter `ruff`: ruff.toml
- configuration for `pylint`: .pylintrc
- git ignore files: .gitignore
- configuration for `pre-commit`: .pre-commit-config.yaml. The script used to check `git commit` summary message is in devsupport/check_commitsummary.py
- configuration for VSCode editor: .vscode directory
