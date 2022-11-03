import PySimpleGUI as sg
from hashlib import sha1
import os, shutil


def gui():
    layout = [
        [sg.Text('你选择的文件夹是:', font=("宋体", 10)), sg.Text('', key='text1', size=(50, 1), font=("宋体", 10))],
        [sg.Text('程序运行记录', justification='center')],
        [sg.Output(size=(70, 20), font=("宋体", 10))],
        [sg.FolderBrowse('打开文件夹', key='folder', target='text1'), sg.Button('重命名'), sg.Button('关闭程序')]
    ]

    window = sg.Window('雁陎的工具箱', layout, font=("宋体", 15), default_element_size=(50, 1))

    while True:
        event, values = window.read()
        if event in (None, '关闭'):  # 如果用户关闭窗口或点击`关闭`
            break
        if event == '重命名':
            if values['folder']:
                print('{0}正在重命名原文件为hash值{0}'.format('*' * 10))
                mult_rename(values['folder'])
                print('{0}重命名完毕{0}'.format('*' * 10))
            else:
                print('请先选择文件夹')

    window.close()


def calchash(file_path):  # 计算图片hash值
    with open(file_path, 'rb') as f:
        sha1obj = sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        return hash


def mult_rename(dir_path):  # 批量重命名
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        if not os.path.isdir(file_path):  # 判断是否为文件夹
            pic_hash = calchash(file_path)  # 计算hash值
            last = file[file.rindex(r'.'):]  # 后缀
            new_name = pic_hash + last
            if file == new_name:
                print(file, '无需修改')
            else:
                try:
                    new_path = os.path.join(dir_path, new_name)
                    os.rename(file_path, new_path)
                    print('{0}已重命名为{1}'.format(file, new_name))
                except FileExistsError:
                    repeat_path = dir_path + r'\重复文件夹'
                    if os.path.exists(repeat_path) == False:
                        os.makedirs(repeat_path)
                    new_path = os.path.join(repeat_path, new_name)
                    shutil.move(file_path, new_path)
                    print(r'{0}文件重复，已移至重复文件夹下'.format(file))


def main():
    gui()


if __name__ == '__main__':
    main()     