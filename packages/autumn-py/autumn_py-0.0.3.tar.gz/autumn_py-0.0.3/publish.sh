# #!/bin/bash

rm -rf dist

hatch build

hatch publish

CURRENT_VERSION=$(grep -E '^__version__ = "[0-9]+\.[0-9]+\.[0-9]+"' src/autumn/__about__.py | cut -d'"' -f2)

echo "pip uninstall autumn-py && pip install autumn-py==$CURRENT_VERSION"
# Read current version


# echo "Current version: $CURRENT_VERSION"

# # Remove current version from PyPI
# pip install twine
# twine remove autumn-py==$CURRENT_VERSION


# if [ -z "$CURRENT_VERSION" ]; then
#     echo "Error: Could not find version number in __about__.py"
#     exit 1
# fi

# # Increment patch version (x.x.1 -> x.x.2)
# NEW_VERSION=$(echo $CURRENT_VERSION | awk -F. '{$NF = $NF + 1;} 1' OFS=.)

# # Update version in __about__.py
# sed -i "s/__version__ = \"$CURRENT_VERSION\"/__version__ = \"$NEW_VERSION\"/" src/autumn/__about__.py

# echo "Updated version from $CURRENT_VERSION to $NEW_VERSION"

