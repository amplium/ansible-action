import functools
import os
import shlex
import subprocess

from contextlib import ExitStack
from tempfile import NamedTemporaryFile

from typing import Callable
from typing import ParamSpec
from typing import TypeVar
from typing import Optional

P = ParamSpec("P")
T = TypeVar("T")


def retry(func: Callable[P, T], tries: int = 5) -> Callable[P, T]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        ntries = tries

        while ntries > 1:
            try:
                return func(*args, **kwargs)
            except Exception as exception:
                print(str(exception))

        return func(*args, **kwargs)

    return wrapper


def setup_private_key(environ: dict[str, str], defer: ExitStack) -> None:
    f = NamedTemporaryFile("w", delete=False, encoding="utf-8")

    environ["ANSIBLE_SSH_PRIVATE_KEY_FILE"] = f.name

    f.write(environ["ANSIBLE_PRIVATE_KEY"])
    f.close()

    defer.callback(lambda: os.remove(f.name))


@retry
def setup_requirements(environ: dict[str, str]) -> None:
    for file in shlex.split(environ["ANSIBLE_REQUIREMENTS"]):
        subprocess.run(
            ["ansible-galaxy", "collection", "install", "--requirements-file", file],
            check=True,
        )

        subprocess.run(
            ["ansible-galaxy", "role", "install", "--role-file", file],
            check=True,
        )


def run(environ: dict[str, str], defer: ExitStack) -> None:
    if "ANSIBLE_PRIVATE_KEY" in environ:
        setup_private_key(environ, defer)

    if "ANSIBLE_REQUIREMENTS" in environ:
        setup_requirements(environ)

    subprocess.run(
        [
            "ansible-playbook",
            *shlex.split(
                environ["ANSIBLE_OPTIONS"] if "ANSIBLE_OPTIONS" in environ else ""
            ),
            *shlex.split(environ["ANSIBLE_PLAYBOOK"]),
        ],
        check=True,
        env=environ | os.environ,
    )


def from_envs(*envs: str) -> Optional[str]:
    for env in envs:
        v = os.environ.get(env)

        if v:
            return v

    return None


def main() -> int:
    """
    Main entrypoint.
    """
    # Create a dict of ansible environment variables from action inputs.
    environ = {
        k.replace("INPUT_", "ANSIBLE_"): os.environ[k]
        for k in os.environ
        if k.startswith("INPUT_")
        if os.environ[k]
    }

    with ExitStack() as defer:
        try:
            run(environ, defer)
        except KeyboardInterrupt:
            return 0
        except Exception as exception:
            import traceback

            traceback.print_exception(exception)
        else:
            return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
