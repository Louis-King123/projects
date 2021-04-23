import cx_Oracle
# 连接数据库，下面括号里内容根据自己实际情况填写
# conn = cx_Oracle.connect('用户名/密码@IP:端口号/SERVICE_NAME')
# conn = cx_Oracle.connect('账号', '密码', 'ip:端口/数据库名称')
conn = cx_Oracle.connect('system', 'oracle', 'xmsso.com:49161/XE')
# 使用cursor()方法获取操作游标
cursor = conn.cursor()
# 使用execute方法执行SQL语句
result = cursor.execute('Select * from all_users')
# 使用fetchone()方法获取一条数据
# data=cursor.fetchone()

# 获取所有数据
all_data = cursor.fetchall()

# 获取部分数据，8条
# many_data=cursor.fetchmany(8)

print(all_data)

conn.close()
