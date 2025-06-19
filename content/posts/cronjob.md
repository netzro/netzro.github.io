---
title: "Setting Up Cronie and Scheduling Scripts in Termux"
date: 2025-06-08
tags:
  - Termux
  - Cronie
description: "A step-by-step guide to installing cronie in Termux and scheduling scripts to run at specific times on Android."
---
### Setting Up Cronie and Scheduling Scripts in Termux

Cronie is a powerful tool for scheduling recurring tasks in Termux, allowing you to automate scripts on your Android device without root access. This guide walks you through installing cronie, setting up cron jobs, and managing them effectively, with examples tailored for Termux users.

### Why Use Cronie in Termux?
Cronie enables you to run scripts at specific times or intervals, perfect for tasks like backups, notifications, or syncing files. Unlike `termux-job-scheduler`, which is better for periodic tasks with Android-specific conditions (e.g., battery level), cronie offers precise, time-based scheduling similar to Linux cron. However, Android’s power management may kill Termux, so a wake lock is recommended.

### Prerequisites
- Termux installed from F-Droid (not Google Play Store).
- Scripts you want to schedule (e.g., Bash, Python) in a known path (e.g., `$HOME/scripts/`).
- Basic familiarity with Termux commands and a text editor like `nano` or `vi`.

### Step 1: Install Cronie and Termux-Services
1. Update Termux packages:
   ```
   pkg update && pkg upgrade
   ```
2. Install cronie and termux-services:
   ```
   pkg install cronie termux-services
   ```

## Step 2: Enable Cronie Service
Enable the crond daemon to run cron jobs:
```
sv-enable crond
```
If you see an error like “unable to change to service directory,” restart Termux and retry. Verify crond is running:
```
sv status crond
```

## Step 3: Create and Schedule Cron Jobs
1. Open the crontab editor:
   ```
   crontab -e
   ```
   This opens the default editor (usually `vi`). If you prefer `nano`, set it first:
   ```
   export EDITOR=nano
   crontab -e
   ```
2. Add cron job entries using the cron syntax: `minute hour day-of-month month day-of-week command`. For example:
   ```
   # Run a script every day at 8:00 AM
   0 8 * * * /data/data/com.termux/files/home/scripts/backup.sh

   # Run a Python script every Monday at 9:00 AM
   0 9 * * 1 /data/data/com.termux/files/usr/bin/python /data/data/com.termux/files/home/scripts/notify.py

   # Run a script every hour
   0 * * * * /data/data/com.termux/files/home/scripts/sync.sh
   ```
3. Save and exit (`:wq` in `vi`, or `Ctrl+O`, `Enter`, `Ctrl+X` in `nano`).
4. Verify cron jobs:
   ```
   crontab -l
   ```

## Example Scripts
### Backup Script (`backup.sh`)
Create a script to back up files:
```
#!/data/data/com.termux/files/usr/bin/bash
mkdir -p $HOME/backups
tar -czf $HOME/backups/backup-$(date +%F).tar.gz $HOME/storage/documents
```
Make it executable:
```
chmod +x $HOME/scripts/backup.sh
```
Schedule it to run daily at 8:00 AM:
```
0 8 * * * /data/data/com.termux/files/home/scripts/backup.sh
```

### Notification Script (`notify.py`)
Create a Python script to send a Termux notification:
```
#!/data/data/com.termux/files/usr/bin/python
import os
os.system('termux-notification -t "Weekly Reminder" -c "Time to review your goals!"')
```
Make it executable:
```
chmod +x $HOME/scripts/notify.py
```
Schedule it to run every Monday at 9:00 AM:
```
0 9 * * 1 /data/data/com.termux/files/usr/bin/python /data/data/com.termux/files/home/scripts/notify.py
```

## Step 4: Prevent Termux Termination
Android may kill Termux in the background, stopping cron jobs. To mitigate:
- **Acquire a Wake Lock**:
  ```
  termux-wake-lock
  ```
  Run this before starting crond to keep Termux active. Note: This may drain battery, so use sparingly.
- **Disable Battery Optimization**: Go to Android Settings > Apps > Termux > Battery > Disable optimization.
- **Optional: Termux:Boot**: Install Termux:Boot from F-Droid, enable it, and add `termux-wake-lock` to `$HOME/.termux/boot/` scripts to run on device startup.

## Troubleshooting
- **Cron Jobs Not Running**:
  - Check if crond is active: `sv status crond`.
  - Ensure script paths are absolute (e.g., `/data/data/com.termux/files/home/scripts/backup.sh`).
  - Verify script permissions: `ls -l $HOME/scripts/backup.sh` (should show `-rwxr-xr-x`).
- **Logs**: Check cron logs at `$PREFIX/var/log/sv/crond/current` for errors.
- **Termux Killed**: Re-run `termux-wake-lock` and `sv-enable crond` after app restarts.

## Cronie vs. Termux-Job-Scheduler
- **Cronie**: Best for precise, recurring schedules (e.g., daily at 8:00 AM). Requires Termux to stay active.
- **Termux-Job-Scheduler**: Better for periodic tasks with Android conditions (e.g., run when charging). Less precise but more battery-friendly. Example:
  ```
  termux-job-scheduler -s $HOME/scripts/backup.sh --period-ms 3600000
  ```

## Tips
- Use [crontab.guru](https://crontab.guru/) to craft cron schedules.
- Test scripts manually before scheduling: `bash $HOME/scripts/backup.sh`.
- Keep Termux open or use a wake lock for reliable cron execution.
- For one-time tasks, consider `at` (if available) or `termux-job-scheduler` with a script to check the date.

*Automate your tasks with cronie and take control of your Termux workflow!*[](https://www.reddit.com/r/termux/comments/i27szk/how_do_i_crontab_on_termux/)[](https://teddit.net/r/termux/comments/i27szk/)[](https://lotositsh.github.io/it/cron-termux.html)
