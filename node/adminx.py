#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liuyc
@file: adminx.py
@time: 2017/1/6 22:12
@describe:
"""
import xadmin
from xadmin import views

from .models import Node, PackType

class PackTypeAdmin(object):
    list_display = ['type_name']
    # 后台要搜索的字段
    search_fields = ['type_name']
    # 后台过滤器
    list_filter = ['type_name']

class NodeAdmin(object):
    # 后台中点击邮箱验证码 要显示的字段
    list_display = ['nick_name', 'svn_path', 'local_path']
    # 后台要搜索的字段
    search_fields = ['nick_name', 'svn_path', 'local_path']
    # 后台过滤器
    list_filter = ['nick_name', 'svn_path', 'local_path']
    # 打包按钮显示在local_path的后面
    show_pack_btn_fields = ['local_path']

class BaseSetting(object):
    # 要使用主题功能
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = "游戏打包管理系统"
    site_footer = "我的公司"

xadmin.site.register(Node, NodeAdmin)
xadmin.site.register(PackType, PackTypeAdmin)
# xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

