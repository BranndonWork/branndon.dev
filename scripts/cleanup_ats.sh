#!/bin/bash

# Cleanup temporary resume files after generation
# Usage: ./scripts/cleanup_ats.sh [file1] [file2] ...
# If no arguments provided, defaults to cleaning up the standard ATS file

# Move to trash function (macOS compatible)
trash_file() {
    if [ -f "$1" ]; then
        mv "$1" ~/.Trash/
        echo "✓ Moved to trash: $1"
        return 0
    else
        return 1
    fi
}

# Default file to clean
DEFAULT_ATS_FILE="webroot/branndon-coelho-resume-ats.json"

# If no arguments provided, use default
if [ $# -eq 0 ]; then
    FILES_TO_DELETE=("$DEFAULT_ATS_FILE")
else
    FILES_TO_DELETE=("$@")
fi

DELETED_COUNT=0
SKIPPED_COUNT=0

for FILE in "${FILES_TO_DELETE[@]}"; do
    if trash_file "$FILE"; then
        ((DELETED_COUNT++))
    else
        echo "✓ No file to clean: $FILE"
        ((SKIPPED_COUNT++))
    fi
done

if [ $DELETED_COUNT -gt 0 ]; then
    echo "✓ Moved $DELETED_COUNT file(s) to trash"
fi

if [ $SKIPPED_COUNT -gt 0 ]; then
    echo "✓ Skipped $SKIPPED_COUNT file(s) (not found)"
fi
