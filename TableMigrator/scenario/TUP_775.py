import sys
import os

import oracledb

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import module.oracle_module as oracle 
import module.tibero_module as tibero
import module.shell_module as execute

# Source DB - Oracle

oracle_conn = oracle.get_oracle_connection('192.168.17.31', 1521, 'sys', 'tibero', 'cdb1', oracledb.AUTH_MODE_SYSDBA)

oracle.create_user(oracle_conn, 'U292622_SRC', 'tmax')

for row in oracle.select(oracle_conn, "select * from all_users where username like '%U292622%'"):
    print(row)

oracle.create(oracle_conn, 'create table U292622_SRC.T292622(a varchar(10), b number)')
# oracle.create(oracle_conn, 'create table U292622_SRC.T292622_2(a varchar(10), b number)')

oracle.insert(oracle_conn, 'insert into U292622_SRC.T292622 select level, level from dual connect by level < 1000')
# oracle.insert(oracle_conn, 'insert into U292622_SRC.T292622_2 select level, level from dual connect by level < 1000')
for row in oracle.select(oracle_conn, "select * from U292622_SRC.T292622"):
    print(row)
# oracle.create(oracle_conn, 'create or replace view U292622_SRC.v292622 as select * from U292622_SRC.T292622_1 union all select * from U292622_SRC.T292622_2')

# Tartgert DB - Tibero

tibero_conn = tibero.get_tibero_connection("{Tibero 7 ODBC Driver}", "192.168.17.33", 12000, "tibero", "tmax", "tibero")

tibero.create_user(tibero_conn, 'U292622_TAR', 'tmax')

tibero.create(tibero_conn, 'create table U292622_TAR.T292622 (a varchar(10), b number);')

# O2T 이관
tb_route = '/home/tibero7/table_migrator'

file = 'migrator.properties_O2T'

command = f'cd /home/tibero7/table_migrator && sh migrator.sh PROPERTY_FILE=./{file} SOURCE_USER=U292622_SRC SOURCE_PASSWORD=tmax SOURCE_LOGIN_AS=sysdba SOURCE_TABLE="T292622" TARGET_USER=U292622_TAR TARGET_PASSWORD=tmax TARGET_TABLE="U292622_TAR.T292622" SOURCE_TABLE_DEDUPLICATE=Y'

output, error = execute.execute_shell('192.168.17.33', 22, 'tibero7', 'tibero', command, file, tb_route)

print(output)

# 초기화
oracle.drop_user(oracle_conn, 'U292622_SRC')
tibero.drop_user(tibero_conn, 'U292622_TAR')

oracle_conn.close()
tibero_conn.close()