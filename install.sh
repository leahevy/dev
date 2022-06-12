#!/bin/bash

set -euo pipefail

# Plain shell scripts
rm -f ~/dev/*
mkdir -p ~/dev 
cp -r scripts/*/* ~/dev/

# My python package
(cd python; pip install -e .)

# Homebrew
brew bundle

# Node deps
npm install -g asciicast2gif

# Gemfile
bundle install --system
