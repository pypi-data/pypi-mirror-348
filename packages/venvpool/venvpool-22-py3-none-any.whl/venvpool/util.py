from . import pooldir, SharedDir
from pathlib import Path
from subprocess import check_output
import logging, os, re

log = logging.getLogger(__name__)

def detach():
    '''For all venvs (typically just one) that this process has locked for reading, set those locks to non-inheritable.
    Return a copy of os.environ in which PATH does not include the bin directories of those venvs.
    Then passing that environment to a subprocess will launch it free of any venvpool venv.'''
    bindirs = set()
    getmatch = re.compile(f"""n({re.escape(f"{pooldir}{os.sep}")}.+){re.escape(f"{os.sep}{SharedDir.readlocksname}{os.sep}")}""").match
    v = check_output(['lsof', '-F', 'fn', '-p', str(os.getpid())]).decode().splitlines()
    for f, n in zip(v[1::2], v[2::2]):
        m = getmatch(n)
        if m is not None:
            fd = int(f[1:])
            log.debug("Set non-inheritable: %s", fd)
            os.set_inheritable(fd, False)
            bindirs.add(Path(m.group(1), 'bin'))
    env = os.environ.copy()
    PATH = env.get('PATH')
    if PATH is not None:
        v = []
        for p in PATH.split(os.pathsep):
            if Path(p) in bindirs:
                log.debug("Exclude from PATH: %s", p)
            else:
                v.append(p)
        if v:
            env['PATH'] = os.pathsep.join(v)
        else:
            del env['PATH']
    return env
