#!/bin/bash

# Error handling
handle_error() {
  echo "🚨 Error: $1"
  exit 1
}

# Check commit message
if [ -z "$1" ]; then
  handle_error "Usage: $0 \"Your commit message\""
fi

# 1. Environment Setup ---------------------------------------------------
if [ -d "venv" ]; then
    source venv/bin/activate || handle_error "Virtualenv activation failed"
    echo "✓ Virtualenv activated"
else
    handle_error "Run 'python -m venv venv' first"
fi

# 2. Dependency Check (Only if requirements changed) ---------------------
# if [ requirements.txt -nt venv/.last_updated ] || [ ! -f venv/.last_updated ]; then
#    echo "🔄 Updating dependencies..."
#    pip install -r requirements.txt || handle_error "Dependency installation failed"
#    touch venv/.last_updated
#    echo "✓ Dependencies updated"
#else
#    echo "✓ Dependencies already current"
#fi

# 3. Source Code Management ----------------------------------------------
git checkout master || handle_error "Couldn't switch to master"
git pull origin master || handle_error "Couldn't pull latest changes"

# 4. Build Process ------------------------------------------------------
echo "🏗️  Building site..."
pelican content -s publishconf.py || handle_error "Build failed"

# 5. Source Commit (Only if changes exist) -------------------------------
if [ -n "$(git status --porcelain)" ]; then
    git add -A
    git commit -m "$1 [$(date +%Y-%m-%d)]" || handle_error "Commit failed"
    git push origin master || handle_error "Push to master failed"
    echo "✓ Source changes committed"
else
    echo "⏩ No source changes to commit"
fi

# 6. Deployment ---------------------------------------------------------
echo "🚀 Deploying to GitHub Pages..."
ghp-import output -b gh-pages -m "Deploy: $(date +'%Y-%m-%d %H:%M')"
git push origin gh-pages || handle_error "Deployment push failed"

echo "✅ Success! Your site is now live at https://netzro.github.io"