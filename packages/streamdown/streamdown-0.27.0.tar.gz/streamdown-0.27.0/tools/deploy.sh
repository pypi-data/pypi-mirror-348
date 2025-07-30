#!/bin/bash
set -eEuo pipefail
version=$(grep version pyproject.toml  | cut -d '"' -f 2)
tag_update() {
    git tag -m v$version $version
    git push --tags
}
pipy() {
    source .venv/bin/activate
    for i in pip hatch build; do
        python3 -m pip install --upgrade $i
    done
    python3 -m build .
    twine upload dist/*${version}*
}
#tag_update
pipy
