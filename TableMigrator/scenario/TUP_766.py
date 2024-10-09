import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import module.oracle_module as oracle 
import module.tibero_module as tibero
import module.shell_module as execute

# Source DB - Oracle

oracle_conn = oracle.get_oracle_connection('192.168.17.31', 1521, 'tibero', 'tmax', 'cdb1')

oracle.create(oracle_conn, 'create table T283075_A(c1 number, c2 number, c3 number)')

oracle.insert(oracle_conn, 'insert into T283075_A values(10, 20, 30)')

# Tartgert DB - Tibero

tibero_conn = tibero.get_tibero_connection("{Tibero 7 ODBC Driver}", "192.168.17.33", 12000, "tibero", "tmax", "tibero")

tibero.create(tibero_conn, 'create table T283075_A(col1 number, col2 number, col3 number);')

# O2T 이관

tb_route = '/home/tibero7/table_migrator'

file = 'migrator.properties_O2T'

# 다양한 Test Case 가 필요한 경우 directory 로 만들어서 중복을 줄이고 유지보수 높임

commands = {
    1: 'SOURCE_TABLE="tibero.T283075_A" TARGET_TABLE="tibero.T283075_A("col1", "col2", "col3")" ',
    2: 'SOURCE_TABLE="tibero.T283075_A" TARGET_TABLE="tibero.T283075_A("col3", "col2", "col1")" ',
    3: 'SOURCE_TABLE="tibero.T283075_A" TARGET_TABLE="tibero.T283075_A("col3", "col1")" ',
    4: 'SOURCE_TABLE="tibero.T283075_A(C1, C2, C3)" TARGET_TABLE="tibero.T283075_A" ',
    5: 'SOURCE_TABLE="tibero.T283075_A(C3, C2, C1)" TARGET_TABLE="tibero.T283075_A" ',
    6: 'SOURCE_TABLE="tibero.T283075_A(C3, C1)" TARGET_TABLE="tibero.T283075_A" '
}

results = []

for row in commands:
    command = f'cd /home/tibero7/table_migrator && sh migrator.sh PROPERTY_FILE=./{file} {commands[row]}'

    output, error = execute.execute_shell('192.168.17.33', 22, 'tibero7', 'tibero', command, file, tb_route)

    if row == 1 and tibero.select(tibero_conn, 'select * from tibero.T283075_A')[0] == (10, 20, 30):
        results.append(f"TC {row} : PASS")
    elif row == 2 and tibero.select(tibero_conn, 'select * from tibero.T283075_A')[1] == (30, 20, 10):
        results.append(f"TC {row} : PASS")
    elif row == 3 and 'java.lang.Exception: The number of source table column and target table column are not matched.' in output:
        results.append(f"TC {row} : PASS")
    elif row == 4 and tibero.select(tibero_conn, 'select * from tibero.T283075_A')[2] == (10, 20, 30):
        results.append(f"TC {row} : PASS")
    elif row == 5 and tibero.select(tibero_conn, 'select * from tibero.T283075_A')[3] == (30, 20, 10):
        results.append(f"TC {row} : PASS")
    elif row == 6 and 'java.lang.Exception: The number of source table column and target table column are not matched.' in output:
        results.append(f"TC {row} : PASS")
    else:
        results.append(f"TC {row} : FAIL")
        
# 초기화

for row in results:
    print(row)
    
oracle.drop(oracle_conn, 'drop table T283075_A')
tibero.drop(tibero_conn, 'drop table T283075_A;')

oracle_conn.close()
tibero_conn.close()