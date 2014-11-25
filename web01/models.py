#coding:utf8
from django.db import models

# Create your models here.
class Physical_Machine(models.Model):
    address=models.CharField(max_length=100,blank=True)
    sn=models.CharField(u'序列号',max_length=50,blank=True)
    hostname=models.CharField(u'主机名',max_length=50)
    ip=models.IPAddressField(blank=True)
    ilo_ip=models.IPAddressField(blank=True)
    ilo_user=models.CharField(max_length=30,blank=True)
    ilo_passwd=models.CharField(max_length=30,blank=True)
    cpu=models.CharField(max_length=30,blank=True)
    memory=models.CharField(max_length=30,blank=True)
    disk=models.CharField(max_length=30,blank=True)
    owner=models.CharField(max_length=30,blank=True)
    memo=models.TextField(u'备注')
    add_time=models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.ip
    class Meta:
        ordering=("address","ip","sn")
class VmInfo(models.Model):
    address=models.CharField(max_length=100,blank=True)
    os=models.CharField(u'操作系统',max_length=50)
    hostname=models.CharField(u'主机名',max_length=50)
    ip=models.IPAddressField(blank=True)
    cpu=models.CharField(max_length=30,blank=True)
    memory=models.CharField(max_length=30,blank=True)
    disk=models.CharField(max_length=30,blank=True)
    owner=models.CharField(max_length=30,blank=True)
    memo=models.TextField(u'备注')
    add_time=models.DateTimeField(auto_now=True)
    father=models.ForeignKey(Physical_Machine)
    def __unicode__(self):
        return "%s %s"%(self.ip,self.hostname)
    class Meta:
        db_table="jq"
        verbose_name='jqr'
        ordering=("father",)
