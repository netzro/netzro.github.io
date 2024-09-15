#!/bin/bash

# Error handling function
handle_error() {
  echo "Error: $1"
  exit 1
}

# Check if a commit message was provided as an argument
if [ -z "$1" ]; then
  handle_error "No commit message provided. Usage: $0 <commit-message>"
fi

# Switch to the master branch
git checkout master || handle_error "Failed to switch to master branch."

# Generate the static site using Pelican
pelican content || handle_error "Pelican failed to generate the site."

# Check the status of the repository and include untracked files
if [ -z "$(git status -s)" ]; then
  echo "No changes to commit."
  exit 0
fi

# Stage all changes, including new files
git add -A || handle_error "Failed to stage changes."

# Commit the changes with the provided message
git commit -m "$1" || handle_error "Failed to commit changes."

# Push the changes to the master branch on the remote repository
git push origin master || handle_error "Failed to push changes to master."

# Import the generated site to the gh-pages branch
ghp-import output -b gh-pages || handle_error "Failed to import to gh-pages branch."

# Push the gh-pages branch to the remote repository
git push origin gh-pages || handle_error "Failed to push gh-pages branch."

# Success message
echo "***********************"
echo "Site successfully deployed!"
echo "***********************"
