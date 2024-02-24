#!/bin/bash

# Prompt for the new version
read -p "Enter the new version: " version

if [[ -z "$version" ]]; then
    echo "Version cannot be empty"
    exit 1
fi

# Update version in setup.py
sed -i '' "s/this_version='.*'/this_version='$version'/" setup.py

# Add changes to git
git add .

# Commit changes
git commit -m "RELEASE: $version"

# Push changes
git push

# Tag the release
git tag -a "$version" -m "RELEASE: $version"

# Push tags
git push --tags

echo "Release $version pushed and tagged successfully."
