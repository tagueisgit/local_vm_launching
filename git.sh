#!/bin/bash

# Prompt for commit message
read -p "What is your message? " message
echo "You entered: $message"

# Ensure you're in a git repo
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Git repository confirmed."
else
    echo "Error: not a git repository."
    exit 1
fi

# Ensure you're on the right branch (change 'main_v1' to your branch name)
git checkout main_v1 || { echo 'Checkout failed'; exit 1; }

# Pull the latest changes from the remote branch
git pull origin main_v1 || { echo 'git pull failed'; exit 1; }

# Check for changes and commit them
if [ -z "$(git status --porcelain)" ]; then
    echo "No changes to commit."
else
    # Add all changes to staging
    git add . || { echo 'git add failed'; exit 1; }
    
    # Commit the changes
    git commit -m "$message" || { echo 'git commit failed'; exit 1; }
    
    # Push the changes to the remote repository
    git push origin main_v1 || { echo 'git push failed'; exit 1; }
fi

echo "Script completed."

