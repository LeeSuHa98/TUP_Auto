import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import module.tibero_info as tibero
import module.execute_linux as execute

# Source DB - Tibero
tibero_conn = tibero.get_tibero_connection("{Tibero 7 ODBC Driver}", "192.168.17.33", 12000, "tibero", "tmax", "tibero")

tibero.create_user(tibero_conn, 'src283075', 'tmax')
tibero.create(tibero_conn, 'create table src283075.t1(col1 number, col2 number, col3 number);')
tibero.insert(tibero_conn, 'insert into src283075.t1 values(10, 20, 30);')

tibero.create(tibero_conn, 'create table src283075.t2(col11 number, col22 number, col33 number);')
tibero.insert(tibero_conn, 'insert into src283075.t2 values(100, 200, 300);')

tibero.create(tibero_conn, 'create table src283075.t3("col1" number, "col2" number, "col3" number);')
tibero.insert(tibero_conn, 'insert into src283075.t3 values(1, 2, 3);')

# Tartgert DB - Tibero
tibero.create_user(tibero_conn, 'trg283075', 'tmax')
tibero.create(tibero_conn, 'create table trg283075.t1(col1 number, col2 number, col3 number);')
tibero.create(tibero_conn, 'create table trg283075.t2(col11 number, col22 number, col33 number);')
tibero.create(tibero_conn, 'create table trg283075.t3("col1" number, "col2" number, "col3" number);')

# T2T 이관
tb_route = '/home/tibero7/table_migrator'

file = 'migrator.properties_T2T'

command = f'cd /home/tibero7/table_migrator && sh migrator.sh PROPERTY_FILE=./{file} SOURCE_USER=src283075 SOURCE_TABLE=\'t1(COL1, COL2, COL3), t2, t3("col1", "col2", "col3")\' TARGET_USER=trg283075 TARGET_TABLE=\'t1(col2, col1, col3), t2, t3("col2", "col1", "col3")\' '

output, error = execute.execute_command_on_remote('192.168.17.33', 22, 'tibero7', 'tibero', command, file, tb_route)

if (
    tibero.select(tibero_conn, 'select * from trg283075.t1')[0] == (20, 10, 30) and 
    tibero.select(tibero_conn, 'select * from trg283075.t2')[0] == (100, 200, 300) and 
    tibero.select(tibero_conn, 'select * from trg283075.t3')[0] == (2, 1, 3)
):
    print('PASS')
else:
    print("FAIL")
        
# 초기화
tibero.drop_user(tibero_conn, 'src283075')
tibero.drop_user(tibero_conn, 'trg283075')

tibero_conn.close()