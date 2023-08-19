# tgcchinese.org

Data Security Management
- Data Backup & Disaster Recovery
  - Backup daily @4AM 
  - Stored at CF-R2 (7 days app stack, full site data)
  - Access via s3cmd
  - Notified https://t.me/tgccn_9marks_backup_notifier
- Server Security Operations

Site Availability Management
- Server & Uptime Monitoring
  - Server monitoring | ECS Dashboard (CPU/Memory/Storage/Network)
  - Uptime Global | https://stats.uptimerobot.com/KQoKF8D54
  - Uptime China | http://175.178.114.107:3001/status/tgc9marks
- Incident Response: < 8 hrs

Service Performance Management
- Routing Quality Monitoring
  - China Telecom http://175.178.114.107:59980/smokeping/?target=9MarksSites
  - China Unicom http://175.178.114.107:59982/smokeping/?target=9MarksSites
  - China Mobile http://175.178.114.107:59981/smokeping/?target=9MarksSites
- Performance & Error Logs
(Sentry)
