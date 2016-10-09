from slacker import Slacker
from apscheduler.schedulers.blocking import BlockingScheduler
import github3
import datetime
import pytz

sched = BlockingScheduler()
local_tz = pytz.timezone('Asia/Seoul')
token = 'xoxb-89187600885-A7V1hrwM8dBN4VKBYUp0wyLP'
slack = Slacker(token)
channels = ['#_general', '#announcements']

def post_to_channel(message):
    slack.chat.post_message(channels[0], message, as_user=False)

def get_repo_last_commit_delta_time(owner, repo):
    repo = github3.repository(owner, repo)
    return repo.pushed_at.astimezone(local_tz)

def get_delta_time(last_commit):
    now = datetime.datetime.now(local_tz)
    delta = now - last_commit
    return delta.days

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=21)
def main():
    members = (
        # (git 계정 이름, repo 이름, 이름),
        # [...]
        ('KangTrue','TMLgorithm','강진실'),
        ('maxtortime','TMLgorithm','김태환'),
        ('QBlek','TMLgorithm','한남규'),
        ('Rekdoll','TMLgorithm','현민성'),
        ('rerong','TMLgorithm','이상란'),
    )
    reports = []

    for owner, repo, name in members:
        last_commit = get_repo_last_commit_delta_time(owner, repo)
        delta_time = get_delta_time(last_commit)

        if(delta_time == 0):
            reports.append('*%s* 님은 오늘 커밋을 하셨어요!' % (name))
        else:
            reports.append('*%s* 님은 *%s* 일이나 커밋을 안하셨어요!' % (name, delta_time))

    post_to_channel('\n 안녕 친구들! 과제 점검하는 커밋벨이야 호호 \n' + '\n'.join(reports))


sched.start()

