#!/usr/bin/env bash
source ./util.sh

info_message "Installing Requirements"
poetry install

info_message "Installing pre-commit"
pre-commit install --hook-type commit-msg


success_message "Build Done!"
