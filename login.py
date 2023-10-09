# 作   者：陈中超
# 开发日期:2023/10/9
import tkinter as tk
import pymysql
import main_window

window = tk.Tk()


def login():
    username = entry_username.get()
    password = entry_password.get()

    # 连接MySQL数据库
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="czc",
        database="student_py"
    )

    mycursor = mydb.cursor()

    # 查询用户名和密码是否匹配
    mycursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    result = mycursor.fetchone()

    if result:
        label_result.config(text="登录成功！", fg="green")
        # 进入主菜单或其他操作
        window.destroy()
        main_window.showInfo()
    else:
        label_result.config(text="用户名或密码错误，请重新登录。", fg="red")


# 创建窗口

window.title("学生信息管理系统")
window.geometry("300x200")

# 创建用户名标签和输入框
label_username = tk.Label(window, text="用户名：")
label_username.pack()
entry_username = tk.Entry(window)
entry_username.pack()

# 创建密码标签和输入框
label_password = tk.Label(window, text="密码：")
label_password.pack()
entry_password = tk.Entry(window, show="*")
entry_password.pack()

# 创建登录按钮
button_login = tk.Button(window, text="登录", command=login)
button_login.pack()

# 创建用于显示登录结果的标签
label_result = tk.Label(window)
label_result.pack()

# 运行窗口
window.mainloop()
