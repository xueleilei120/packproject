# -*- coding:gb2312 -*-
"""
@author : liuyc
@mtime : {2017/6/20 0020} {���� 10:35}
@Description : 
"""
import sys
import os
from datetime import datetime


from ExportPack import ExportPack


class MakePackBase(object):
    """
    1.ǿsvn���߱��ص��ļ����Ƶ�����
    2.����packList.txt�е��ļ�
    3.ɾ��excludeLIST.txt�е��ļ�
    """
    def __init__(self):
        # node_file_path = 'C:\Users\a\Desktop\test\packproject\node'
        node_file_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]

        # �ļ�����·������svn��local������Ϸ�ű�����Ŀ¼��
        self.export_path = os.path.join(node_file_path, "ExportFile\\")
        # zip�Ļ���·��
        self.cache_path = os.path.join(node_file_path, "Cache\\")
        # ������ʵ��
        self.export_pack_obj = ExportPack()

    # �������Ŀ¼
    def create_out_file(self, out_path):
        cmd_line = "md %s"%(out_path)
        os.system(cmd_line)

    def make_zip(self, export_path, local_cache_path, zip_name):
        curdir = sys.path[0]
        # ���Ĺ���Ŀ¼
        os.chdir(export_path)

        zippath = "%s\\%s" % (local_cache_path, zip_name)
        #print("zippath:%s" % zippath)
        # make new zip
        strCmd = "winrar a -t -r %s .\\*.*" % (zippath)
        os.system(strCmd)

        # ���Ļ�ԭ�ȹ���Ŀ¼
        os.chdir(curdir)


class MakePackSvrGame(MakePackBase):
    """
    ��Ϸ���������
    """
    def __init__(self):
        super(MakePackSvrGame, self).__init__()

    # ִ�д��
    def Doit(self, svn_game_path, local_path, nick_name):
        # �ж��Ǳ��ػ���svn ����svn
        if svn_game_path:
            _, game_name = os.path.split(svn_game_path)
            local_export_path = self.export_path + game_name
            if not self.export_pack_obj.export_file_from_svn(svn_game_path, local_export_path):
                return "", ""
        else:
            _, game_name = os.path.split(local_path)
            local_export_path = self.export_path + game_name
            if not self.export_pack_obj.export_file_from_local(local_path, local_export_path):
                return "", ""
        local_cache_path = self.cache_path + game_name

        if not os.path.exists(local_cache_path):
            self.create_out_file(local_cache_path)

        version = datetime.now().strftime('%Y.%m.%d-%H.%M.%S')
        zip_name = "%s-%s.zip" % (nick_name, version )
        self.make_zip(local_export_path, local_cache_path, zip_name)
        return local_cache_path, zip_name




# if __name__ == "__main__":
#     clsMakePack = MakePackSvrGame()
#     svn_path = "http://192.168.130.214/svn/resource/trunk/bins/debug/luagame/XServer/games/njmj"
#     clsMakePack.Doit("server", svn_path)

# print(os.path.join(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0], "ExportFile\\"))
