import os
import tkinter as tk
import urllib.request
from tkinter import messagebox
from tkinter.filedialog import *

from PIL import Image

# 字符串
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


# """颜色转化灰度值"""
def rgb_char(r, g, b, alpha=256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1) / length
    return ascii_char[int(gray / unit)]


# """根据url获取文件名"""
def get_file_name(url):
    if url is None:
        return None
    if url == "":
        return ""
    arr = url.split("/")
    return arr[len(arr) - 1]

# 定义个一个窗口，里面包含一个文本框（默认字为图片网址），一个按钮（点击选择电脑文件），一个按钮（转化）
class Application():
    def __init__(self, root):
        self.root = root
        self.frame_top()
        self.frame_bottom()

    def frame_top(self):
        self.top_label = tk.Label(self.root, text="图片转字符画神器", bg="yellow", font=('黑体', 20))
        self.top_label.grid(row=0, column=0, pady=15, ipady=5)

    def frame_bottom(self):
        self.bottom = tk.LabelFrame(self.root)  # 底部父容器
        self.bottom.grid()

        self.bottom_label = tk.Label(self.bottom, text="本地图片路径：", font=("黑体", 12))
        self.bottom_label.grid(row=0, sticky=W, padx=30, ipadx=5, pady=15, ipady=5)

        self.bottom_local_entry_var = StringVar()  # 获取值
        self.bottom_local_entry = tk.Entry(self.bottom, textvariable=self.bottom_local_entry_var, width=30)
        self.bottom_local_entry.grid(row=0, column=1, padx=30, ipadx=5, pady=15, ipady=5)

        self.bottom_button = tk.Button(self.bottom, text="选择文件", bd=5, width=10, command=self.open_dialog)
        self.bottom_button.grid(row=1, columnspan=3, padx=30, pady=15, ipady=5, sticky=E)

        self.bottom_label2 = tk.Label(self.bottom, text="网络图片路径：", font=("黑体", 12))
        self.bottom_label2.grid(row=2, sticky=W, padx=30, ipadx=5, pady=15, ipady=5)

        self.bottom_net_entry_var = StringVar()  # 获取值
        self.bottom_net_entry = tk.Entry(self.bottom, textvariable=self.bottom_net_entry_var, width=30)
        self.bottom_net_entry.grid(row=2, column=1, padx=30, ipadx=5, pady=15, ipady=5)

        self.bottom_to = tk.Button(self.bottom, text="转化", bd=5, width=10, command=self.rgb2char)
        self.bottom_to.grid(row=3, columnspan=3, padx=30, ipadx=5, pady=15, ipady=5, sticky=E)

    def open_dialog(self):
        filename = askopenfilename(filetypes=(("All files", "*.*"),))  # 打开系统文件夹,获取文件
        if filename != "":  # 将选择的文件路径填写到输入框中
            self.bottom_local_entry_var.set(filename)

    def rgb2char(self):
        if self.bottom_local_entry_var.get() == "":
            if self.bottom_net_entry_var.get() == "":
                messagebox.showinfo("提示", "路径不为空或者路径不正确！")
            else:
                # 从网络获取图片，保存到本地，再获取该图片图片路径，再转化
                file_name = get_file_name(self.bottom_net_entry_var.get())
                urllib.request.urlretrieve(self.bottom_net_entry_var.get(), file_name)
                image_file(os.path.abspath(file_name))
        else:
            image_file(self.bottom_local_entry_var.get())

def image_file(path):
    im = Image.open(path)
    im = im.resize((int(im.size[0] * 0.9), int(im.size[1] * 0.5)))
    txt = ""
    for i in range(im.size[1]):  # 高
        for j in range(im.size[0]):  # 宽
            txt += rgb_char(*im.getpixel((j, i)))
        txt += "\n"
    with open('abc.txt', 'w') as f:
        f.write(txt)
    messagebox.showinfo("提示", "转换成功")



if __name__ == "__main__":
    root = tk.Tk()
    Application(root)
    root.mainloop()
