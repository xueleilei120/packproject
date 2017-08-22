# _*_ encoding=utf-8 _*_
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class PackType(models.Model):
    """
    打包类型：如 客户端 client或server
    """
    type_name = models.CharField(default="", max_length=20, verbose_name=u"类型名称")

    class Meta:
        verbose_name = u"打包类型"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.type_name


class Node(models.Model):
    nick_name = models.CharField(default="", max_length=200, blank=True, null=True, verbose_name=u"包昵称")
    svn_path = models.CharField(default="", max_length=200, blank=True, null=True, verbose_name=u"svn路径")
    local_path = models.CharField(default="", max_length=200, blank=True, null=True, verbose_name=u"本地路径")
    pack_type = models.ForeignKey(PackType)

    class Meta:
        verbose_name = u"包节点"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.nick_name
