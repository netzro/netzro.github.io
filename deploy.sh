#!/bin/bash

# Check if a commit message was provided as an argument
if [ -z "$1" ]; then
  echo "Error: No commit message provided."
  echo "Usage: $0 <commit-message>"
  exit 1
fi

# Switch to the master branch
git checkout master

# Generate the static site using Pelican
pelican content

# Check the status of the repository
git status -s

# Stage all changes
git add -A

# Commit the changes with the provided message
git commit -m "$1"

# Push the changes to the master branch on the remote repository
git push origin master

# Import the generated site to the gh-pages branch
ghp-import output -b gh-pages

# Push the gh-pages branch to the remote repository
git push origin gh-pages
