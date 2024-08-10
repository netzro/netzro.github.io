#!/bin/bash

# Function to display a progress bar
progress_bar() {
  local duration=$1
  local interval=0.1
  local steps=$(bc <<< "scale=2; $duration / $interval")
  for i in $(seq 1 $steps); do
    echo -ne "#"
    sleep $interval
  done
  echo ""
}

# Function to pause with a progress bar
pause_with_progress() {
  local duration=$1
  echo -ne "Processing: "
  progress_bar $duration
}

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
pause_with_progress 1

# Generate the static site using Pelican
pelican content || handle_error "Pelican failed to generate the site."
pause_with_progress 2

# Check the status of the repository and include untracked files
if [ -z "$(git status -s)" ]; then
  echo "No changes to commit."
  exit 0
fi
pause_with_progress 1

# Stage all changes, including new files
git add -A || handle_error "Failed to stage changes."
pause_with_progress 1

# Commit the changes with the provided message
git commit -m "$1" || handle_error "Failed to commit changes."
pause_with_progress 1

# Push the changes to the master branch on the remote repository
git push origin master || handle_error "Failed to push changes to master."
pause_with_progress 2

# Import the generated site to the gh-pages branch
ghp-import output -b gh-pages || handle_error "Failed to import to gh-pages branch."
pause_with_progress 1

# Push the gh-pages branch to the remote repository
git push origin gh-pages || handle_error "Failed to push gh-pages branch."
pause_with_progress 2

# Success message
echo "***********************"
echo "Site successfully deployed!"
echo "***********************"
