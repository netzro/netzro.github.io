#!/bin/bash

# Error handling
handle_error() {
  echo "Error: $1"
  exit 1
}

# Check commit message
[ -z "$1" ] && handle_error "Usage: $0 \"Your deploy message\""
[ ${#1} -lt 10 ] && handle_error "Commit message must be at least 10 characters long"

# Build Process - show output and capture it
BUILD_OUTPUT=$(uv run pelican content -s publishconf.py 2>&1 | tee /dev/tty)
BUILD_STATUS=${PIPESTATUS[0]}
if [ $BUILD_STATUS -ne 0 ]; then
  handle_error "Build failed"
fi

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
DEPLOY_MSG="Deploy ${DEPLOY_HASH}: $(date +'%Y-%m-%d %H:%M') - $1

$BUILD_OUTPUT

Live at https://netzro.github.io"

uv run ghp-import output -b gh-pages -m "$DEPLOY_MSG" -f || handle_error "Deployment failed"
git push origin gh-pages --force || handle_error "Deployment push failed"

echo "Success! Deploy Message:
$DEPLOY_MSG"