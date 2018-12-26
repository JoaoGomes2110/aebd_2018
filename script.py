import cx_Oracle
import time
import datetime

sys = cx_Oracle.connect('sys/oracle@localhost:1521/orcl',mode=cx_Oracle.SYSDBA)
cur = sys.cursor()

jjnm = cx_Oracle.connect('jjnm/oracle@localhost:1521/orcl')
curI = jjnm.cursor()

statement = """
        SELECT USERNAME, ACCOUNT_STATUS, EXPIRY_DATE, CREATED,
        USER_ID, DEFAULT_TABLESPACE
        FROM DBA_USERS"""

res = cur.execute(statement)

def convert(s):
    if s is not None:
        return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

for row in res:
    print(row[3])

    data =(int(row[4]),row[0],(row[2]),row[1],(row[3]))

    curI.execute("""INSERT INTO USER_T(
         USER_ID,USERNAME,EXPIRATION_DATE,
         STATUS,CREATED_DATE)
         VALUES (%d,%s,%s,%s,%s) """,data)


cur.close()
curI.close()
