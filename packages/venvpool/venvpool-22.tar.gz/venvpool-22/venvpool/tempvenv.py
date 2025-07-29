from . import executablebits, ParsedRequires, Pool
from .util import detach
from inspect import getsource
from pathlib import Path
from subprocess import check_call
from tempfile import TemporaryDirectory
import logging, os, sys

log = logging.getLogger(__name__)

class Shell:

    def __init__(self):
        self.path = os.environ['SHELL']

    def run(self, script, *args):
        check_call([self.path, '-c', script, '-c', *args], env = detach())

def _temppip():
    from pathlib import Path
    from shutil import which
    import os, sys
    assert sys.argv[1] in {'check', 'debug', 'download', 'freeze', 'hash', 'help', 'list', 'search', 'show', 'wheel'}
    os.execv(Path(which('python')).parent / 'pip', sys.argv)

def main(args):
    requires = ParsedRequires(args.reqs)
    shell = Shell()
    if args.w:
        with Pool().readwrite(requires) as venv:
            shell.run('. "$1" && exec "$2"', Path(venv.venvpath, 'bin', 'activate'), shell.path)
    else:
        with Pool().readonly(requires) as venv, TemporaryDirectory() as tempdir:
            temppip = Path(tempdir, 'pip')
            temppip.write_text(f"#!{sys.executable}\n{getsource(_temppip)}_temppip()\n")
            temppip.chmod(temppip.stat().st_mode | executablebits)
            shell.run('. "$1" && PATH="$2:$PATH" && exec "$3"', Path(venv.venvpath, 'bin', 'activate'), tempdir, shell.path)
