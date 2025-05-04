#!/bin/bash

# Error handling
handle_error() {
  echo "Error: $1"
  exit 1
}

# Check commit message
[ -z "$1" ] && handle_error "Usage: $0 \"Your deploy message\""

# Activate Virtualenv (if exists)
[ -d "venv" ] && source venv/bin/activate

# Source Code Management
git checkout master || handle_error "Couldn't switch to master"
git pull origin master || handle_error "Couldn't pull latest changes"

# Build Process
pelican content -s publishconf.py || handle_error "Build failed"

# Source Commit (if changes exist)
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "$1 [$(date +%Y-%m-%d)]" || handle_error "Commit failed"
  git push origin master || handle_error "Push to master failed"
fi

# Deployment
DEPLOY_HASH=$(git rev-parse --short HEAD)
DEPLOY_MSG="Deploy ${DEPLOY_HASH}: $(date +'%Y-%m-%d %H:%M') - $1"

ghp-import output -b gh-pages -m "$DEPLOY_MSG" -f || handle_error "Deployment failed"
git push origin gh-pages --force || handle_error "Deployment push failed"

echo "Success! Live at https://netzro.github.io"
echo "Deploy Message: $DEPLOY_MSG"