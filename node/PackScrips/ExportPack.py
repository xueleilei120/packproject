# -*- coding:gb2312 -*-
"""
@author : liuyc
@mtime : {2017/6/20 0020} {���� 10:35}
@Description : ��������������
"""

import os
import copy
import shutil
import logging

class ExportPack:
    def __init__(self):
        pass

    # ��ָ����Ϸ��svn�ϵ�����ָ��λ��
    # ����1����Ҫ�������Ϸ��svn������2���������ļ�������λ��
    def export_file_from_svn(self, svn_path, export_to_path):
        # ɾ�����ļ�
        self.deleted_old_file(export_to_path)

        # ��packlist�����ѡ����Ҫ������ļ�
        packlist_path = svn_path + '/packLIST.txt'
        # print "packlist_path=%s" % packlist_path

        # ��packLIST.txt�ļ�����
        str_cmdline = "svn export -q  --force %s %s" % (packlist_path, export_to_path)
        try:
            os.system(str_cmdline)
        except Exception, e:
            logging.error(e, exc_info=True)

        # �ж�packLIST.txt�ļ��Ƿ����
        local_packlist_path = export_to_path + '/packLIST.txt'
        has_packlist = os.path.exists(local_packlist_path)
        if not has_packlist:
            # print "error: cannot find packlist"
            return False

        # print "has_packlist"

        # ��¼������Ҫ������ļ���
        file_list = copy.deepcopy(self.check_configs(local_packlist_path))
        # ���ļ����е������ļ����뵽ָ���ı���λ��
        for file_name in file_list:
            file_path = svn_path + '/' + str(file_name)
            # print file_path
            temp_path = export_to_path   # �˾���Ϊ�˽����ļ�������ʽ����ڱ��ص��ļ�����
            temp_path = temp_path + '\\' + file_name
            str_cmdline = "svn export -q  --force %s %s" % (file_path, temp_path)
            os.system(str_cmdline)

        # �����ų��б��ļ�
        excludelist_svnpath = svn_path + '/excludeLIST.txt'
        cmd_line = "svn export -q  --force %s %s" % (excludelist_svnpath, export_to_path)
        try:
            os.system(cmd_line)
        except Exception, e:
            logging.warn(e, exc_info=True)
            return

        # �ж��ļ��Ƿ����
        exclude_txt = export_to_path + '/excludeLIST.txt'
        has_file = os.path.exists(exclude_txt)
        if not has_file:
            # print "cannot find excludeLIST"
            return

        # ɾ���ų��б��в�ϣ��������ļ�
        self.del_exclude_files(export_to_path, exclude_txt)
        return True

    # ��ָ����Ϸ�ӱ����ϵ�����ָ��λ��
    def export_file_from_local(self, local_path, export_to_path):
        # ɾ�����ļ�
        self.deleted_old_file(export_to_path)

        # �ж�packLIST.txt�ļ��Ƿ����
        local_packlist_path = local_path + '/packLIST.txt'
        print(local_packlist_path)
        has_packlist = os.path.exists(local_packlist_path)
        if not has_packlist:
            # print "error: cannot find packlist"
            return False

        # print "has_packlist"

        # ��¼������Ҫ������ļ���
        file_list = copy.deepcopy(self.check_configs(local_packlist_path))
        # ���ļ����е������ļ����뵽ָ���ı���λ��
        for file_name in file_list:
            local_file_path = local_path+'\\' + file_name
            export_file_path = export_to_path+ '\\' + file_name
            print(local_file_path)
            print(export_file_path)
            if os.path.isdir(local_file_path):
                shutil.copytree(local_file_path, export_file_path)
            elif os.path.isfile(local_file_path):
                shutil.copyfile(local_file_path, export_file_path)
            else:
                print("copy local_pack_file error")
                return False

        exclude_txt = local_path+'\\' + "excludeLIST.txt"
        self.del_exclude_files(export_to_path, exclude_txt)
        # # ɾ���ų��б��в�ϣ��������ļ�
        # self.del_exclude_files(svn_path, export_to_path)
        return True

    # ����ļ��б���¼������Ҫ������ļ�
    def check_configs(self, sConfigFile):
        # ��ָ���ļ�
        fileinfo = file(sConfigFile, 'rb')

        filelist = []
        for strLine in fileinfo:
            if strLine == "":
                continue
            if strLine.startswith("#") or strLine.startswith(";"):
                continue
            lst_info = strLine.split()
            if len(lst_info) == 1:
                filelist.extend(lst_info)

        # �ر�IO
        fileinfo.close()

        # ����ļ��б���Ϣ
        # print "Filelist: %s" % filelist
        return filelist

    # ɾ��ָ��Ŀ¼�µ������ļ�
    def deleted_old_file(self, old_filepath):
        # ɾ��ָ��Ŀ¼������Ŀ¼�µ������ļ�
        cmd_line = "rd /s /q %s" % (old_filepath)
        os.system(cmd_line)
        # ���´���Ŀ¼
        cmd_line = "md %s" % (old_filepath)
        os.system(cmd_line)

    # ɾ��ָ���ļ�
    def del_file(self, filepath):
        str_cmd = "del /f %s" % (filepath)
        os.system(str_cmd)

    def del_exclude_files(self, svn_path, export_localpath):
        # �����ų��б��ļ�
        excludelist_svnpath = svn_path + '/excludeLIST.txt'
        cmd_line = "svn export -q  --force %s %s" % (excludelist_svnpath, export_localpath)
        try:
            os.system(cmd_line)
        except Exception, e:
            logging.warn(e, exc_info=True)
            return

        # �ж��ļ��Ƿ����
        excludelist_path = export_localpath + '/excludeLIST.txt'
        has_file = os.path.exists(excludelist_path)
        if not has_file:
            # print "cannot find excludeLIST"
            return

        # print "find excludeLIST sucessful"

        # ��¼������Ҫ�ų����ļ���
        filelist = copy.deepcopy(self.check_configs(excludelist_path))
        for obj in filelist:
            obj = obj.replace('/', '\\')
            obj_path = export_localpath + '\\' + obj
            if os.path.exists(obj_path):  # �ļ�������ڣ�ɾ��
                self.del_file(obj_path)
                # print "del file:%s" % obj_path

# if __name__ == "__main__":
#     clsExportPack = ExportPack()
#     clsExportPack.ExportFileFromSvn("http://192.168.130.214/svn/resource/trunk/gamecore/clientcore-dev/drmj", "C:\\Users\\a\\Desktop\\test_pack\\drmj")