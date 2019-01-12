import cx_Oracle
import time
import datetime

sys = cx_Oracle.connect(
    'sys/oracle@localhost:1521/orcl', mode=cx_Oracle.SYSDBA)
cur = sys.cursor()

jjnm = cx_Oracle.connect('jjnm/oracle@localhost:1521/orcl')
curI = jjnm.cursor()

#-------USERS-------#
users_ST = """
        SELECT USERNAME, ACCOUNT_STATUS, EXPIRY_DATE, CREATED,
        USER_ID, DEFAULT_TABLESPACE
        FROM DBA_USERS"""

res = cur.execute(users_ST)

for row in res:
    if row[2] is not None:
        ed =  row[2].strftime('%d.%m.%Y')
    else:
        ed = row[2]
    query1 = """INSERT INTO USER_T(
        USER_ID,USERNAME,EXPIRATION_DATE,
        STATUS,CREATED_DATE)
        VALUES ('%d','%s',TO_DATE('%s','dd.mm.yyyy'),'%s',TO_DATE('%s','dd.mm.yyyy')) """ % (int(row[4]), row[0], ed, row[1], row[3].strftime('%d.%m.%Y'))
    queryU = """ UPDATE USER_T
                SET USER_ID = :id,
                USERNAME = :n,
                EXPIRATION_DATE = TO_DATE(:ed,'dd.mm.yyyy'),
                STATUS = :s,
                CREATED_DATE = TO_DATE(:cd,'dd.mm.yyyy')
                where USER_ID = :id
        """

    curI.execute(queryU,{'id':(int(row[4])),'n':row[0],'ed':ed,'s':row[1],'cd':row[3].strftime('%d.%m.%Y')})
    if curI.rowcount ==0:
       curI.execute(query1)


    jjnm.commit()


#--------ROLES--------#
roles_ST = """SELECT RLS.ROLE, RLS.ROLE_ID, RLS.AUTHENTICATION_TYPE, RLS.COMMON
                FROM DBA_ROLES RLS"""

res = cur.execute(roles_ST)

for row in res:
        queryU = """
                UPDATE ROLE_T
                        SET NAME_ROLE = :n,
                        COMMON = :c,
                        AUTHENTICATION_ROLE = :a
                WHERE ROLE_ID = :id
                """ 
        query = """INSERT INTO ROLE_T(
                ROLE_ID,NAME_ROLE,COMMON,
                AUTHENTICATION_ROLE)
                VALUES('%d','%s','%s','%s')""" % (int(row[1]), row[0], row[3], row[2])
        
        curI.execute(queryU,{'id':row[1],'n':row[0],'c':row[3],'a':row[2]})
        if curI.rowcount == 0:
                curI.execute(query)
        jjnm.commit()

#---------TABLESPACES---------#
tablespace_ST = """
                SELECT DISTINCT TBS.TABLESPACE_NAME,USG.USED_PERCENT,TBS.MAX_SIZE,TBS.STATUS,TBS.CONTENTS,
                USG.TABLESPACE_SIZE,(TABLESPACE_SIZE - USED_SPACE) AS FREE_SPACE
                FROM DBA_TABLESPACE_USAGE_METRICS  USG, DBA_TABLESPACES  TBS
                WHERE TBS.TABLESPACE_NAME = USG.TABLESPACE_NAME
                """
res = cur.execute(tablespace_ST)

for row in res: 
        queryU = """
                UPDATE TABLESPACE_T
                        SET SIZE_TABLESPACE = :si,
                        FREE_SPACE = :f,
                        USED = :u,
                        TYPE_TABLESPACE = :t,
                        MAX_SIZE = :m,
                        STATUS = :s
                WHERE NAME_TABLESPACE = :n
                """

        query = """INSERT INTO TABLESPACE_T(
                NAME_TABLESPACE,SIZE_TABLESPACE,FREE_SPACE,
                USED,TYPE_TABLESPACE,
                MAX_SIZE,STATUS)
                VALUES('%s','%d','%d','%d','%s','%d','%s')""" % (row[0],row[5], row[6], row[1],row[4],row[2],row[3])

        curI.execute(queryU,{'n':row[0],'si':row[5],'f':row[6],'u':row[1],'t':row[4],'m':row[2],'s':row[3]})
        if curI.rowcount == 0:
                curI.execute(query)
        jjnm.commit()

#-----------USER_HAS_ROLE----------#
tab_del = """DELETE FROM USER_HAS_ROLE"""
curI.execute(tab_del)

user_has_role_ST = """
                SELECT US.USER_ID, RLS.ROLE_ID
                FROM DBA_ROLES RLS
                INNER JOIN DBA_ROLE_PRIVS RLP
                ON RLS.ROLE = RLP.GRANTED_ROLE
                INNER JOIN DBA_USERS US
                ON RLP.GRANTEE = US.USERNAME
                """
res = cur.execute(user_has_role_ST)

for row in res:
    query = """INSERT INTO USER_HAS_ROLE(
                USER_ID,ROLE_ID)
                VALUES('%d','%d')""" % (row[0],row[1])
    curI.execute(query)
    jjnm.commit()

#--------TABLESPACES_USERS---------#
tabus_del = """DELETE FROM TABLESPACE_USER"""
curI.execute(tabus_del)

tabl_user_ST = """
        SELECT TBS.TABLESPACE_NAME,US.USER_ID
        FROM DBA_TABLESPACES  TBS, DBA_USERS US
        """
res = cur.execute(tabl_user_ST)

for row in res:
        existeUser = """
                SELECT USER_ID FROM USER_T
                WHERE USER_ID = '%d' """ % row[1]
        ex = curI.execute(existeUser)
        c = ex.fetchall()
        existTable = """
                SELECT NAME_TABLESPACE FROM TABLESPACE_T
                WHERE NAME_TABLESPACE = '%s' """ % row[0]
        ex2 = curI.execute(existTable)

        query = """INSERT INTO TABLESPACE_USER(
                NAME_TABLESPACE,USER_ID)
                VALUES('%s','%d')""" % (row[0],row[1])
        
        if (len(c)>0 and len(ex2.fetchall())>0):
                curI.execute(query)
                jjnm.commit()

#----------DATAFILES--------#
datafiles_ST = """
        SELECT FILE_NAME, FILE_ID, TABLESPACE_NAME, BYTES, STATUS, AUTOEXTENSIBLE,
        USER_BYTES
        FROM DBA_DATA_FILES   
        """

res = cur.execute(datafiles_ST)

for row in res:
        queryU = """
                UPDATE DATAFILE_T
                        SET NAME_DATAFILE = :n,
                        USER_BYTES = :u,
                        AUTOEXTENSIBLE = :a,
                        STATUS = :s,
                        BYTES = :b,
                        NAME_TABLESPACE = :nt
                WHERE DATAFILE_ID = :id
                """

        query = """INSERT INTO DATAFILE_T(
                DATAFILE_ID,NAME_DATAFILE,USER_BYTES,AUTOEXTENSIBLE,
                STATUS,BYTES,NAME_TABLESPACE)
                VALUES('%d','%s','%d','%s','%s','%d','%s')""" % (row[1],row[0],row[6],row[5],row[4],row[3],row[2])
        existe = """
                SELECT NAME_TABLESPACE FROM TABLESPACE_T
                where NAME_TABLESPACE = '%s' """ % row[2]

        ex = curI.execute(existe)
        if len(ex.fetchall())>0:
                curI.execute(queryU,{'id':row[1],'n':row[0],'u':row[6],'a':row[5],'s':row[4],'b':row[3],'nt':row[2]})
                if curI.rowcount == 0:
                        curI.execute(query)
                jjnm.commit()

#---------SESSIONS----------#
sessions_ST = """
        SELECT
        s.username,
        t.sid,
        s.serial#,
        s.seconds_in_wait,
        SUM(VALUE/100) as "cpu usage (seconds)",
        (select us.user_id from DBA_USERS us
        where(us.username = s.username)) AS USER_ID
        FROM
        v$session s,
        v$sesstat t,
        v$statname n
        WHERE
        t.STATISTIC# = n.STATISTIC#
        AND
        NAME like '%CPU used by this session%'
        AND
        t.SID = s.SID
        AND
        s.status='ACTIVE'
        AND
        s.username is not null
        GROUP BY username,t.sid,s.serial#,s.seconds_in_wait
        """

res = cur.execute(sessions_ST)

for row in res:
        queryU = """
                UPDATE SESSIONS
                        SET USERNAME = :u,
                        SERIAL = :s,
                        CPU = :c,
                        WAIT_SESSIONS = :ws,
                        USER_ID = :id
                WHERE SERIAL = :s
                """
        query = """INSERT INTO SESSIONS(USERNAME,SERIAL,
                                CPU,WAIT_SESSIONS,USER_ID)
                                VALUES('%s','%d','%d','%d','%d')""" % (row[0],row[2],row[4],row[3],row[5])
        rowCount = curI.execute(queryU,{'u':row[0],'s':row[2],'c':row[4],'ws':row[3],'id':row[5]})
        
        if curI.rowcount == 0:
                curI.execute(query)
        jjnm.commit()

#---------Memory--------#
memory_ST1 = """
        SELECT
        s.name,s.bytes/(1024*1024) MB 
        FROM
        v$sgastat s
        where s.name = 'buffer_cache'
        or s.name = 'shared_io_pool'
        """
memory_ST2 = """
        SELECT
        st.name,st.bytes/(1024*1024) MB
        FROM
        v_$sgainfo st
        where  st.name ='Java Pool Size'
                or st.name ='Streams Pool Size'
                or st.name ='Large Pool Size'
                or st.name ='Shared Pool Size'
        """
memory_ST3 = """
        SELECT
        sum(pga_used_mem)/(1024*1024)
        FROM 
        v$process p
        """
memory_ST4 = """
        select sum(max(bytes)/1024/1024) from dba_hist_sgastat where pool is not null group by pool
        """  
dataStorage_ST = """SELECT
                SUM((p.pga_max_mem)/1024/1024/1024) as DATA_STORAGE
                FROM
                v$process p"""

res = cur.execute(memory_ST1)
for row in res:
        if(row[0]=='buffer_cache'):
                buffer_cache = row[1]
        else:
                io_pool = row[1]

res = cur.execute(memory_ST2)

for row in res:
        if(row[0]=='Java Pool Size'):
                java_pool = row[1]
        if(row[0]=='Large Pool Size'):
                large_pool = row[1]
        if(row[0]=='Shared Pool Size'):
                shared_pool = row[1]
        if(row[0]=='Streams Pool Size'):
                streams_pool = row[1]
        
res = cur.execute(memory_ST3)

for row in res:
        pga = row[0]
res = cur.execute(memory_ST4)

for row in res:
        sga = row[0]
        
res = cur.execute(dataStorage_ST)

for row in res:
        data_storage = row[0]

queryU = """
        UPDATE MEMORY_T
                SET PGA = :p,
                DATA_STORAGE = :ds,
                SGA = :sga,
                SHARED_IO_POOL = :sp,
                BUFFER_CACHE_MEMORY = :bm,
                LARGE_POOL = :lp,
                JAVA_POOL = :jp,
                STREAM_POOL = :spo,
                NAME_TABLESPACE = :sys
                WHERE NAME_TABLESPACE = :sys
                """  
query = """INSERT INTO MEMORY_T(PGA,DATA_STORAGE,
                SGA,SHARED_IO_POOL,
                BUFFER_CACHE_MEMORY,LARGE_POOL,JAVA_POOL,
                STREAM_POOL,NAME_TABLESPACE)
                VALUES('%d','%d','%d','%d','%d','%d','%d','%d','%s')""" % (pga,data_storage,sga,shared_pool,buffer_cache,large_pool,java_pool,streams_pool,'SYSTEM')
        
curI.execute(queryU,{'p':pga,'ds':data_storage,'sga':sga,'sp':shared_pool,'bm':buffer_cache,'lp':large_pool,'jp':java_pool,'spo':streams_pool,'sys':'SYSTEM'})
if curI.rowcount==0:
   curI.execute(query)
jjnm.commit()
cur.close()
curI.close()
