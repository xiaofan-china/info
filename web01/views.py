#coding:utf-8
from django.shortcuts import *
from django.http import *
from web01.models import *
from web01.decorators import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate,login,logout
import crowd
from convert_excel import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import csv
import codecs
import datetime
# Create your views here.
class Myauth(ModelBackend):
    def authenticate(self,username,password):
        app_url = 'http://xxxx.com/crowd/'
        app_user = '123'
        app_pass = '123'
        user=None    
            
        cs = crowd.CrowdServer(app_url, app_user, app_pass)
        success = cs.auth_user(username, password)
        if success:
            if not User.objects.filter(username=username):
                User.objects.create(username=username)
            user=User.objects.get(username=username)
        return user
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
def logins(req):
    next=req.GET.get("next")
    return render_to_response("login.html",locals(),RequestContext(req))
def logouts(req):
    logout(req)
    return HttpResponseRedirect("/accounts/login/",RequestContext(req)) 

def dologin(req):
    next=req.GET.get("next","/info/")
    user=req.POST.get('user')
    passwd=req.POST.get('passwd')
    user=authenticate(username=user,password=passwd)
    if user:
        login(req,user)
        return HttpResponseRedirect("%s"%next)
    return render_to_response("dologin.html",locals())
def pages(count,page_len,page):
#count 总条目数
#page_len 每页条目
#page raw current page
    pageNum=(count+page_len-1)/page_len
    try:
        page=eval(page)
    except Exception,e:
        pass
    if type(page)!=int:
        page=0
    elif pageNum==0:
        page=0
    elif (page+1)>pageNum:
        page=pageNum-1
    elif page <0:
        page=0
    if page==0:
        prePage=False
    else:
        prePage=True
    if pageNum>(page+1):
        nextPage=True
    else:
        nextPage=False
    return page,prePage,nextPage 
@login_required
def info(req):
    count=Physical_Machine.objects.count()
    page_len=20
    page=req.GET.get("page","0")
    page,prePage,nextPage=pages(count,page_len,page)        

    machines=Physical_Machine.objects.all()[page*page_len:(page+1)*page_len]
    return render_to_response("info.html",locals(),RequestContext(req))
@login_required
def vminfo(req):
    vmlist=[]
    count=0
    m_count=0
    page_len=10
    page=req.GET.get("page")
    machines=Physical_Machine.objects.all()
    for m in machines:
        vm=m.vminfo_set.all() 
        if vm:
            count+=len(vm)
            m_count+=1
            vmlist.append([m,vm])
    page,prePage,nextPage=pages(m_count,page_len,page)
    vmlist=vmlist[page*page_len:(page+1)*page_len]
    return render_to_response("vminfo.html",locals(),RequestContext(req))
@login_required
@sys_required
def detail(req):
    id=req.GET.get("dog")
    success=req.GET.get("success",0)
    if id:
        id=int(id)
        m_list=Physical_Machine.objects.filter(id=id)
        if m_list:
            m=m_list[0]
            return render_to_response("views.html",locals(),RequestContext(req))
    return HttpResponseRedirect("/")
@login_required
@sys_required
def detail_vm(req):
    id=req.GET.get("cat")
    father_error=req.GET.get("father_error")
    success=req.GET.get("success",0)
    if id:
        id=int(id)
        vm_list=VmInfo.objects.filter(id=id)
        if vm_list:
            vm=vm_list[0]
            return render_to_response("views_vm.html",locals(),RequestContext(req))
    return HttpResponseRedirect("/")
@login_required
@sys_required
def save(req):
    success=1
    if req.method!="POST":
        return HttpResponseRedirect("/")  
    id=req.POST.get('dog',"")
    address=req.POST.get('address',"")[:100]
    sn=req.POST.get('sn',"")[:50]
    hostname=req.POST.get("hostname","")[:50]
    ip=req.POST.get("ip","")[:15]
    ilo_ip=req.POST.get("ilo_ip","")[:15]
    ilo_user=req.POST.get("ilo_user","")[:30]
    ilo_passwd=req.POST.get("ilo_passwd","")[:30]
    cpu=req.POST.get("cpu","")[:30]
    memory=req.POST.get("memory","")[:30]
    disk=req.POST.get("disk","")[:30]
    owner=req.POST.get("owner","")[:30]
    memo=req.POST.get("memo","")
    if id:
        id=int(id)
        try:
            m=Physical_Machine.objects.get(id=id)
            m.address=address
            m.sn=sn
            m.hostname=hostname
            m.ip=ip
            m.ilo_ip=ilo_ip
            m.ilo_user=ilo_user
            m.ilo_passwd=ilo_passwd
            m.cpu=cpu
            m.memory=memory
            m.disk=disk
            m.owner=owner
            m.memo=memo
            m.save()
        except Exception,e:
            success=2
        return HttpResponseRedirect("/detail/?dog=%s&success=%s"%(id,success)) 
           
    return HttpResponseRedirect("/")
@login_required
@sys_required
def save_vm(req):
    success=1
    if req.method!="POST":
        return HttpResponseRedirect("/")
    id=req.POST.get('cat',"")
    address=req.POST.get('address',"")[:100]
    os=req.POST.get('os',"")[:50]
    hostname=req.POST.get("hostname","")[:50]
    ip=req.POST.get("ip","")[:15]
    cpu=req.POST.get("cpu","")[:30]
    memory=req.POST.get("memory","")[:30]
    disk=req.POST.get("disk","")[:30]
    owner=req.POST.get("owner","")[:30]
    memo=req.POST.get("memo","")
    father_ip=req.POST.get("father_ip","")
    father=Physical_Machine.objects.filter(ip=father_ip)
    if not father:
        father_error=1
        return HttpResponseRedirect("/detail_vm/?cat=%s&father_error=%s"%(id,father_error))
    else:
        father=father[0]
    if id:
        id=int(id)
        vm_list=VmInfo.objects.filter(id=id)
        if vm_list:
            try:
                vm=vm_list[0] 
                vm.address=address
                vm.os=os
                vm.hostname=hostname
                vm.ip=ip
                vm.cpu=cpu
                vm.memory=memory
                vm.disk=disk
                vm.owner=owner
                vm.memo=memo
                vm.father=father
                vm.save()
            except Exception,e:
                success=2
            return HttpResponseRedirect("/detail_vm/?cat=%s&success=%s"%(id,success))

    return HttpResponseRedirect("/")
@login_required
@sys_required
def add(req):
    if req.method=="POST":
        return HttpResponse("ok")
    else:
        return render_to_response("add.html",locals(),RequestContext(req))
@login_required
@sys_required
def addvm(req):
    if  req.method=="POST":
        return HttpResponse("ok")
    else:
        return render_to_response("add.html",locals(),RequestContext(req))
@login_required
@sys_required
def dels(req):
    dog=req.GET.get("dog","")
    if not dog:
        cat=req.GET.get("cat","")
        if not cat:
            return HttpResponseRedirect("/")
        try:
            vm=VmInfo.objects.get(id=cat)
            vm.delete()
        except:
            pass
        return HttpResponseRedirect("/vminfo")
    else:
        try:
            m=Physical_Machine.objects.get(id=dog)    
            m.delete()
        except:
            pass
        return HttpResponseRedirect("/info")
@login_required
@sys_required
def fupload(req):
    return render_to_response("fupload.html",locals(),RequestContext(req))

@login_required
@sys_required
def fdownload(req):
    if req.method !="POST":
        return render_to_response("fdownload.html",locals(),RequestContext(req))
    else:
        f=file("/opt/bin/crontab/download.log","w")
        target=req.POST.get("target","host")
        response=HttpResponse(mimetype='text/csv')
        if target == "host":
            response['Content-Disposition'] = 'attachment; filename=host.csv' 
            response.write(u'\ufeff')
            writer = csv.writer(response,dialect='excel')
            host=Physical_Machine.objects.all()    
            try:
                for i in host:
                    writer.writerow(
[i.address.encode("gb2312"),
i.sn.encode("gb2312"),
i.hostname.encode("gb2312"),
i.ip.encode("gb2312"),
i.ilo_ip.encode("gb2312"),
i.ilo_user.encode("gb2312"),
i.ilo_passwd.encode("gb2312"),
i.cpu.encode("gb2312"),
i.memory.encode("gb2312"),
i.disk.encode("gb2312"),
i.owner.encode("gb2312"),
i.memo.encode("gb2312"),
i.add_time])   
            except Exception,e:
                f.write("%s %s \n"%(datetime.datetime.now(),e))
                response=HttpResponse("download error,please contact admin!")
            finally:
                f.close()
        elif target=="vm":
            response['Content-Disposition'] = 'attachment; filename=vm.csv'
            response.write(u'\ufeff')
            writer = csv.writer(response,dialect='excel')
            vm=VmInfo.objects.all()
            try:
                for i in vm:
                    writer.writerow(
[i.address.encode("gb2312"),
i.os,i.hostname.encode("gb2312"),
i.ip,i.cpu.encode("gb2312"),
i.memory.encode("gb2312"),
i.disk.encode("gb2312"),
i.owner.encode("gb2312"),
i.memo.encode("gb2312"),
i.add_time,
i.father.ip])
            except Exception,e:
                f.write("%s %s \n"%(datetime.datetime.now(),e))
                response=HttpResponse("download error,please contact admin!")
            finally:
                f.close()
        return response

@login_required
def search(req):
    field_list=['all','address','sn','hostname','ip','ilo_ip','cpu','memory','disk','owner','memo']
    field=req.GET.get("field","all")
    if field not in field_list:
        field="all"
    name=req.GET.get("monkey","")
    if field == "all": 
        machines=Physical_Machine.objects.filter(
Q(address__icontains=name)|
Q(sn__icontains=name)|
Q(hostname__icontains=name)|
Q(ip__icontains=name)|
Q(ilo_ip__icontains=name)|
Q(ilo_user__icontains=name)|
Q(ilo_passwd__icontains=name)|
Q(cpu__icontains=name)|
Q(memory__icontains=name)|
Q(disk__icontains=name)|
Q(owner__icontains=name)|
Q(memo__icontains=name)
)
    
        count=len(machines) 
    elif field=="address":        
        machines=Physical_Machine.objects.filter(address__icontains=name)
        count=len(machines)
    elif field=="sn":
        machines=Physical_Machine.objects.filter(sn__icontains=name)
        count=len(machines)
    elif field=="hostname":
        machines=Physical_Machine.objects.filter(hostname__icontains=name)
        count=len(machines)
    elif field=="ip":
        machines=Physical_Machine.objects.filter(ip__icontains=name)
        count=len(machines)
    elif field=="ilo_ip":
        machines=Physical_Machine.objects.filter(ilo_ip__icontains=name)
        count=len(machines)
    elif field=="cpu":
        machines=Physical_Machine.objects.filter(cpu__icontains=name)
        count=len(machines)
    elif field=="memory":
        machines=Physical_Machine.objects.filter(memory__icontains=name)
        count=len(machines)
    elif field=="disk":
        machines=Physical_Machine.objects.filter(disk__icontains=name)
        count=len(machines)
    elif field=="owner":
        machines=Physical_Machine.objects.filter(owner__icontains=name)
        count=len(machines)
    elif field=="memo":
        machines=Physical_Machine.objects.filter(memo__icontains=name)
        count=len(machines)    
    page_len=20
    page=req.GET.get("page","0")
    page,prePage,nextPage=pages(count,page_len,page)
    machines=machines[page*page_len:(page+1)*page_len]
    return render_to_response("search.html",locals(),RequestContext(req)) 

@login_required
def search_vm(req):
    field_list=['all','address','os','hostname','ip','cpu','memory','disk','owner','memo','father']
    field=req.GET.get("field","all")
    if field not in field_list:
        field="all"
    name=req.GET.get("fish","")
    if  field=="all":
        machines=VmInfo.objects.filter(
Q(address__icontains=name)|
Q(os__icontains=name)|
Q(hostname__icontains=name)|
Q(ip__icontains=name)|
Q(cpu__icontains=name)|
Q(memory__icontains=name)|
Q(disk__icontains=name)|
Q(owner__icontains=name)|
Q(memo__icontains=name)
)

        count=len(machines)
    elif field=="father": 
        page_len=10
        m_list=Physical_Machine.objects.filter(ip__icontains=name)
        vmlist=[]
        count=0
        m_count=0
        if m_list:
            for m in m_list:
                vm=m.vminfo_set.all() 
                if vm:
                    count+=len(vm)
                    m_count+=1
                    vmlist.append([m,vm])
            page=req.GET.get("page","0")
            page,prePage,nextPage=pages(m_count,page_len,page)
            vmlist=vmlist[page*page_len:(page+1)*page_len]
        return render_to_response("vm_father_search.html",locals(),RequestContext(req))
    elif field=="address":
        machines=VmInfo.objects.filter(address__icontains=name)
        count=len(machines)
    elif field=="os":
        machines=VmInfo.objects.filter(os__icontains=name)
        count=len(machines)
    elif field=="hostname":
        machines=VmInfo.objects.filter(hostname__icontains=name)
        count=len(machines)
    elif field=="ip":
        machines=VmInfo.objects.filter(ip__icontains=name)
        count=len(machines)
    elif field=="cpu":
        machines=VmInfo.objects.filter(cpu__icontains=name)
        count=len(machines)
    elif field=="memory":
        machines=VmInfo.objects.filter(memory__icontains=name)
        count=len(machines)
    elif field=="disk":
        machines=VmInfo.objects.filter(disk__icontains=name)
        count=len(machines)
    elif field=="owner":
        machines=VmInfo.objects.filter(owner__icontains=name)
        count=len(machines)
    elif field=="memo":
        machines=VmInfo.objects.filter(memo__icontains=name)
        count=len(machines)
    page=req.GET.get("page","0")
    page_len=20
    page,prePage,nextPage=pages(count,page_len,page)
    machines=machines.all()[page*page_len:(page+1)*page_len]
    return render_to_response("vm_search.html",locals(),RequestContext(req))

@login_required
@csrf_exempt
def fread(req):
    #return render_to_response("fupload.html",locals(),RequestContext(req))
    f=req.FILES.get("file")
    if f:
        filename="/tmp/"+str(req.user)+"_"+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".xls"
        w=file(filename,"w")
        w.write(f.read())
        w.close()
        if import_info(filename):
            return HttpResponse("ok")
        else:
            return HttpResponseNotFound()
    else:
        return HttpResponseNotFound()

@login_required
@sys_required
def users(req):
    u_list=User.objects.all()
    count=User.objects.count()

    page_len=20
    page=req.GET.get("page","0")
    page,prePage,nextPage=pages(count,page_len,page)
    u_list=u_list[page*page_len:(page+1)*page_len]
    return render_to_response("users.html",locals(),RequestContext(req))

@login_required
@sys_required
def user(req):
    success=False
    if req.method=="POST":
        usr=req.POST.get("user","") 
        if usr:
            try:
                u=User.objects.get(username=usr)
                groups=req.POST.getlist("groups")
                for g in u.groups.all():
                    u.groups.remove(g)
                for new in groups:
                    g=Group.objects.get(name=new)
                    u.groups.add(g)
                groups=Group.objects.all()
                success=True
                return render_to_response("user.html",locals(),RequestContext(req))
            except User.DoesNotExist,e:
                raise Http404
            except Group.DoesNotExist,e:
                raise Http404
        else:
            raise Http404
    else:
        usr=req.GET.get("user","")
        if usr:
            try:
                u=User.objects.get(username=usr)
                groups=Group.objects.all()
                return render_to_response("user.html",locals(),RequestContext(req))
            except User.DoesNotExist,e:
                raise Http404
                
        else:
            return HttpResponseRedirect("/")
@login_required
@sys_required
def addGroup(req):
    user=req.GET.get("user","someone")
    
    return render_to_response("addGroup.html",locals(),RequestContext(req))

def bs(req):
    return render_to_response("bs.html")
