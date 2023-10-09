# 作   者：陈中超
# 开发日期:2023/10/9
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
from mysql import MysqlUtil


class Information(Frame):
    def __init__(self, master=None, mysqlUtil=None):
        """
        完成类的属性的初始化
        :param master: 窗口
        :param mysqlUtil: 数据库连接对象
        """
        super().__init__(master)
        self.master = master
        self.mysqlUtil = mysqlUtil
        self.createWidget()

    # 定义并绑定Treeview组件的鼠标左键双击事件
    def treeviewClick(self, event):
        """
        双击可显示选中人的姓名
        :param event:鼠标左键双击
        :return:
        """
        selectedItem = self.tree.selection()[0]
        name = self.tree.item(selectedItem, 'values')[0]
        messagebox.showinfo('报告', "你的选择是\n" + name)

    # 导入数据
    def insertData(self, data):
        # 将数据库中的信息导入表格
        for item in data:
            values = [item.get('姓名'), item.get('年龄'), item.get('学号')]
            self.tree.insert('', 'end', values=values)

    # 删除选中学生
    def dele_student(self):
        if not self.tree.selection():
            messagebox.showerror('抱歉', "你还没有选择，不能删除")
            return
        selectedItem = self.tree.selection()[0]
        # 获取选中对象的名字
        name = self.tree.item(selectedItem, 'values')[0]
        # 删除表格中的数据
        for item in self.tree.selection():
            self.tree.delete(item)
        # 删除数据库中的数据
        self.mysqlUtil.dele_student(name)

    # 新增学生到表格中
    def add_student(self):
        # 创建新窗口
        add_window = tk.Toplevel(self.master)
        add_window.title("新增学生")
        add_window.geometry("300x250")

        # 创建学生信息输入框和确定按钮等组件
        # 姓名标签和输入框
        label_name = tk.Label(add_window, text="姓名:", bg='pink')
        label_name.grid(column=1, row=1, padx=10, pady=5)
        entry_name = tk.Entry(add_window, width=30, bg='white', fg='black')
        entry_name.grid(column=2, row=1)

        # 年龄标签和输入框
        label_age = tk.Label(add_window, text="年龄:", bg='pink')
        label_age.grid(column=1, row=3, padx=10, pady=5)
        entry_age = tk.Entry(add_window, width=30, bg='white', fg='black')
        entry_age.grid(column=2, row=3)
        # 学号标签和输入框
        label_student_id = tk.Label(add_window, text="学号:", bg='pink')
        label_student_id.grid(column=1, row=4, padx=10, pady=5)
        entry_student_id = tk.Entry(add_window, width=30, bg='white', fg='black')
        entry_student_id.grid(column=2, row=4)

        # 确认按钮
        btn_confirm = tk.Button(add_window, text="确定", width=20, height=1,
                                command=lambda: (self.insertData([{"姓名": entry_name.get(),

                                                                   "年龄": entry_age.get(),
                                                                   "学号": entry_student_id.get(), }]),
                                                 self.mysqlUtil.add_student((entry_name.get(),

                                                                             int(entry_age.get()),
                                                                             entry_student_id.get())),
                                                 add_window.destroy()))

        btn_confirm.grid(column=2, row=7)

    # 修改学生信息函数
    def fix_student(self):
        if not self.tree.selection():
            messagebox.showerror('抱歉', "你还没有选择，不能修改")
            return
        selectedItem = self.tree.selection()[0]
        selected_values = self.tree.item(selectedItem, 'values')
        name = selected_values[0]
        # 创建新窗口
        fix_window = tk.Toplevel(self.master)
        fix_window.title("修改学生信息")
        fix_window.geometry("300x200")

        # 创建学生信息输入框和确定按钮等组件
        labels = ["姓名", "年龄", "学号"]
        entries = []
        for i, label_text in enumerate(labels):
            label = tk.Label(fix_window, text=label_text + ":", bg='pink')
            label.grid(column=1, row=i + 1)
            entry = tk.Entry(fix_window, width=30, bg='white', fg='black')
            entry.insert(0, selected_values[i])
            entry.grid(column=2, row=i + 1)
            entries.append(entry)

        # 确认按钮
        btn_confirm = tk.Button(fix_window, text="确定", width=20, height=1,
                                command=lambda: (
                                    self.tree.item(selectedItem, values=[entry.get() for entry in entries]),
                                    self.mysqlUtil.update_student(stu_tuple=tuple(entry.get() for entry in entries),
                                                                  name=name),
                                    fix_window.destroy()))
        btn_confirm.grid(column=2, row=7)

    # 查询学生信息函数
    def inquire_student(self):
        # 创建新窗口
        inquire_window = tk.Toplevel(self.master)
        inquire_window.title("查询学生信息")
        inquire_window.geometry("300x100")
        # 创建学生姓名输入框和确认按钮
        label_name = tk.Label(inquire_window, text="学生姓名:", bg='pink')
        label_name.grid(column=1, row=1, padx=10, pady=5)
        entry_name = tk.Entry(inquire_window, width=30, bg='white', fg='black')
        entry_name.grid(column=2, row=1)
        btn_confirm = tk.Button(inquire_window, text="确认", width=20, height=1,
                                command=lambda: self.display_student_info(entry_name.get(), inquire_window))
        btn_confirm.grid(column=2, row=2)

    # 显示学生信息函数
    def display_student_info(self, name, inquire_window):
        inquire_window.destroy()  # 关闭查询学生信息窗口

        # 检查是否输入了学生姓名
        if not name:
            messagebox.showerror('错误', "请输入学生姓名")
            return

        # 在主窗口中查找学生信息并显示
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if values[0] == name:
                messagebox.showinfo('查询结果',
                                    f"姓名: {values[0]}\n"

                                    f"年龄: {values[1]}\n"
                                    f"学号: {values[2]}\n"
                                    , icon=messagebox.INFO)
                return

        # 如果没有找到学生信息，则弹出提示框
        messagebox.showinfo('查询结果', "未找到该学生的信息")

    # 创建组件
    def createWidget(self):
        # 在窗体上创建frame组件
        self.frame = tk.Frame(self.master)
        self.frame.place(x=0, y=10, width=650, height=280)

        # 在frame容器中创建滚动条
        self.scrollBar = tk.Scrollbar(self.frame)
        self.scrollBar.pack(side=RIGHT, fill=Y)

        # 在Frame容器中使用TreeView组件实现表格功能
        # Treeview组件中，6列显示表头，带垂直滚动条
        self.tree = ttk.Treeview(self.frame,
                                 columns=('c1', 'c2', 'c3'),
                                 show='headings',
                                 yscrollcommand=self.scrollBar.set)

        # 设置每列宽度和对齐方式
        self.tree.column('c2', width=70, anchor='center')
        self.tree.column('c1', width=70, anchor='center')
        self.tree.column('c3', width=70, anchor='center')

        # 设置每列表头标题文本
        self.tree.heading('c1', text='姓名')

        self.tree.heading('c2', text='年龄')
        self.tree.heading('c3', text='学号')

        # 左对齐，纵向填充
        self.tree.pack(side=LEFT, fill=Y)

        # Treeview组件与垂直滚动条结合
        self.scrollBar.config(command=self.tree.yview)

        # 事件绑定
        self.tree.bind('<Double-1>', self.treeviewClick)
        # 新增按钮
        btnInsert = tk.Button(self.master,
                              text='新增学生',
                              command=self.add_student)
        btnInsert.place(x=20, y=310, width=120, height=20)
        # 删除按钮
        btnDelete = tk.Button(self.master,
                              text="删除学生",
                              command=self.dele_student)
        btnDelete.place(x=160, y=310, width=120, height=20)
        # 查询按钮
        btnInquire = tk.Button(self.master,
                               text="查询信息",
                               command=self.inquire_student)
        btnInquire.place(x=440, y=310, width=120, height=20)
        # 修改按钮
        btnFix = tk.Button(self.master,
                           text="修改信息",
                           command=self.fix_student)
        btnFix.place(x=300, y=310, width=120, height=20)


def showInfo():
    window = tk.Tk()
    window.title("学生信息界面")
    window.geometry("680x340+400+300")
    # 不允许改变窗口大小
    window.resizable(False, False)

    mysqlUtil = MysqlUtil()
    sv = Information(window, mysqlUtil)
    studentList = mysqlUtil.getInformation_dict()
    sv.insertData(studentList)

    # 运行程序，启动事件循环
    window.mainloop()


if __name__ == '__main__':
    showInfo()
