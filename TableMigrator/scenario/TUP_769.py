import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import module.tibero_module as tibero
import module.shell_module as execute

tibero_conn = tibero.get_tibero_connection("{Tibero 7 ODBC Driver}", "192.168.17.33", 12000, "tibero", "tmax", "tibero")

# Source DB - Tibero
file = 'TUP_769_sr.sh'
execute.execute_sql('192.168.17.33', 22, 'tibero7', 'tibero', file)

# Tartgert DB - Tibero
file = 'TUP_769_tg.sh'
execute.execute_sql('192.168.17.33', 22, 'tibero7', 'tibero', file)

# T2T 이관
tb_route = '/home/tibero7/table_migrator'
file = 'migrator.properties_T2T'
command = f'cd /home/tibero7/table_migrator && sh migrator.sh PROPERTY_FILE=./{file} SOURCE_SCHEMA=SRC283075 SOURCE_TABLE=t283075_a TARGET_SCHEMA=TRG283075 TARGET_TABLE=t283075_2'
output, error = execute.execute_shell('192.168.17.33', 22, 'tibero7', 'tibero', command, file, tb_route)

if('java.lang.Exception: The number of source table column and target table column are not matched.' in output):
    print("PASS")
elif('java.lang.ArrayIndexOutOfBoundsException' in output):
    print("FAIL : Operate with the pre-patch scenario")
else:
    print("FAIL")
    
# 초기화
tibero.drop_user(tibero_conn, 'src283075')
tibero.drop_user(tibero_conn, 'trg283075')

tibero_conn.close()