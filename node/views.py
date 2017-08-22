# -*- coding: utf-8 -*-
from django.shortcuts import render


from django.views.generic.base import View
from django.views.static import serve
from django.http import HttpResponseNotFound


from node.models import Node
from PackScrips.MakePack import MakePackSvrGame

# Create your views here.

class PackView(View):
    """
    课程详情页
    """
    def get(self, request, node_id):
        node_obj = Node.objects.get(id=int(node_id))
        nick_name = node_obj.nick_name
        svn_path = node_obj.svn_path
        local_path = node_obj.local_path
        pack_type = node_obj.pack_type

        make_pack_obj = None
        # 判断是打包类型 client or server
        if pack_type == "client":
            pass
        else:
            # 服务器打包
            make_pack_obj = MakePackSvrGame()

        # zip文件路径
        zip_path, zip_name = make_pack_obj.Doit(svn_path, local_path, nick_name)
        print("zip_name:", zip_name)
        print("zip_path:", zip_path)
        if zip_path == "" or zip_name == "":
            print("Error: MakePackSvrGame zip_path error")
            return HttpResponseNotFound("MakePackSvrGame zip_path={0} or zip_path={1}  error".format(zip_name, zip_path))

        # DownLadTemplate
        response_temp = serve(request, zip_name, document_root=zip_path)
        response_temp['Content-Disposition'] = 'attachment; filename=%s' % zip_name
        return response_temp

