CREATE TABLESPACE aebd_trabalho 
    DATAFILE '\u01\app\oracle\oradata\orcl12\orcl\aebd_trabalho01.dbf' SIZE 500M;
    
CREATE TEMPORARY TABLESPACE aebd_trabalho_temp
    TEMPFILE '\u01\app\oracle\oradata\orcl12\orcl\aebd_trabalho_temp01.dbf' 
    SIZE 250M
    AUTOEXTEND on;    
    
GRANT RESOURCE TO jjnm;
GRANT CONNECT TO jjnm;
GRANT DBA TO jjnm;
