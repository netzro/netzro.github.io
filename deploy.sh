#!/bin/bash

# Error handling
handle_error() {
  echo "Error: $1"
  exit 1
}

# Check commit message
[ -z "$1" ] && handle_error "Usage: $0 \"Your deploy message\""
[ ${#1} -lt 10 ] && handle_error "Commit message must be at least 10 characters long"

# Activate Virtualenv
if [ -d "venv" ]; then
  source venv/bin/activate
else
  read -p "No virtualenv found. Would you like to activate one? (y/n): " response
  if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
    read -p "Enter path to virtualenv activate script (e.g., /path/to/venv/bin/activate): " venv_path
    [ -f "$venv_path" ] && source "$venv_path" || handle_error "Invalid virtualenv path"
  else
    handle_error "Virtualenv required for Pelican build. Please create or activate one."
  fi
fi


# Build Process
pelican content -s publishconf.py || handle_error "Build failed"

# Source Commit (if changes exist)
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "$1 [$(date +%Y-%m-%d)]" || handle_error "Commit failed"
  git push origin master || handle_error "Push to master failed"
fi

# Clean output directory
rm -rf output/venv output/__pycache__ output/*.pyc 2>/dev/null

# Deployment
DEPLOY_HASH=$(git rev-parse --short HEAD)
DEPLOY_MSG="Deploy ${DEPLOY_HASH}: $(date +'%Y-%m-%d %H:%M') - $1"

ghp-import output -b gh-pages -m "$DEPLOY_MSG" -f || handle_error "Deployment failed"
git push origin gh-pages --force || handle_error "Deployment push failed"

echo "Success! Live at https://netzro.github.io"
echo "Deploy Message: $DEPLOY_MSG"