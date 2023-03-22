import importlib
import pkg_resources
import subprocess
import sys


def is_module_installed(module_name: str) -> bool:
  """as it says on the tin"""
  known_modules = {pkg.key for pkg in pkg_resources.working_set}
  return module_name in known_modules


def install(module_name: str):
  """a helper function to aid us in installing a package. pip does not support
  calling its methods directly, hence we call pip via subprocess.

  Throws:
    CalledProcessError(retcode, cmd) if there is a non-zero exit code.

  h/t: https://www.activestate.com/resources/quick-reads/how-to-install-python-packages-using-a-script/
  """
  kwargs = [
    sys.executable,
    "-m",
    "pip",
    "install",
    module_name,
  ]
  subprocess.check_call(kwargs)


def load_module(module_name: str):
  """h/t: https://stackoverflow.com/questions/44492803/dynamic-import-how-to-import-from-module-name-from-variable/44492879#44492879"""
  module = importlib.import_module(module_name)
  globals().update(
    {n: getattr(module, n) for n in module.__all__}
    if hasattr(module, "__all__")
    else {k: v for (k, v) in module.__dict__.items() if not k.startswith("_")}
  )


def main(args):
  """this is where the stuff happens"""
  module_name = args[1]
  if not is_module_installed(module_name):
    install(module_name)
  load_module(module_name)


if __name__ == "__main__":
  main(sys.argv)
