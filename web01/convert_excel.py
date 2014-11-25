#coding:utf-8

from pyExcelerator import *
from web01.models import *
import datetime

def format(x):
    if type(x) == float:
        return ("%.0f"%x)
    else:
        return x


def import_m(upfile,j,f):


    #excel row value
    y=range(12)
    #excel column value
    if len(j)%len(y):
        f.write("[%s] %s file has empty value \n"%(datetime.datetime.now(),upfile))
        return 0
    x=range(1,len(j)/len(y))

    for k in x:
        sn=format(j.get((k,0),""))
        hostname=format(j.get((k,1),""))
        ip=format(j.get((k,2),""))
        ilo_ip=format(j.get((k,3),""))
        ilo_user=format(j.get((k,4),""))
        ilo_passwd=format(j.get((k,5),""))
        cpu=format(j.get((k,6),""))
        memory=format(j.get((k,7),""))
        disk=format(j.get((k,8),""))
        owner=format(j.get((k,9),""))
        memo=format(j.get((k,10),""))
        address=format(j.get((k,11),""))

        m=Physical_Machine.objects.filter(sn=sn)
        if m:
            try:
                m.update(
sn=sn,
hostname=hostname,
ip=ip,
ilo_ip=ilo_ip,
ilo_user=ilo_user,
ilo_passwd=ilo_passwd,
cpu=cpu,
memory=memory,
disk=disk,
owner=owner,
memo=memo,
address=address,
)
            except BaseException,e:
                f.write("[%s] %s 第%s行 %s \n"%(datetime.datetime.now(),upfile,k,e))
                return 0
        else:  
            try:         
                Physical_Machine.objects.create(
sn=sn,
hostname=hostname,
ip=ip,
ilo_ip=ilo_ip,
ilo_user=ilo_user,
ilo_passwd=ilo_passwd,
cpu=cpu,
memory=memory,
disk=disk,
owner=owner,
memo=memo,
address=address,
)
            except BaseException,e:
                f.write("[%s] %s 第%s行 %s \n"%(datetime.datetime.now(),upfile,k,e))
                return 0
    return 1
def import_vm(upfile,j,f):



    #excel row value
    y=range(10)
    #excel column value
    if len(j)%len(y):
        f.write("[%s] %s file has empty value \n"%(datetime.datetime.now(),upfile))
        return 0
    x=range(1,len(j)/len(y))
    
    for k in x:
        f.write("[%s] %s 第%s行 processing \n"%(datetime.datetime.now(),upfile,k))
        father_ip=format(j.get((k,9),""))
        os=format(j.get((k,0),""))
        hostname=format(j.get((k,1),""))
        ip=format(j.get((k,2),""))
        cpu=format(j.get((k,3),""))
        memory=format(j.get((k,4),""))
        disk=format(j.get((k,5),""))
        owner=format(j.get((k,6),""))
        address=format(j.get((k,7),""))
        memo=format(j.get((k,8),""))
        if not father_ip:
            f.write("[%s] %s 第%s行 no father ip \n"%(datetime.datetime.now(),upfile,k))
            return 0
        father=Physical_Machine.objects.filter(ip=father_ip)
        if not father:
            f.write("[%s] %s 第%s行 找不到father ip \n"%(datetime.datetime.now(),upfile,k))
            return 0
        else:
            father=father[0]
        m=VmInfo.objects.filter(father=father,os=os,hostname=hostname,ip=ip,cpu=cpu,memory=memory,disk=disk,owner=owner,address=address,memo=memo)
        if m:
            try:
                m.update(
os=os,
hostname=hostname,
ip=ip,
cpu=cpu,
memory=memory,
disk=disk,
owner=owner,
address=address,
memo=memo,
father=father,
)   
            except BaseException,e:
                f.write("[%s] %s 第%s行 %s \n"%(datetime.datetime.now(),upfile,k,e))
                return 0
        else:
            try:
                VmInfo.objects.create(
os=os,
hostname=hostname,
ip=ip,
cpu=cpu,
memory=memory,
disk=disk,
owner=owner,
address=address,
memo=memo,
father=father,
)
            except BaseException,e:
                f.write("[%s] %s 第%s行 %s \n"%(datetime.datetime.now(),upfile,k,e))
                return 0
    return 1
def import_info(upfile):

    f=file("/tmp/parse.log","a")
    try:

        sheets = parse_xls(upfile)

        #sheets[0] is the first sheet
        #sheetName is sheet name,j is dict
        sheetName,j=sheets[0]
        if sheetName=="host":
            ret=import_m(upfile,j,f)    
            return ret
        elif sheetName=="vm":
            ret=import_vm(upfile,j,f)
            return ret
        else:
            f.write("[%s] %s sheetName is unknown \n"%(datetime.datetime.now(),upfile))     
            f.close()
            return 0
    except BaseException,e:
        f.write("[%s] %s %s \n"%(datetime.datetime.now(),upfile,e))
    finally:
        f.close()
