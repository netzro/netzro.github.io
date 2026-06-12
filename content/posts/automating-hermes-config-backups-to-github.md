Title: Automating Hermes Agent Configuration Backups to GitHub
Date: 2026-06-10
Author: Gifted
Category: Tech
Tags: ai, development, technology
Slug: automating-hermes-config-backups-to-github
Status: published
Summary: How I set up automated daily backups of my Hermes agent configuration to a private GitHub repository using cron jobs and custom scripts.

As my Hermes agent setup has grown more complex with custom skills, memories, and configurations, I realized I needed a reliable backup system. Losing my agent's learned memories or carefully crafted skills would be a significant setback. Here's how I implemented automated daily backups to GitHub.

## The Challenge

Hermes stores all its configuration in `~/.hermes/`, including:
- `config.yaml` - Main configuration file
- `SOUL.md` - Personal notes and reflections
- `memories/` - User and agent memories
- `skills/` - Custom skills and skill collections
- `cron/` - Scheduled jobs and their outputs

Manually backing this up was error-prone and I often forgot. I needed an automated solution that would run reliably without my intervention.

## The Solution

I created a three-part system:

### 1. Private GitHub Repository
First, I created a private repository `netzro/hermes-config-backup` to store the backups securely.

### 2. Backup Script
I wrote a bash script that:
- Clones or pulls the backup repository
- Copies the essential Hermes configuration files and directories
- Commits changes with a timestamp
- Pushes to GitHub
- Logs all operations for monitoring

The script specifically backs up:
- `config.yaml` (excluding `.env` for security)
- `SOUL.md`
- `memories/` directory
- `skills/` directory  
- `cron/` directory

### 3. Automated Scheduling
Using Hermes' built-in cron system, I scheduled the backup script to run daily at 2:00 AM.

## Key Features

**Selective Backups**: Only backs up configuration and data, excluding large caches and temporary files.

**Timestamped Commits**: Each backup commit includes the exact timestamp: "Agent backup YYYY-MM-DD HH:MM:SS"

**Error Handling**: The script exits on any error and logs detailed output.

**Efficient**: Only commits and pushes when there are actual changes.

## The Cron Job

I configured a Hermes cron job with:
- Schedule: `0 2 * * *` (daily at 2:00 AM)
- Workdir: `/data/data/com.termux/files/home/workspace` 
- Toolsets: terminal (for git operations)
- Delivery: local (logs stored in ~/.hermes/logs/backup.log)

## Results

Since implementation, the system has been running flawlessly:
- Daily backups occur without manual intervention
- The GitHub repository shows a clear history of configuration changes
- I can easily roll back to any previous state if needed
- Peace of mind knowing my agent's learned state is preserved

## Lessons Learned

1. **Security First**: Always exclude sensitive files like `.env` containing API keys
2. **Logging Matters**: Detailed logs make troubleshooting much easier
3. **Test Thoroughly**: Test the backup script manually before automating it
4. **Monitor Regularly**: Check the logs and GitHub repository periodically to ensure everything works

This backup system gives me confidence to continue experimenting with my Hermes agent, knowing that I can always recover to a previous working state if something goes wrong.

The setup took about an hour to implement but will save countless hours of potential rework and frustration. Sometimes the best productivity tools are the ones that protect your existing work.