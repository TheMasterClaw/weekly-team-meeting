#!/bin/bash
# Git credential helper for SEER
# Usage: git config credential.helper "/home/azureuser/.openclaw/workspace/git-credential-seer.sh"

if [ "$1" = "get" ]; then
    echo "username=TheeMasterClaw"
    echo "password=PLACEHOLDER_PAT"
fi
