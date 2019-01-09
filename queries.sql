/*Users*/
SELECT USERNAME, ACCOUNT_STATUS, EXPIRY_DATE, CREATED,
        USER_ID, DEFAULT_TABLESPACE
FROM DBA_USERS;


/*ROLES*/
SELECT US.USER_ID, RLS.ROLE_ID
FROM DBA_ROLES RLS
INNER JOIN DBA_ROLE_PRIVS RLP
ON RLS.ROLE = RLP.GRANTED_ROLE
INNER JOIN DBA_USERS US
ON RLP.GRANTEE = US.USERNAME;

SELECT RLS.ROLE, RLS.ROLE_ID, RLS.AUTHENTICATION_TYPE, RLS.COMMON
FROM DBA_ROLES RLS;
/*Tablespace*/
SELECT TBS.TABLESPACE_NAME,USG.USED_SPACE,USG.USED_PERCENT,TBS.MAX_SIZE,TBS.STATUS,TBS.CONTENTS,DF.FILE_NAME,DF.AUTOEXTENSIBLE, US.USER_ID,
(TABLESPACE_SIZE - USED_SPACE) AS FREE_SPACE
FROM DBA_TABLESPACE_USAGE_METRICS  USG, DBA_TABLESPACES  TBS, DBA_DATA_FILES  DF, DBA_USERS US
WHERE TBS.TABLESPACE_NAME = USG.TABLESPACE_NAME AND TBS.TABLESPACE_NAME = DF.TABLESPACE_NAME AND USG.TABLESPACE_NAME = DF.TABLESPACE_NAME;

SELECT DISTINCT TBS.TABLESPACE_NAME,USG.USED_PERCENT,TBS.MAX_SIZE,TBS.STATUS,TBS.CONTENTS,
                USG.TABLESPACE_SIZE,(TABLESPACE_SIZE - USED_SPACE) AS FREE_SPACE
                FROM DBA_TABLESPACE_USAGE_METRICS  USG, DBA_TABLESPACES  TBS
                WHERE TBS.TABLESPACE_NAME = USG.TABLESPACE_NAME;
                
SELECT TBS.TABLESPACE_NAME,US.USER_ID
FROM DBA_TABLESPACES  TBS, DBA_USERS US;

SELECT DISTINCT TBS.TABLESPACE_NAME,TBS.MAX_SIZE,TBS.STATUS,TBS.CONTENTS
FROM DBA_TABLESPACES  TBS, DBA_TABLESPACE_USAGE_METRICS  USG
WHERE TBS.TABLESPACE_NAME = USG.TABLESPACE_NAME;

select df.tablespace_name "Tablespace",
totalusedspace "Used MB",
(df.totalspace - tu.totalusedspace) "Free MB",
df.totalspace "Total MB",
round(100 * ( (df.totalspace - tu.totalusedspace)/ df.totalspace))
"Pct. Free"
from
(select tablespace_name,
round(sum(bytes) / 1048576) TotalSpace
from dba_data_files 
group by tablespace_name) df,
(select round(sum(bytes)/(1024*1024)) totalusedspace, tablespace_name
from dba_segments 
group by tablespace_name) tu
where df.tablespace_name = tu.tablespace_name ;

/*DataFiles*/
SELECT FILE_NAME, FILE_ID, TABLESPACE_NAME, BYTES, STATUS, AUTOEXTENSIBLE,
USER_BYTES
FROM DBA_DATA_FILES;



/*Sessions*/
select distinct serial# from v$session;

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
GROUP BY username,t.sid,s.serial#,s.seconds_in_wait;

/*Memory*/
SELECT
    SUM((p.pga_max_mem)/1024/1024/1024) as DATA_STORAGE
    FROM
    v$process p;
SELECT
    s.value as SGA_VALUE,
    p.pga_max_mem as DATA_STORAGE
    --p.pname as PGA
FROM 
    v$sgastat st,
    v$sga s,
    v$process p;
SELECT
    sum(pga_used_mem)/(1024*1024)
FROM 
    v$process p;
select * 
from(
   select 
      name, bytes/(1024*1024) MB 
   from 
      v$sgastat 
   where 
      pool ='shared pool' 
   order by 
      bytes desc
   ) 
where rownum < 20;
select * from v$java_pool_advice;
select (sum(value))/(1024*1024) from v$sga;
select name,value/(1024*1024) from v$pgastat; 
select * --value/(1024*1024)
FROM
    v$statname stat1
    where stat1.name = 'session pga memory';

SELECT
     s.pool, s.name, s.bytes/(1024*1024) MB 
FROM
     v$sgastat s
where s.name = 'buffer_cache'
      or s.name = 'shared_io_pool';
    
SELECT
    st.name,st.bytes/(1024*1024) MB
FROM
    v_$sgainfo st
    where  st.name ='Java Pool Size'
        or st.name ='Streams Pool Size'
        or st.name ='Large Pool Size'
        or st.name ='Shared Pool Size';
        
select sum(value)/1024/1024 Total_size_In_MB from V$sga;
Select ((select sum(sg.value)/1024/1024 Total_size_In_MB from V$sga sg ) - sum(s.bytes/1024/1024))
     From V$sgastat s
     Where Name Like '%free memory%';
     
select name,value/(1024*1024) from v$pgastat where name='total PGA inuse';
select bytes/(1024*1024) from v$sgastat;

 select sum(max(bytes)/1024/1024) from dba_hist_sgastat where pool is not null group by pool;
