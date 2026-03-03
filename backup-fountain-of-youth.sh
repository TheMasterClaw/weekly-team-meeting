#!/bin/bash
# Daily backup script for fountain-of-youth repository
# Runs at 04:20 UTC daily
# Commits any local changes and pulls latest from origin

REPO_DIR="/home/azureuser/.openclaw/workspace/backups/fountain-of-youth"
BACKUP_LOG="/home/azureuser/.openclaw/workspace/backups/fountain-of-youth-backup.log"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

echo "[$TIMESTAMP] Starting fountain-of-youth backup..." >> "$BACKUP_LOG"

cd "$REPO_DIR" || exit 1

# Configure git user for commits
git config user.email "seer-backup@swarm.local"
git config user.name "SEER Backup Bot"

# Check if there are local changes to commit
if [ -n "$(git status --porcelain)" ]; then
    echo "[$TIMESTAMP] Local changes detected, committing..." >> "$BACKUP_LOG"
    git add -A
    git commit -m "Auto-backup: $TIMESTAMP" >> "$BACKUP_LOG" 2>&1
fi

# Pull latest changes from origin
echo "[$TIMESTAMP] Pulling latest from origin..." >> "$BACKUP_LOG"
git pull origin main >> "$BACKUP_LOG" 2>&1 || git pull origin master >> "$BACKUP_LOG" 2>&1

# Push any local commits
echo "[$TIMESTAMP] Pushing to origin..." >> "$BACKUP_LOG"
git push origin >> "$BACKUP_LOG" 2>&1

echo "[$TIMESTAMP] Backup complete." >> "$BACKUP_LOG"
echo "---" >> "$BACKUP_LOG"
