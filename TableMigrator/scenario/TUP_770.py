import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import module.tibero_module as tibero
import module.shell_module as execute

tibero_conn = tibero.get_tibero_connection("{Tibero 7 ODBC Driver}", "192.168.17.33", 12000, "tibero", "tmax", "tibero")

# Source DB - Tibero
file = 'TUP_770_sr.sh'
execute.execute_sql('192.168.17.33', 22, 'tibero7', 'tibero', file)

# Tartgert DB - Tibero
file = 'TUP_770_tg.sh'
execute.execute_sql('192.168.17.33', 22, 'tibero7', 'tibero', file)

# T2T 이관
tb_route = '/home/tibero7/table_migrator'
file = 'migrator.properties_T2T'

commands = {
    1: 'SOURCE_SCHEMA=SRC283075 SOURCE_TABLE="t283075_a(c1), t283075_b" TARGET_SCHEMA=TRG283075 TARGET_TABLE="t283075_2(col1), t283075_2" ',
    2: 'SOURCE_SCHEMA=SRC283075 SOURCE_TABLE="t283075_a, t283075_b(c1)" TARGET_SCHEMA=TRG283075 TARGET_TABLE="t283075_2(col1), t283075_2" ',
    3: 'SOURCE_SCHEMA=SRC283075 SOURCE_TABLE="t283075_a, t283075_b(c1)" TARGET_SCHEMA=TRG283075 TARGET_TABLE="t283075_2, t283075_2(col1)" '
}

results = []

for row in commands:
    command = f'cd /home/tibero7/table_migrator && sh migrator.sh PROPERTY_FILE=./{file} {commands[row]}'

    output, error = execute.execute_shell('192.168.17.33', 22, 'tibero7', 'tibero', command, file, tb_route)
    
    print(output)
    if row == 1:
        if ('aaaaaaaaaa', '30.0', 'fourty') in tibero.select(tibero_conn, 'SELECT col1, col3, col4 FROM TRG283075.t283075_2'):
            results.append(f"TC {row} : PASS")
        else: results.append(f"TC {row} : FAIL")
    elif row == 2:
        if 'java.lang.Exception: The number of source table column and target table column are not matched.' in output:
            results.append(f"TC {row} : PASS")
        else: results.append(f"TC {row} : FAIL")
    elif row == 3:
        if 'aaaaaaaaaa' in tibero.select(tibero_conn, 'SELECT col1 FROM TRG283075.t283075_2'):
            results.append(f"TC {row} : PASS")
        else: results.append(f"TC {row} : FAIL")
    else:
        results.append(f"TC {row} : FAIL, retry test")
    tibero.truncate(tibero_conn, 'truncate table TRG283075.t283075_2')
        
for row in results:
    print(row)
    
# 초기화
# tibero.drop_user(tibero_conn, 'src283075')
# tibero.drop_user(tibero_conn, 'trg283075')

tibero_conn.close()