from pymysql import Connection

conn = Connection(
    host='localhost',
    port=3306,
    user='root',
    password='136479',
    autocommit=True
)
cursor = conn.cursor()
# cursor.execute('create database school')
cursor.execute('use school')
# cursor.execute('create table student(id int,name varchar(10),sex varchar(10),age int);')
sql = f'insert into student(name,age,sex) values({'student_name'},student_age,{'student_sex'})'
