#!/bin/bash

set -euo pipefail

rm -f ~/bin/*
mkdir ~/bin 
cp -r scripts/*/* ~/bin/
