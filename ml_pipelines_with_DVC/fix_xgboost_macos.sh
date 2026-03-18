#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "This repair script is only for macOS."
  exit 1
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
venv_python="$repo_root/.venv/bin/python"
runtime_prefix="$repo_root/.xgboost-runtime"

if [[ ! -x "$venv_python" ]]; then
  echo "Expected a virtualenv Python at $venv_python"
  echo "Create the repo venv and install requirements first."
  exit 1
fi

conda_bin="$(command -v conda || true)"
if [[ -z "$conda_bin" && -x /opt/anaconda3/bin/conda ]]; then
  conda_bin="/opt/anaconda3/bin/conda"
fi

if [[ -z "$conda_bin" ]]; then
  echo "Conda was not found."
  echo "Install Conda or install libomp with Homebrew, then retry."
  exit 1
fi

xgboost_lib="$("$venv_python" - <<'PY'
import glob
import os
import site
import sys

for base in site.getsitepackages():
    matches = glob.glob(os.path.join(base, "xgboost", "lib", "libxgboost.dylib"))
    if matches:
        print(matches[0])
        sys.exit(0)

print("Could not find xgboost/lib/libxgboost.dylib in the virtualenv.", file=sys.stderr)
sys.exit(1)
PY
)"

if [[ ! -f "$runtime_prefix/lib/libomp.dylib" ]]; then
  "$conda_bin" create -y -p "$runtime_prefix" -c conda-forge llvm-openmp
fi

if ! otool -l "$xgboost_lib" | grep -Fq "$runtime_prefix/lib"; then
  install_name_tool -add_rpath "$runtime_prefix/lib" "$xgboost_lib"
fi

"$venv_python" - <<'PY'
import xgboost
print(f"xgboost import OK: {xgboost.__version__}")
PY
