#!/bin/bash

set -euo pipefail

rm -f ~/bin/*
mkdir -p ~/bin 
cp -r scripts/*/* ~/bin/
