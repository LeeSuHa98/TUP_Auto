import sys
import os

# 현재 파일 기준으로 상위 디렉토리의 main 경로를 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import module.execute_linux as execute

# tablemigrator 수행
def run_tablemigrator():
    host = '192.168.17.33'
    port = 22
    tb_user = 'tibero7'
    tb_pw = 'tibero'

    tb_route = '/home/tibero7/table_migrator'
    
    # tablemigrator properties 기본값
    file = 'migrator.properties_T2T'
    
    # properties 옵션 추가 값
    add_properties = 'SOURCE_TABLE=tibero.TEST_749 TARGET_TABLE=tibero.DUAL'
    
    # 최종 tablemigrator properties
    command = f'cd /home/tibero7/table_migrator && sh migrator.sh PROPERTY_FILE=./{file} {add_properties}'

    output, error = execute.execute_command_on_remote(host, port, tb_user, tb_pw, command, file, tb_route)

    print("Output:", output)
    print("Error:", error)
    
    return output

# table migrator 수행
# properties 값 파라미터로 입력 받기

result = run_tablemigrator()

if 'Invalid Source Table' in result:
    print('PASS')
else:
    print('FAIL')