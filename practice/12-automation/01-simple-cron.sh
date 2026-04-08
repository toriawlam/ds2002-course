#!/usr/bin/env bash
#
# One-time setup:
#   chmod +x 01-simple-cron.sh
#
# Run manually to test:
#   ./01-simple-cron.sh
#
# Schedule with crontab (crontab -e). 
#
# Each run appends one line to runs.log

set -euo pipefail

log_dir="${HOME}/cron-demo"
mkdir -p "$log_dir"
# $$ is the process id of the current shell
printf '%s  01-simple-cron.sh executed (pid %s)\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$$" >> "${log_dir}/runs.log"

# Insert other commands here...