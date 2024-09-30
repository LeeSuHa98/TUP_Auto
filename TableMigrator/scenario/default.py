import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import module.oracle_info as oracle 
import module.tibero_info as tibero
import module.execute_linux as execute

# oracle 접속 정보
def oracle_remote():
    user = ""
    pw = ""
    ip = ""
    port = ""
    sid = ""

    create_query = '''
    '''

    oracle_conn = oracle.get_oracle_connection(ip, port, user, pw, sid)
    
    oracle.create(oracle_conn, create_query)
    
    # 삽입할 데이터를 튜플 형태로 준비
    bind_values = [
        
    ]
    
    insert_query = ""
    
    oracle.insert(oracle_conn, bind_values, insert_query)
    
    # 접속 종료
    oracle_conn.close()

# Tibero 접속
def tibero_remote():
    
    # 기본 접속 정보
    driver = "{Tibero 7 ODBC Driver}"
    ip = ""
    port = ""
    user = ""
    pw = ""
    sid = ""

    tibero_conn = tibero.get_tibero_connection(driver, ip, port, user, pw, sid)
    
    drop_query = ""
    
    tibero.drop(tibero_conn, drop_query)
    
    tibero_conn.close()

# tablemigrator 수행
def run_tablemigrator():
    host = ''
    port = 22
    tb_user = ''
    tb_pw = ''

    tb_route = '/home/tibero7/table_migrator'
    
    # tablemigrator properties 기본값
    file = 'migrator.properties_TUP'
    
    # properties 옵션 추가 값
    add_properties = ''
    
    # 최종 tablemigrator properties
    command = f'cd /home/tibero7/table_migrator && sh migrator.sh PROPERTY_FILE=./{file} {add_properties}'
    
    print(command)
    output, error = execute.execute_command_on_remote(host, port, tb_user, tb_pw, command, file, tb_route)

    print("Output:", output)
    print("Error:", error)
    

# Source DB Schema 수행
oracle_remote()

# Target DB Schema 수행
tibero_remote()

# table migrator 수행
# properties 값 파라미터로 입력 받기
run_tablemigrator()