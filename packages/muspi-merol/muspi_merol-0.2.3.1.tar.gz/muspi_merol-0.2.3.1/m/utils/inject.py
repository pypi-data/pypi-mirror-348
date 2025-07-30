def restart_in_venv_if_needed():
    from os import getenv
    from pathlib import Path
    from shutil import which
    from sys import argv, executable

    if getenv("VIRTUAL_ENV") is not None and (venv_python := which("python")) is not None and str(Path(venv_python)) != executable:
        from site import getsitepackages
        from subprocess import run

        s = set(getsitepackages())
        exit(
            run(
                [
                    venv_python,
                    "-c",
                    f"import site,sys; sys.argv={['m', *argv[1:]]}; sys.path.extend({[*s, str(Path(__file__, '../' * 3).resolve())]}); site.addsitepackages({s}); from m.cli.main import app; app()",
                ]
            ).returncode
        )
