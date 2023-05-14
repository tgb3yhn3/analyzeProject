import sqlite3
db = sqlite3.connect('modelDB.db')
#execute sql
def execute_sql(sql):
    try:
        cursor= db.cursor()
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    finally:
        cursor.close()

#resetDB
def resetDB():
    sql="delete from model"
    execute_sql(sql)
    sql="delete from modelEfficacy"
    execute_sql(sql)
    sql="delete from nowUseModel"
    execute_sql(sql)
    sql="update sqlite_sequence SET seq = 0 where name ='model'"
    execute_sql(sql)
    sql="update sqlite_sequence SET seq = 0 where name ='nowUseModel'"
    execute_sql(sql)
def backUpDB():
    import time
    import shutil
    shutil.copyfile('modelDB.db', 'dbBackUp/modelDB'+time.strftime("%Y%m%d%H%M%S", time.localtime())+'.db')
if __name__=='__main__':
    backUpDB()
