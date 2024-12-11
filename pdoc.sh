# This script is used to update InputMaker documentation automatically.
# Requires pdoc, install it with `pip install pdoc`.
# Run this script as `source pdoc.sh`.

# Extract the version number from constants.py
version="$(grep -oP 'version\s*=\s*\K.*' ./thoth/__init__.py | tr -d "'")"
# Update README.md header with the version number
sed -i "s/^# Thoth.*/# Thoth $version/" README.md
# Generate the documentation
pdoc ./thoth/ -o ./docs --mermaid --math --footer-text="Thoth $version documentation"
