# 作   者：陈中超
# 开发日期:2023/10/9

from pymysql import Connection


class MysqlUtil:
    def __init__(self):
        # 获取到mysql数据库的连接对象
        self.cone = Connection(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 默认端口为3306
            user='root',  # 默认账户名
            password='czc',  # 登录密码
            database="student_py"
        )

    def getInformation_dict(self):
        """
        获取数据库信息，返回学生字典列表
        :param cone: 数据库连接对象
        :return: dict
        """
        self.cursor = self.cone.cursor()
        self.cone.select_db("student_py")

        # 使用游标对象执行执行sql语句
        self.cursor.execute("SELECT *FROM student")
        # 获取查询结果
        results = self.cursor.fetchall()

        studentList = []
        for result in results:
            student_dict = {
                "姓名": result[0],
                "年龄": result[1],
                "学号": result[2],

            }
            studentList.append(student_dict)
        return studentList

    # 删除数据库中的指定学生
    def dele_student(self, name: str):
        self.cursor.execute(f"DELETE FROM student WHERE name='%s'" % name)
        self.cone.commit()

    # 新增学生到数据库中
    def add_student(self, stu_tuple: tuple):
        self.cursor.execute(f"INSERT INTO student VALUES('%s','%d',%s)" % stu_tuple)
        self.cone.commit()

    # 修改数据库中的学生信息
    def update_student(self, name: str, stu_tuple: tuple):
        self.cursor.execute(f"UPDATE student SET `name` = '{stu_tuple[0]}',"
                            f"`age` = {stu_tuple[1]},"
                            f"`id` = '{stu_tuple[2]}',"
                            f" WHERE `name` = '{name}'")
        self.cone.commit()


if __name__ == '__main__':
    cone = MysqlUtil()
    studentList = cone.getInformation_dict()
    print(studentList)
