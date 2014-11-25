import  crowd
import os
import sys
import datetime
sys.path.insert(0,"/apps/product/tengine/html/zan")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")

app_url = 'http://sso.corp.ncfgroup.com/crowd/'
app_user = 'opuser'
app_pass = '3870032'
cs = crowd.CrowdServer(app_url, app_user, app_pass)
user_list=cs.get_nested_group_users(groupname="jira-users")
from django.contrib.auth.models import *
f=file("/opt/bin/crontab/sync_crowd.log","a")
for u in user_list:
    try:
        User.objects.get(username=u)
    except User.DoesNotExist,e:
        User.objects.create(username=u)
        day=datetime.datetime.now()
        f.write("%s %s is add\n"%(day,u))
f.write("%s sync crowd done\n"%datetime.datetime.now())
f.close()

