#!/bin/bash

set -euo pipefail

# Plain shell scripts
rm -f ~/bin/*
mkdir -p ~/bin 
cp -r scripts/*/* ~/bin/

# My python package
(cd python; pip install -e .)

# Homebrew
brew bundle

# Node deps
npm install -g asciicast2gif

# Gemfile
bundle install --system
