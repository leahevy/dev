#!/bin/bash

OIFS="$IFS"
IFS=$'\n'
for file in `find "$1" -type d` ; do
    if [[ ! -d "$file/.git" ]]; then
        continue
    fi
    (cd "$file"; git cherry -v 2>/dev/null)
    if [[ ! -z $(cd "$file"; git status -s) ]]; then
        echo "Uncommited changes: $file"
    fi

done
IFS="$OIFS"