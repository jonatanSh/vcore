#!/usr/bin/env bash

./build.sh

sudo pip3 uninstall vcore_api

sudo pip3 install $(find dist/ -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" ")