from django.conf.urls import patterns, include, url
from web01 import views as v
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^accounts/login/$', v.logins),
    url(r'^logout/$', v.logouts),
    url(r'^dologin/$',v.dologin),
    url(r'^info/$',v.info),
    url(r'^vminfo/$',v.vminfo),
    url(r'^detail/$',v.detail),
    url(r'^detail_vm/$',v.detail_vm),
    url(r'^save/$',v.save),
    url(r'^save_vm/$',v.save_vm),
    url(r'^add/$',v.add),
    url(r'^addvm/$',v.addvm),
    url(r'^dels/$',v.dels),
    url(r'^fupload/$',v.fupload),
    url(r'^fread/$',v.fread),
    url(r'^fdownload/$',v.fdownload),
    url(r'^search/$',v.search),
    url(r'^search_vm/$',v.search_vm),
    url(r'^users/$',v.users),
    url(r'^user/$',v.user),
    url(r'^addGroup/$',v.addGroup),
    url(r'^bs/$',v.bs),

)





