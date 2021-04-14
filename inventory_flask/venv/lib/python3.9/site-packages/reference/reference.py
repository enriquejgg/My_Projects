#!/usr/bin/env python
# -*- coding=utf-8 -*-


import os
import sys
import re
import getopt
import subprocess



__author__ = "handa"
__version__ = "0.1.0"

def excommand_until_done(cmd):
    """
    子线程执行脚本，直到结束，并输出
    Arguments:
        cmd {str} -- cmd命令
    :returns (,str)
    """
    p=subprocess.Popen(args="export LANG=en_US.UTF-8;"+cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    outPut=""
    for line in iter(p.stdout.readline, ''):
        outPut+=line
        print line.rstrip()
    p.wait()
    return (p.returncode,outPut)

def file_exist(path):
    """
    检测模块是否已经安装
    Arguments:
        path {str} -- 模块路径
    Returns:
        Bool -- 是否已经安装
    """
    if os.path.isdir(path) or os.path.isfile(path):
        return True
    return False

def format_print(printString, separator=""):
    """
    格式化输出格式
    Arguments:
        printString {str} -- 要输出的内容
    """
    if separator:
        print (separator) * 40 + '\n'
    print str(printString)
    if separator:
        print (separator) * 40 + '\n'


def write_to_File(string, filePath):
    """把内容写进文件
    Arguments:
        string {string} -- 文件内容
        filePath {string} -- 文件路径
    """
    with open(filePath, "w+") as fileWriter:
        fileWriter.write(str(string))


def append_to_file(string, filePath):
    with open(filePath, "a+") as fileWriter:
        fileWriter.write(str(string))

def read_file(filePath):
    """读文件

    Arguments:
        filePath {str} -- 文件路径

    Returns:
        str -- 文件内容
    """
    with open(filePath, "r+") as fileReader:
        return fileReader.read()


def read_file_lines(filePath):
    """读文件成行
    Arguments:
        filePath {str} -- 文件路径
    Returns:
        str -- 文件内容
    """
    with open(filePath, "r+") as fileReader:
        return fileReader.readlines()


def match_list(pattern, string, byLine=False):
    """正则匹配

    Arguments:
        pattern {str} -- 正则表达式
        string {str} -- 要匹配的全量字符串

    Keyword Arguments:
        byLine {bool} -- 是不是一行一样匹配 (default: {False})

    Returns:
        [list] -- 匹配成功的列表
    """
    if string == "未知消息类型":
        return -1
    if byLine:
        pattern = re.compile(pattern)
    else:
        pattern = re.compile(pattern, re.S)
    matchList = pattern.findall(string)
    if matchList:
        return matchList
    else:
        return ["未知消息类型"]


def print_tips():
    format_print("""
    本脚本主要作用是帮助组件解耦
    
    功能如下：
        1. 替换不规范的引用方式，如引用第三方库，把 #import "xxx.h" 或者 #import <xx.h> 替换成 #import <xxx/xxx.h>
        
    参数如下：
            --projectPath               项目路径
            --sourcePath                要查的库的路径，多个路径用 "," 隔开，不填写的话，会找符合podspec标准模板的库
            --onlyCheck                 仅检查不改动引用方式
    示例：
        > reference
            --projectPath=/Users/handa/Documents/Messenger      
            --sourcePath=/Users/handa/Documents/Messenger/LJMessengerSDK

    
    """, " *")


def return_error():
    exit(1)


def get_arguments():
    """
    获得参数
    :param type: 哪个命令的参数
    :return:
    """
    if type == "":
        return
    try:
        opts, args = getopt.getopt(sys.argv[1:], "psoh",
                                   ["help", "projectPath=", "sourcePaths=", "onlyCheck"])
        # sys.argv[1:] 过滤掉第一个参数(它是脚本名称，不是参数的一部分)
    except getopt.GetoptError:
        print_tips()
        return_error
    if not args and not opts:
        print_tips()
        return_error()
    onlyCheck = False
    projectPath=""
    sourcePaths=""
    for cmd, arg in opts:
        print cmd
        # 使用一个循环，每次从opts中取出一个两元组，赋给两个变量。cmd保存选项参数，arg为附加参数。接着对取出的选项参数进行处理。
        if cmd in ("--onlyCheck", "-o"):
            onlyCheck = True
        elif cmd in ("--projectPath", "-p"):
            projectPath = str(arg)
        elif cmd in ("--sourcePaths", "-s"):
            sourcePaths = str(arg)
        else:
            print_tips()
            return_error()
    for arg in args:
        print arg
    if projectPath:
        projectPath = projectPath.rstrip("/")
    return projectPath, sourcePaths, onlyCheck

def get_source_file_path(projectPath, sourcePath):
    os.chdir(sourcePath)
    returnCode, content = excommand_until_done("tree -f -i | grep 'Class[A-Za-z0-9_/\\]*\.m*[hm]$'")
    if not content:
        format_print(sourcePath + "里面没有任何oc文件", " *")
        return_error()
    filePaths = str(content).strip(" ").split("\n")
    os.chdir(projectPath)
    return filePaths

def pods_dirs(projectPath):
    returnCode, content = excommand_until_done("tree -f -i | grep 'Pods$'")
    if returnCode > 0:
        format_print("Pods文件不存", " -")
        returnCode, podfile_content = excommand_until_done("tree -f -i | grep 'Podfile$'")
        if returnCode > 0:
            format_print("没找到podfile文件，不适合本程序。")
            return_error()
        podfilePaths = str(podfile_content).strip(" ").split("\n")
        podfileDir = os.path.dirname(podfilePaths[0])
        os.chdir(podfileDir)
        returnCode, content = excommand_until_done("IS_SOURCE=1 pod update --verbose")
        if returnCode > 0:
            format_print("pod update 失败", " *")
            return_error()
        os.chdir(projectPath)
        returnCodes, content = excommand_until_done("tree -f -i | grep 'Pods$'")
    podsPaths = str(content).strip(" ").split("\n")
    podsPath = podsPaths[0]
    os.chdir(podsPath)
    returnCode, content = excommand_until_done("ls -F |awk '{print i$0}' i=`pwd`'/'")
    tmpPaths = content.replace(projectPath, ".").strip("").strip("\n").split("\n")
    podPaths = []
    for podPath in tmpPaths:
        if not podPath.endswith("/"):
            continue
        elif podPath.endswith("Target Support Files/"):
            continue
        elif podPath.endswith("Headers/"):
            continue
        elif podPath.endswith("Local Podspecs/"):
            continue
        elif podPath.endswith("Pods.xcodeproj/"):
            continue
        else:
            podPaths.append(podPath)
    os.chdir(projectPath)
    return podPaths

def source_paths(projectPath, sourcePaths=""):
    resultPaths = []
    if sourcePaths:
        paths = sourcePaths.strip("").split(",")
        for tmpPath in paths:
            resultPaths.append(str(tmpPath).strip("").strip("\n").replace(projectPath, "."))
    else:
        returnCode, content = excommand_until_done("tree -f -i | grep 'podspec$'")
        if returnCode > 0:
            format_print("podspec文件不存", " *")
            return_error()
        podspecPaths = str(content).strip(" ").strip("\n").split("\n")
        for podspecPath in podspecPaths:
            specName = podspecPath.strip(" ").split("/")[-1].strip(".podspec")
            resultPaths.append("./" + specName)
    return resultPaths


def path_dict(projectDict, allPaths):
    allDict = {}
    for filePath in allPaths:
        pattern = "tree -f -i | grep '^" + str(filePath).strip("").rstrip("/") + ".*\.[m]*[hm]$'"
        returnCode, content = excommand_until_done(pattern)
        if returnCode > 0:
            format_print(pattern + "失败", " *")
        filePaths = str(content).strip("").strip("\n").split("\n")
        tmpPaths = []
        for file in filePaths:
            if "/Framework/" in file or "/Archive/" in file or "/Assets/" in file:
                continue
            if "\\" in file:
                file = file.replace("\\", "")
            tmpPaths.append(file)
        # swiftPattern = "tree -f -i | grep '^" + str(filePath).strip("").rstrip("/") + ".*\.swift$'"
        # returnCode, content = excommand_until_done(swiftPattern)
        # if returnCode > 0:
        #     format_print(pattern + "失败", " *")
        #     return_error()
        # swiftFilePaths = str(content).strip("").strip("\n").split("\n")
        # for file in swiftFilePaths:
        #     if "/Framework/" in file or "/Archive/" in file or "/Assets/" in file:
        #         continue
        #     if "\\" in file:
        #         file = file.replace("\\", "")
        #     tmpPaths.append(file)
        allDict[filePath] = "\n".join(tmpPaths)
    return allDict

def find_pod(header, allDict={}):
    for podPath, filePathContent in allDict.items():
        if header in filePathContent:
            podName = str(podPath).rstrip("/").split("/")[-1]
            filePaths = filePathContent.split("\n")
            for filePath in filePaths:
                if header in filePath:
                    return podName, filePath
    return "", ""

def make_report(originReference, originFilePath, destReference, destFilePath):
    format_print(originFilePath + "   =>  " + originReference + "\n替换成 => " + destReference, " -")
    originReference = originReference.replace("<", "\<").replace(">", "\>")
    originFilePath = originFilePath.replace("<", "\<").replace(">", "\>")
    destReference = destReference.replace("<", "\<").replace(">", "\>")
    destFilePath = destFilePath.replace("<", "\<").replace(">", "\>")
    return "[" + originReference + "](" + originFilePath + ") => [" + destReference + "](" + destFilePath + ")\n"


def check_reference(projectPath, sourcePaths, allDicts, onlyCheck):
    reportFilePath = os.path.join(projectPath, "report.md")
    reportContent = "## 引用更改报\n\n"
    cacheReferenceDict = {}
    cachePodFilePathDict = {}
    for sourcePath in sourcePaths:
        filePathContent = allDicts[sourcePath]
        filePaths = filePathContent.split("\n")
        for filePath in filePaths:
            fileLines = read_file_lines(filePath)
            fileContent = read_file(filePath)
            changed = False
            for line in fileLines:
                line = str(line).strip(" ").strip("\n")
                if not line:
                    continue
                if line.startswith("/"):
                    continue
                elif line.startswith("#import <") and line.find("/") > -1:
                    continue
                elif line.startswith("#import"):
                    # 处理
                    replaceContent = ""
                    podFilePath = ""
                    if line in cacheReferenceDict.keys():
                        replaceContent = cacheReferenceDict[line]
                        podFilePath = cachePodFilePathDict[line]
                    else:
                        headerFile = line.replace("#import ", "").strip("").replace("\"", "").replace("<", "").replace(">", "")
                        if headerFile in filePathContent:
                            continue
                        else:
                            # 在别的里面。
                            podName, podFilePath = find_pod(headerFile, allDicts)
                            if not podName or not podFilePath:
                                # 系统的。
                                continue
                            replaceContent = "#import <" + podName + "/" + headerFile + ">"
                            cacheReferenceDict[line] = replaceContent
                            cachePodFilePathDict[line] = podFilePath
                    reportContent += make_report(line, filePath, replaceContent, podFilePath)
                    fileContent = str(fileContent).replace(line, replaceContent)
                    changed = True
                else:
                    break
            if changed and not onlyCheck:
                write_to_File(fileContent, filePath)
    if reportContent:
        write_to_File(reportContent, reportFilePath)



def checkopts():
    """
    检测输入参数
    """

    projectPath, sourcePaths, onlyCheck = get_arguments()
    if not file_exist(projectPath):
        format_print("所给的目录不存在，请检查", " *")
        return_error()
    os.chdir(projectPath)
    podPaths = pods_dirs(projectPath)
    sourcePaths = source_paths(projectPath, sourcePaths)
    allPaths = []
    allPaths.extend(podPaths)
    allPaths.extend(sourcePaths)
    format_print("正在分析目录结构中。。。", "- ")
    allDicts = path_dict(projectPath, allPaths)
    format_print("正在处理引用方式", "- ")
    check_reference(projectPath, sourcePaths, allDicts, onlyCheck)
    format_print("处理完毕","- ")

def main():
    # 调用接口
    checkopts()


if __name__ == "__main__":
    sys.exit(checkopts())
