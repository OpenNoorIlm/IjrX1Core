#!/bin/bash
set -e  # Exit immediately if any command fails

# Default values (adjust these to your paths)
DEFAULT_SOURCE="/home/bismillah/Downloads/Ijr-X1-Core"
DEFAULT_DEST="/home/bismillah/Downloads/IjrX1Core"
DEFAULT_MSG="Some updates1"

# Use command-line arguments or fallback to defaults
SOURCE="${1:-$DEFAULT_SOURCE}"
DEST="${2:-$DEFAULT_DEST}"
MSG="${3:-$DEFAULT_MSG}"

# Validate directories
if [ ! -d "$SOURCE" ]; then
    echo "Error: Source directory '$SOURCE' does not exist."
    exit 1
fi
if [ ! -d "$DEST" ]; then
    echo "Error: Destination directory '$DEST' does not exist."
    exit 1
fi
if [ ! -d "$DEST/.git" ]; then
    echo "Error: '$DEST' is not a Git repository (no .git folder)."
    exit 1
fi

# Sync files (trailing slashes copy contents, not the folder itself)
echo "Syncing from '$SOURCE' to '$DEST' ..."
rsync -av "$SOURCE"/ "$DEST"/

# Stage all changes
echo "Staging changes in '$DEST' ..."
git -C "$DEST" add .

# Commit with the given message
echo "Committing with message: '$MSG'"
git -C "$DEST" commit -m "$MSG"

# Push to remote main branch
echo "Pushing to origin main ..."
git -C "$DEST" push origin main

echo "All done!"
