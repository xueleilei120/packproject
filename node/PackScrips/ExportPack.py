# -*- coding:gb2312 -*-
"""
@author : liuyc
@mtime : {2017/6/20 0020} {上午 10:35}
@Description : 导出包类至本地
"""

import os
import copy
import shutil
import logging

class ExportPack:
    def __init__(self):
        pass

    # 将指定游戏从svn上导出到指定位置
    # 参数1：需要打包的游戏的svn，参数2：将所需文件导出的位置
    def export_file_from_svn(self, svn_path, export_to_path):
        # 删除旧文件
        self.deleted_old_file(export_to_path)

        # 按packlist打包来选择需要打包的文件
        packlist_path = svn_path + '/packLIST.txt'
        # print "packlist_path=%s" % packlist_path

        # 将packLIST.txt文件导出
        str_cmdline = "svn export -q  --force %s %s" % (packlist_path, export_to_path)
        try:
            os.system(str_cmdline)
        except Exception, e:
            logging.error(e, exc_info=True)

        # 判断packLIST.txt文件是否存在
        local_packlist_path = export_to_path + '/packLIST.txt'
        has_packlist = os.path.exists(local_packlist_path)
        if not has_packlist:
            # print "error: cannot find packlist"
            return False

        # print "has_packlist"

        # 记录所有需要打包的文件名
        file_list = copy.deepcopy(self.check_configs(local_packlist_path))
        # 将文件夹中的所有文件导入到指定的本地位置
        for file_name in file_list:
            file_path = svn_path + '/' + str(file_name)
            # print file_path
            temp_path = export_to_path   # 此举是为了将按文件件的形式存放在本地的文件夹下
            temp_path = temp_path + '\\' + file_name
            str_cmdline = "svn export -q  --force %s %s" % (file_path, temp_path)
            os.system(str_cmdline)

        # 导出排除列表文件
        excludelist_svnpath = svn_path + '/excludeLIST.txt'
        cmd_line = "svn export -q  --force %s %s" % (excludelist_svnpath, export_to_path)
        try:
            os.system(cmd_line)
        except Exception, e:
            logging.warn(e, exc_info=True)
            return

        # 判断文件是否存在
        exclude_txt = export_to_path + '/excludeLIST.txt'
        has_file = os.path.exists(exclude_txt)
        if not has_file:
            # print "cannot find excludeLIST"
            return

        # 删除排除列表中不希望打包的文件
        self.del_exclude_files(export_to_path, exclude_txt)
        return True

    # 将指定游戏从本地上导出到指定位置
    def export_file_from_local(self, local_path, export_to_path):
        # 删除旧文件
        self.deleted_old_file(export_to_path)

        # 判断packLIST.txt文件是否存在
        local_packlist_path = local_path + '/packLIST.txt'
        print(local_packlist_path)
        has_packlist = os.path.exists(local_packlist_path)
        if not has_packlist:
            # print "error: cannot find packlist"
            return False

        # print "has_packlist"

        # 记录所有需要打包的文件名
        file_list = copy.deepcopy(self.check_configs(local_packlist_path))
        # 将文件夹中的所有文件导入到指定的本地位置
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
        # # 删除排除列表中不希望打包的文件
        # self.del_exclude_files(svn_path, export_to_path)
        return True

    # 检查文件列表，记录所有需要打包的文件
    def check_configs(self, sConfigFile):
        # 打开指定文件
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

        # 关闭IO
        fileinfo.close()

        # 输出文件列表信息
        # print "Filelist: %s" % filelist
        return filelist

    # 删除指定目录下的所有文件
    def deleted_old_file(self, old_filepath):
        # 删除指定目录及其子目录下的所有文件
        cmd_line = "rd /s /q %s" % (old_filepath)
        os.system(cmd_line)
        # 重新创建目录
        cmd_line = "md %s" % (old_filepath)
        os.system(cmd_line)

    # 删除指定文件
    def del_file(self, filepath):
        str_cmd = "del /f %s" % (filepath)
        os.system(str_cmd)

    def del_exclude_files(self, svn_path, export_localpath):
        # 导出排除列表文件
        excludelist_svnpath = svn_path + '/excludeLIST.txt'
        cmd_line = "svn export -q  --force %s %s" % (excludelist_svnpath, export_localpath)
        try:
            os.system(cmd_line)
        except Exception, e:
            logging.warn(e, exc_info=True)
            return

        # 判断文件是否存在
        excludelist_path = export_localpath + '/excludeLIST.txt'
        has_file = os.path.exists(excludelist_path)
        if not has_file:
            # print "cannot find excludeLIST"
            return

        # print "find excludeLIST sucessful"

        # 记录所有需要排除的文件名
        filelist = copy.deepcopy(self.check_configs(excludelist_path))
        for obj in filelist:
            obj = obj.replace('/', '\\')
            obj_path = export_localpath + '\\' + obj
            if os.path.exists(obj_path):  # 文件如果存在，删除
                self.del_file(obj_path)
                # print "del file:%s" % obj_path

# if __name__ == "__main__":
#     clsExportPack = ExportPack()
#     clsExportPack.ExportFileFromSvn("http://192.168.130.214/svn/resource/trunk/gamecore/clientcore-dev/drmj", "C:\\Users\\a\\Desktop\\test_pack\\drmj")