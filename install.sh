#!/bin/bash

set -euo pipefail

rm -f ~/bin/*
mkdir -p ~/bin 
cp -r scripts/*/* ~/bin/

(cd python; pip install -e .)

brew bundle

npm install -g asciicast2gif
