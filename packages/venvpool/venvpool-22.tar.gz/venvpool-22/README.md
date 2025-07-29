# venvpool
Run your Python scripts using an automated pool of virtual environments to satisfy their requirements.

This README is auto-generated, see [project wiki](https://wikiwheel.net/s/foyono/w/venvpool) for details.

## Commands

### motivate
Create and maintain wrapper scripts in ~/.local/bin for all runnable modules in the given projects, or the current project if none given.

## API

<a id="venvpool"></a>

### venvpool

<a id="venvpool.dotpy"></a>

###### dotpy

Python source file extension including dot.

<a id="venvpool.initlogging"></a>

###### initlogging

```python
def initlogging()
```

Initialise the logging module to send debug (and higher levels) to stderr.

<a id="venvpool.util"></a>

### venvpool.util

<a id="venvpool.util.detach"></a>

###### detach

```python
def detach()
```

For all venvs (typically just one) that this process has locked for reading, set those locks to non-inheritable.
Return a copy of os.environ in which PATH does not include the bin directories of those venvs.
Then passing that environment to a subprocess will launch it free of any venvpool venv.

