import tkinter as tk
from tkinter import Label


class GUI:
    def __init__(self):
        """设置窗体"""
        self.top = tk.Tk()
        self.top.title("simulation")
        self.top.geometry("1080x710")
        self.top.resizable(width=False, height=False)
        """设置画布"""
        self.c = tk.Canvas(self.top, width=1080, height=680, bg="#A9A9A9")
        self.c.pack()
        self.label = Label(self.top, text="Time = 0.0 s")
        self.label.pack()
    """绘制障碍物"""
    def add_barrier(self):
        #  添加边框
        self.c.create_rectangle(0, 0, 1080, 40, fill="#696969", outline="#696969")
        self.c.create_rectangle(0, 640, 1080, 680, fill="#696969", outline="#696969")
    """更新显示时间"""
    def update_time(self, _time):
        self.label['text'] = "Time = \t"+_time + "\t s"
    """绘制圆"""
    def add_oval(self, x, y, r, tag, p_type):
        if p_type == 1:
            self.c.create_oval(x - r, y - r, x + r, y + r, fill="#FFE4B5", tag=tag)
        else:
            self.c.create_oval(x - r, y - r, x + r, y + r, fill="#00BFFF", tag=tag)
    """删除圆"""
    def del_oval(self, oval_tag):
        self.c.delete(oval_tag)
    '''更新'''
    def update_gui(self):
        self.top.update()
        self.c.update()
    '''启动GUI'''
    def start(self):
        self.top.mainloop()