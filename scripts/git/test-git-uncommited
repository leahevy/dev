#!/bin/bash

ROOTDIR="$1"
if [[ "$ROOTDIR" == "" ]]; then
	ROOTDIR="$HOME/Source/"
fi

OIFS="$IFS"
IFS=$'\n'
for file in `find "$ROOTDIR" -type d` ; do
    if [[ ! -d "$file/.git" ]]; then
        continue
    fi
    if [[ ! -z $(cd "$file"; git status -s) ]]; then
        echo "Uncommited changes: $file"
    fi
    if [[ ! -z $(cd "$file"; git cherry -v 2>/dev/null) ]]; then
        echo "Unpushed changes: $file"
    fi
done
IFS="$OIFS"