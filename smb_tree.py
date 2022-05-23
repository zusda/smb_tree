import os
import re

'''
代码没有设置报错处理功能，报错会直接显示到shell上，自行处理（滑稽
'''

D=[]
disk="//10.10.10.100/Replication"
username=""
password=""

limit=999

def list_dir(dir,level):


    if level!=limit:

        command="smbclient -c \"ls "+dir+"\" "+disk+" -U  "+username+"%"+password
        resualt = os.popen(command)

        # 查看执行的命令，debug用
        # print(command)

        resualts = resualt.read().split("\n")
        num = 0
        for line in resualts:
            # 去除空行
            if line == "":
                break

            # 判断是否是文件夹
            line_blocks = re.sub(' +', ' ', line)
            line_blocks = line_blocks.split(" ")

            # print(line_blocks)

            name_temp=line_blocks[1:-7]
            if len(name_temp)>1:
                name="\\\""
                for iii in name_temp:
                    if iii != name_temp[len(name_temp)-1]:
                        name=name+iii
                        name=name+" "
                    else:
                        name = name + iii
                name = name+"\\\""
            else:
                name=" ".join(name_temp)

            dir_type=line_blocks[-7]

            # print(dir_type)
            # print(name)

            if name =="." or name=="..":
                continue


            D.append([name,level,dir_type])

            if dir_type=="D" :
                # print(dir+name+"/")
                list_dir(dir+name+"/",level+1)


def print_list(D):

    def chars(num,c):
        return str(c) * num * 3

    D = D[1:]

    for i in D:
        if i[2]=="A":
            print(chars(i[1] - 1,"- ") + i[0].replace("\\\"","") + "(" + i[2] + ")")
        else:
            print(chars(i[1] - 1, "  ") + i[0].replace("\\\"","") + "(" + i[2] + ")")

def get_path(D):

    # path 记录当前路径
    path = []

    path_list = []

    j = 0
    i = 0
    # path[i] 记录路径的最后一个文件夹名字
    # D[j] 当前处理的文件或文件夹
    while 1:

        if len(D)==j:
            break

        if D[j][2] != "A":

            if len(path)==0:
                path.append(D[0])
                continue

            if path[i][1] < D[j][1]:
                path.append(D[j])
                i = i + 1
                j = j + 1
                # print(path)
                continue

            if path[i][1] == D[j][1]:
                path.pop()
                path.append(D[j])
                j = j + 1
                # print(path)
                continue

            if path[i][1] > D[j][1]:
                path.pop()
                # path.pop()
                # path.append(D[j])
                # j = j + 1
                i = i - 1
                # print(path)
                continue

        elif D[j][2] == "A":
            while D[j][1]<path[i][1] or D[j][1]==path[i][1] :
                path.pop()
                i=i-1

            path_temp=[]

            for ii in path:

                path_temp.append(ii[0])
                path_temp.append("/")


            P="".join(path_temp)
            path_list.append(P+D[j][0])
            j=j+1
        else:
            j = j + 1

    print(path_list)
    return path_list


import os

import datetime
import time


today = datetime.date.today()
now = time.strftime("%H_%M_%S")
saved_dir="./smb_tree_{}_{}".format(str(today).replace("-",""),now)



if not os.path.exists(saved_dir):
    os.makedirs(saved_dir)

def smb_download(paths):

    for i in paths:
        file_name=i.split("/")[-1]

        if  os.path.exists(saved_dir+"/"+file_name):
            now = time.strftime("%H_%M_%S")
            file_name=file_name+"_"+str(now)

        saved_path=saved_dir+"/"+file_name

        command="smbclient -c \"get "+i+" "+saved_path+" \" "+disk+" -U  "+username+"%"+password
        # print(command)
        resualt = os.system(command)

        if resualt!=0:
            print("\n下载出错： {}\n".format(i))

D.append(["",0,0])
current_dir=""
l=0

list_dir(current_dir,l+1)

print("\n\n原始获得的数据\n")
print(D)
print("\n\n")
print("there is smb_tree")
print_list(D)
print("\n\n")

D = D[1:]
path=get_path(D)

# print(path)
smb_download(path)

print("\n\nfiles save in {}\n\n".format(saved_dir))











