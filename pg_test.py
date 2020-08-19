import psycopg2
import psycopg2.extras

'''
host = 39.107.77.70
port = 5432
user = zengqi
password = 123456
database = testdb
'''
options = {
    'host': '39.107.77.70',
    'port': 5432,
    'user': 'zengqi',
    'password': '123456',
    'database': 'testdb',
}
connect = psycopg2.connect(**options)
cursor = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
'''
id = Column('id', Integer, primary_key=True)
    content = Column('content', String)
    # user_nickname = Column('user_nickname', String)
    # user_icon = Column('user_icon', String)
    user_id = Column('user_id', Integer, ForeignKey('user.id'))
    publish_time = Column('publish_time', DateTime, default=datetime.now())
    # 链接地址
    content_url = Column('content_url', String)
'''
# cursor.execute('SELECT id as f_id,content as f_content FROM moment;')
# cursor.execute('SELECT * FROM moment;')
# cursor.execute(
#     'create table en_study(_id integer primary key,'
#     'en_name varchar(20),'
#     'en_description varchar(100),'
#     'en_speaks varchar(20),'
#     'en_example varchar(100),'
#     'en_plural varchar(20));')
# connect.commit()
# cursor.execute("insert into moment values(6,'晚上天气不错',2,now(),'baidu.com');")
print(cursor.description)
# res = cursor.fetchone()
# res = cursor.fetchall()
# connect.commit()
# print(dict(res))
# for r in res:
#     print(dict(r))

# cursor.execute("insert into en_study values(1,"
#                "'explore',"
#                "'v.探索，探测,勘探, 勘查;',"
#                "'ɪkˈsplɔː(r)',"
#                "'I just wanted to explore Paris, read Sartre, listen to Sidney Bechet:我就想逛逛巴黎，读读萨特的作品，听听悉尼·贝谢的音乐。',"
#                "'explores')")
# connect.commit()
cursor.execute('select * from en_study;')
print(cursor.fetchall())
cursor.close()
connect.close()
