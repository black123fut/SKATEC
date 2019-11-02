from crontab import CronTab

cron = CronTab(user=True)
job = cron.new(command='python3 CierreCaja.py')
job.minute.on(20)
job.hour.on(4)

cron.write()
