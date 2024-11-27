# Feierabenduhr

Create `config.json` in the script directory. The sample values of 480 and 510 correspond to 8 hours and 8,5 hours. This means that the Task Timer is set to 8,5 hours to display a closing time that would include 30 minutes of overtime.

Contents:

```json
{
    "awtrix_ip": "1.2.3.4",
    "WorkDuration": 480,
    "TaskTimerWorkDuration": 510
}
```