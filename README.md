packproject
===========================
基于 django+xadmin 的游戏脚本打包系统 支持本地和拉取svn 打包 <br>
大家 可以通过添加 svn路径和本地路径 然后就可以在线打包了
****
### Author:男儿有泪不轻弹
### QQ:290484002
### [我的博客](http://liuyc2.pythonanywhere.com) 
****
## 打包说明
* 包中必须包含一个 packLIST.txt
    ;本文件夹中存放需要打包的目录和文件名
    ;文件夹打包只需要填写文件夹目录，具体文件则需要填写文件名加后缀 如
    File
    config.lua
    init.lua
* 包中必须包含一个 excludeLIST.txt
    ;打包排除列表下列的文件均不会被打包
    excludeLIST.txt
    packLIST.txt
* 需要注意的是svn打包 必须安装 svn client

## Requirements
* Django <1.9.8>
* django-crispy-forms <1.6.1>
* django-formtools <2.0>
* httplib2 <0.9.2>
* setuptools <18.0.1>
* wheel <0.24.0>
## Installation
    https://github.com/xueleilei120/packproject.git

## Screenshots
![](https://github.com/xueleilei120/packproject/raw/master/static/images/jietu.PNG)
