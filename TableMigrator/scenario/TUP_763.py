import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import module.oracle_info as oracle 
import module.tibero_info as tibero
import module.execute_linux as execute

# Source DB - Oracle

oracle_conn = oracle.get_oracle_connection('192.168.17.31', 1521, 'tibero', 'tmax', 'cdb1')

oracle.create(oracle_conn, 'create table T283075_A(c1 number, c2 number, c3 number)')

oracle.insert(oracle_conn, 'insert into T283075_A values(1, 1, 1)')

# Tartgert DB - Tibero

tibero_conn = tibero.get_tibero_connection("{Tibero 7 ODBC Driver}", "192.168.17.33", 12000, "tibero", "tmax", "tibero")

tibero.create(tibero_conn, 'create table T283075_A(c1 number, c2 number, c3 number);')

# O2T 이관
tb_route = '/home/tibero7/table_migrator'

file = 'migrator.properties_O2T'

command = f'cd /home/tibero7/table_migrator && sh migrator.sh PROPERTY_FILE=./{file} SOURCE_TABLE="tibero.T283075_A(C1, C2, C3)" TARGET_TABLE="tibero.T283075_A("col1", "col2", "col3")" '

output, error = execute.execute_command_on_remote('192.168.17.33', 22, 'tibero7', 'tibero', command, file, tb_route)

print(output)

if 'java.lang.Exception: Target Table "T283075_A" has been specified invalid column(s) : "COL1", "COL2", "COL3"' in output:
    print("PASS")
else:
    print("FAIL")
    
# 초기화

oracle.drop(oracle_conn, 'drop table T283075_A')
tibero.drop(tibero_conn, 'drop table T283075_A;')

oracle_conn.close()
tibero_conn.close()