import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import main.oracle_info as oracle 
import main.tibero_info as tibero
import main.execute_linux as execute

# Source DB - Oracle

oracle_conn = oracle.get_oracle_connection('192.168.17.31', 1521, 'tibero', 'tmax', 'cdb1')

oracle.alter(oracle_conn, 'alter session set "_ORACLE_SCRIPT"=true')

# tablespace 생성
oracle.create(oracle_conn, "create tablespace ts1_1 datafile 'ts1_2.tdf' size 200m autoextend on next 100m")
oracle.create(oracle_conn, "create tablespace ts2_1 datafile 'ts2_2.tdf' size 200m autoextend on next 100m")
oracle.create(oracle_conn, "create tablespace ts3_1 datafile 'ts3_2.tdf' size 200m autoextend on next 100m")
oracle.create(oracle_conn, "create tablespace ts4_1 datafile 'ts4_2.tdf' size 200m autoextend on next 100m")

oracle_create_query = '''
create table tbl_tup_1 (
 ROWCNT  number
, C1  number
, C2  varchar2(100)
, C3  char(10)
, C4  date not null
, C5  timestamp
, C6  interval day to second
, C7  interval year to month
, C8  raw(16)
, C9  nchar(15)
, C10 nvarchar2(10)
, C11 varchar(10)
, C12 blob
, c13 xmltype
) LOGGING
tablespace ts2_1 LOB ("C12") STORE AS (TABLESPACE ts3_1)
partition by range(C2)
subpartition by range(C3) (
partition p1 values less than (2010) tablespace ts1_1 (
subpartition s11 values less than (2010),
subpartition s12 values less than (2020),
subpartition s13 values less than (2050),
subpartition s14 values less than (2070),
subpartition s15 values less than (2080),
subpartition s16 values less than (2090),
subpartition s17 values less than (2100),
subpartition s18 values less than (maxvalue)),
partition p2 values less than (2020) tablespace ts1_1 (
subpartition s21 values less than (2010),
subpartition s22 values less than (2020),
subpartition s23 values less than (2050),
subpartition s24 values less than (2070),
subpartition s25 values less than (2080),
subpartition s26 values less than (2090),
subpartition s27 values less than (2100),
subpartition s28 values less than (maxvalue)),
partition p3 values less than (2040) tablespace ts1_1 (
subpartition s31 values less than (2010),
subpartition s32 values less than (2020),
subpartition s33 values less than (2050),
subpartition s34 values less than (2070),
subpartition s35 values less than (2080),
subpartition s36 values less than (2090),
subpartition s37 values less than (2100),
subpartition s38 values less than (maxvalue)),
partition p4 values less than (2060) tablespace ts1_1 (
subpartition s41 values less than (2010),
subpartition s42 values less than (2020),
subpartition s43 values less than (2050),
subpartition s44 values less than (2070),
subpartition s45 values less than (2080),
subpartition s46 values less than (2090),
subpartition s47 values less than (2100),
subpartition s48 values less than (maxvalue)),
partition p5 values less than (2080) tablespace ts1_1 (
subpartition s51 values less than (2010),
subpartition s52 values less than (2020),
subpartition s53 values less than (2050),
subpartition s54 values less than (2070),
subpartition s55 values less than (2080),
subpartition s56 values less than (2090),
subpartition s57 values less than (2100),
subpartition s58 values less than (maxvalue)),
partition p6 values less than (2090) tablespace ts1_1 (
subpartition s61 values less than (2010),
subpartition s62 values less than (2020),
subpartition s63 values less than (2050),
subpartition s64 values less than (2070),
subpartition s65 values less than (2080),
subpartition s66 values less than (2090),
subpartition s67 values less than (2100),
subpartition s68 values less than (maxvalue)),
partition p7 values less than (2100) tablespace ts1_1 (
subpartition s71 values less than (2010),
subpartition s72 values less than (2020),
subpartition s73 values less than (2050),
subpartition s74 values less than (2070),
subpartition s75 values less than (2080),
subpartition s76 values less than (2090),
subpartition s77 values less than (2100),
subpartition s78 values less than (maxvalue)),
partition p8 values less than (maxvalue) tablespace ts1_1
)
'''

oracle.create(oracle_conn, oracle_create_query)

oracle_create_index_query = '''
CREATE UNIQUE INDEX tbl_tup_1_I01_UK ON tbl_tup_1 (                          
c1 ASC,                                                    
c2 ASC,                                                   
c3 ASC                                                     
)                                                          
LOGGING                                                    
TABLESPACE ts4_1                              
NOPARALLEL                                                 
PCTFREE 10                                                 
INITRANS 2                                                 
LOCAL                                                      
(                                                          
partition p1 tablespace ts1_1,            
partition p2 tablespace ts1_1,            
partition p3 tablespace ts1_1,           
partition p4 tablespace ts1_1,            
partition p5 tablespace ts1_1,            
partition p6 tablespace ts1_1,            
partition p7 tablespace ts1_1,            
partition p8 tablespace ts1_1             
)
'''

oracle.create_index(oracle_conn, oracle_create_index_query)

oracle_insert_query = '''
insert into tbl_tup_1
( rowcnt
, C1
, C2
, C3
, C4
, C5
, C6
, C7
, C8
, C9
, C10
, C11
, C12
, c13
)
(
select
level
,level+1
,to_date(to_char(trunc(dbms_random.value(2000,2010)))||'0101','yyyymmdd')+trunc(dbms_random.value(1,365))
,to_date(to_char(trunc(dbms_random.value(2000,2100)))||'0101','yyyymmdd')+trunc(dbms_random.value(1,365))
,sysdate
,sysdate
,INTERVAL '30' MINUTE
, INTERVAL '01-02' YEAR TO MONTH
,SYS_GUID()
,'test'
,'test'
,'2000'
,lpad('A',4000,'A')
,  '<?xml version="1.0" encoding="UTF-8"?>
    <mods:beta xmlns:mods="test" xmlns:ndlklds="http://nl.go.kr/schema/license/terms/">
    <mods:alpha>
      <mods:a id="KAC202045778" authority="국립중앙도서관전거데이터" name="국립"> 이름 </mods:a>
      <mods:b name="국립2"> 이름2 </mods:b>
    </mods:alpha>
    <mods:alpha>
      <mods:c name="국립"> 이름 </mods:c>
      <mods:d name="국립2"> 이름2 </mods:d>
    </mods:alpha>
    </mods:beta>'
from dual connect by level <= 1000)
'''

oracle.insert(oracle_conn, oracle_insert_query)

# Target DB - Tibero

tibero_conn = tibero.get_tibero_connection("{Tibero 7 ODBC Driver}", "192.168.17.33", 12000, "tibero", "tmax", "tibero")

# tablespace 생성
tibero.create(tibero_conn, "create tablespace ts1_1 datafile 'ts1_2.tdf' size 200m autoextend on next 100m;")
tibero.create(tibero_conn, "create tablespace ts2_1 datafile 'ts2_2.tdf' size 200m autoextend on next 100m;")
tibero.create(tibero_conn, "create tablespace ts3_1 datafile 'ts3_2.tdf' size 200m autoextend on next 100m;")
tibero.create(tibero_conn, "create tablespace ts4_1 datafile 'ts4_2.tdf' size 200m autoextend on next 100m;")

tibero_create_query = '''
create table tbl_tup_1 (
 ROWCNT  number
, C1  number
, C2  varchar2(100)
, C3  char(10)
, C4  date not null
, C5  timestamp
, C6  interval day to second
, C7  interval year to month
, C8  raw(16)
, C9  nchar(15)
, C10 nvarchar2(10)
, C11 varchar(10)
, C12 blob
, c13 xmltype
) LOGGING
tablespace ts2_1 LOB ("C12") STORE AS (TABLESPACE ts3_1)
partition by range(C2)
subpartition by range(C3) (
partition p1 values less than (2010) tablespace ts1_1 (
subpartition s11 values less than (2010),
subpartition s12 values less than (2020),
subpartition s13 values less than (2050),
subpartition s14 values less than (2070),
subpartition s15 values less than (2080),
subpartition s16 values less than (2090),
subpartition s17 values less than (2100),
subpartition s18 values less than (maxvalue)),
partition p2 values less than (2020) tablespace ts1_1 (
subpartition s21 values less than (2010),
subpartition s22 values less than (2020),
subpartition s23 values less than (2050),
subpartition s24 values less than (2070),
subpartition s25 values less than (2080),
subpartition s26 values less than (2090),
subpartition s27 values less than (2100),
subpartition s28 values less than (maxvalue)),
partition p3 values less than (2040) tablespace ts1_1 (
subpartition s31 values less than (2010),
subpartition s32 values less than (2020),
subpartition s33 values less than (2050),
subpartition s34 values less than (2070),
subpartition s35 values less than (2080),
subpartition s36 values less than (2090),
subpartition s37 values less than (2100),
subpartition s38 values less than (maxvalue)),
partition p4 values less than (2060) tablespace ts1_1 (
subpartition s41 values less than (2010),
subpartition s42 values less than (2020),
subpartition s43 values less than (2050),
subpartition s44 values less than (2070),
subpartition s45 values less than (2080),
subpartition s46 values less than (2090),
subpartition s47 values less than (2100),
subpartition s48 values less than (maxvalue)),
partition p5 values less than (2080) tablespace ts1_1 (
subpartition s51 values less than (2010),
subpartition s52 values less than (2020),
subpartition s53 values less than (2050),
subpartition s54 values less than (2070),
subpartition s55 values less than (2080),
subpartition s56 values less than (2090),
subpartition s57 values less than (2100),
subpartition s58 values less than (maxvalue)),
partition p6 values less than (2090) tablespace ts1_1 (
subpartition s61 values less than (2010),
subpartition s62 values less than (2020),
subpartition s63 values less than (2050),
subpartition s64 values less than (2070),
subpartition s65 values less than (2080),
subpartition s66 values less than (2090),
subpartition s67 values less than (2100),
subpartition s68 values less than (maxvalue)),
partition p7 values less than (2100) tablespace ts1_1 (
subpartition s71 values less than (2010),
subpartition s72 values less than (2020),
subpartition s73 values less than (2050),
subpartition s74 values less than (2070),
subpartition s75 values less than (2080),
subpartition s76 values less than (2090),
subpartition s77 values less than (2100),
subpartition s78 values less than (maxvalue)),
partition p8 values less than (maxvalue) tablespace ts1_1
);
'''

tibero.create(tibero_conn, tibero_create_query)

tibero_create_index_query = '''
CREATE UNIQUE INDEX tbl_tup_1_I01_UK ON tbl_tup_1 (                          
c1 ASC,                                                    
c2 ASC,                                                   
c3 ASC                                                     
)                                                          
LOGGING                                                    
TABLESPACE ts4_1                              
NOPARALLEL                                                 
PCTFREE 10                                                 
INITRANS 2                                                 
LOCAL                                                      
(                                                          
partition p1 tablespace ts1_1,            
partition p2 tablespace ts1_1,            
partition p3 tablespace ts1_1,            
partition p4 tablespace ts1_1,            
partition p5 tablespace ts1_1,            
partition p6 tablespace ts1_1,            
partition p7 tablespace ts1_1,            
partition p8 tablespace ts1_1             
);
'''

tibero.create_index(tibero_conn, tibero_create_index_query)

# tablemigrator 수행

driver = "{Tibero 7 ODBC Driver}"
ip = "192.168.17.33"
port = "12000"
user = "tibero"
pw = "tmax"
sid = "tibero"

tb_route = '/home/tibero7/table_migrator'

# tablemigrator properties 기본값
file = 'migrator.properties_O2T'
 
command = f'cd /home/tibero7/table_migrator && sh migrator.sh PROPERTY_FILE=./{file} SOURCE_LOGIN_AS=normal SOURCE_TABLE=tibero.tbl_tup_1 TARGET_TABLE=tibero.tbl_tup_1 '

output, error = execute.execute_command_on_remote('192.168.17.33', 22, 'tibero7', 'tibero', command, file, tb_route)

test_query = "select count(*) from tibero.tbl_tup_1;"

if any(row[0] == 1000 for row in tibero.select(tibero_conn, test_query)):
    print("PASS")
else:
    print("FAIL")

# 초기화 작업
oracle.drop(oracle_conn, 'drop table tbl_tup_1')
oracle.drop(oracle_conn, 'drop tablespace ts1_1 including contents and datafiles')
oracle.drop(oracle_conn, 'drop tablespace ts2_1 including contents and datafiles')
oracle.drop(oracle_conn, 'drop tablespace ts3_1 including contents and datafiles')
oracle.drop(oracle_conn, 'drop tablespace ts4_1 including contents and datafiles')

tibero.drop(tibero_conn, 'drop table tbl_tup_1;')
tibero.drop(tibero_conn, 'drop tablespace ts1_1 including contents and datafiles;')
tibero.drop(tibero_conn, 'drop tablespace ts2_1 including contents and datafiles;')
tibero.drop(tibero_conn, 'drop tablespace ts3_1 including contents and datafiles;')
tibero.drop(tibero_conn, 'drop tablespace ts4_1 including contents and datafiles;')

oracle_conn.close()
tibero_conn.close()