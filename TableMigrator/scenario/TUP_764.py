import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import module.oracle_module as oracle 
import module.tibero_module as tibero
import module.shell_module as execute

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

command_tc1 = f'cd /home/tibero7/table_migrator && sh migrator.sh PROPERTY_FILE=./{file} SOURCE_TABLE="tibero.T283075_A(C1, C2, C3)abc()" TARGET_TABLE="tibero.T283075_A(c1, c2, c3)" '

output, error = execute.execute_shell('192.168.17.33', 22, 'tibero7', 'tibero', command_tc1, file, tb_route)

if 'Invalid Source Table Name : "tibero.T283075_A(C1, C2, C3)abc()" error occurs at 1:28 mismatched input' in error:
    print("TC 1 : PASS")
else:
    print("TC 1 : FAIL")
    
command_tc2 = f'cd /home/tibero7/table_migrator && sh migrator.sh PROPERTY_FILE=./{file} SOURCE_TABLE="tibero.T283075_A(C1, C2, C3)" TARGET_TABLE="tibero.T283075_A(c1, c2, c3)abc()" '

output, error = execute.execute_shell('192.168.17.33', 22, 'tibero7', 'tibero', command_tc2, file, tb_route)

if 'Invalid Target Table Name : "tibero.T283075_A(c1, c2, c3)abc()" error occurs at 1:28 mismatched input' in error:
    print("TC 2 : PASS")
else:
    print("TC 2 : FAIL")
    
# 초기화

oracle.drop(oracle_conn, 'drop table T283075_A')
tibero.drop(tibero_conn, 'drop table T283075_A;')

oracle_conn.close()
tibero_conn.close()