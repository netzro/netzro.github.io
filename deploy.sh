#!/bin/bash

# Error handling function
handle_error() {
  echo "Error: $1"
  exit 1
}

# Check commit message
if [ -z "$1" ]; then
  handle_error "No commit message provided. Usage: $0 <commit-message>"
fi

# Activate virtualenv
if [ -d "venv" ]; then
    source venv/bin/activate || handle_error "Failed to activate virtualenv"
else
    handle_error "Virtual environment (venv) not found"
fi

# Ensure dependencies
#pip install -r requirements.txt || handle_error "Failed to install dependencies"

# Switch to master
git checkout master || handle_error "Failed to switch to master branch."
git pull origin master || handle_error "Failed to pull latest changes"

# Build site with production settings
pelican content -s publishconf.py || handle_error "Pelican build failed"

# Commit source changes
if [ -z "$(git status -s)" ]; then
  echo "No changes to commit."
else
  git add -A || handle_error "Failed to stage changes."
  git commit -m "$1 - $(date '+%Y-%m-%d %H:%M')" || handle_error "Commit failed"
  git push origin master || handle_error "Failed to push to master"
fi

# Deploy to GitHub Pages
ghp-import output -b gh-pages -m "Deploy: $(date '+%Y-%m-%d %H:%M')" || handle_error "ghp-import failed"
git push origin gh-pages || handle_error "Failed to push gh-pages"

# Success message
echo "***************************************"
echo "  Site successfully deployed!          "
echo "  ➜ https://netzro.github.io          "
echo "***************************************"