# This script is used to update InputMaker documentation automatically.
# Requires pdoc, install it with `pip install pdoc`.
# Run this script as `source pdoc.sh`.

# Extract the version number from constants.py
version="$(grep -oP 'version\s*=\s*\K.*' ./inputmaker/tools.py | tr -d "'")"
# Update README.md header with the version number
sed -i "s/^# InputMaker.*/# InputMaker $version/" README.md
# Generate the documentation
pdoc ./inputmaker/ -o ./docs --mermaid --math --footer-text="InputMaker $version documentation"
