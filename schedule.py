from apscheduler.schedulers.blocking import BlockingScheduler

import tvmatchen, hltv
sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=24*3600) #every 24 hours
def tvmatchen_job():
    print('Fetching new data from Tvmatchen')
    tvmatchen.tvmatchen(False,True)

@sched.scheduled_job('interval', seconds=2*3600) #every 2 hours
def hltv_job():
    print('Fetching new data from HLTV')
    hltv.hltv(False, True)

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=10)
#def scheduled_job():
#    print('This job is run every weekday at 10am.')

sched.start()
