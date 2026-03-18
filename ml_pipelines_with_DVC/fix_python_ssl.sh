#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
venv_python="$repo_root/.venv/bin/python"

if [[ ! -x "$venv_python" ]]; then
  echo "Expected a virtualenv Python at $venv_python"
  echo "Create the repo venv and install requirements first."
  exit 1
fi

"$venv_python" -m pip install --quiet --disable-pip-version-check certifi

sitecustomize_path="$("$venv_python" - <<'PY'
import os
import site

for base in site.getsitepackages():
    print(os.path.join(base, "sitecustomize.py"))
    break
PY
)"

cat > "$sitecustomize_path" <<'PY'
"""Configure Python's default HTTPS trust store for this virtualenv."""

import os

try:
    import certifi
except Exception:
    cert_path = None
else:
    cert_path = certifi.where()

if cert_path:
    os.environ.setdefault("SSL_CERT_FILE", cert_path)
    os.environ.setdefault("REQUESTS_CA_BUNDLE", cert_path)
    os.environ.setdefault("CURL_CA_BUNDLE", cert_path)

    try:
        import ssl
    except Exception:
        pass
    else:
        _orig_create_default_context = ssl.create_default_context

        def _create_default_context(*args, **kwargs):
            if not any(key in kwargs for key in ("cafile", "capath", "cadata")):
                kwargs["cafile"] = cert_path
            return _orig_create_default_context(*args, **kwargs)

        ssl.create_default_context = _create_default_context
        ssl._create_default_https_context = _create_default_context
PY

"$venv_python" - <<'PY'
import ssl
import urllib.request

url = "https://raw.githubusercontent.com/entbappy/Branching-tutorial/refs/heads/master/tweet_emotions.csv"
with urllib.request.urlopen(url, timeout=20) as response:
    print("SSL fix OK:", response.status, ssl.get_default_verify_paths().openssl_cafile)
PY
