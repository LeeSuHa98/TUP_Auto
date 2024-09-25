import sys
import os

# 현재 파일의 상위 디렉토리인 project를 PYTHONPATH에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import paramiko
import main.oracle_info as oracle 
import main.tibero_info as tibero

# 리눅스 원격 접속 함수
def execute_command_on_remote(host, port, username, password, command, file, tb_route):
    # SSH 클라이언트 생성
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 원격 서버에 SSH 연결
        ssh.connect(host, port=port, username=username, password=password)

        # SFTP 파일 전송
        sftp = ssh.open_sftp()

        # tablemigrator 에 필요한 properties 파일 원격 서버에 전송
        current_dir = os.path.dirname(os.path.abspath(__file__))
        local_file = os.path.join(current_dir, 'properties', file)  # Python 코드가 실행되는 로컬 파일 경로
        if not os.path.exists(local_file):
            raise FileNotFoundError(f"File not found: {local_file}")
        
        remote_file = tb_route + '/' + file
        
        sftp.put(local_file, remote_file)
        
        sftp.close()
        
        # 명령어 실행
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # 명령어 출력 및 에러 가져오기
        output = stdout.read().decode()
        error = stderr.read().decode()
                
        # 출력 반환
        return output, error
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # SSH 연결 종료
        ssh.close()
        
        
# oracle 접속 정보
def oracle_remote():
    user = "tibero"
    pw = "tmax"
    ip = "192.168.17.31"
    port = "1521"
    sid = "cdb1"

    create_query = '''
    create table mig_test(c1 number, c2 char(10), c3 varchar2(10) )
    '''
    
    oracle_conn = oracle.get_oracle_connection(ip, port, user, pw, sid)
    
    oracle.drop(oracle_conn, 'drop table mig_test purge')
    oracle.create(oracle_conn, create_query)
    
    # 삽입할 데이터를 튜플 형태로 준비
    bind_values = [
        (1, 'abc      ', 'def'),
        (2, ' ', ' '),
        (3, None, None)
    ]

    insert_query = "insert into mig_test values (:1, :2, :3)"
    
    oracle.insert(oracle_conn, bind_values, insert_query)

    oracle.select(oracle_conn, " select c3, length(c3) c3_len, nvl(c3, 'NULL') c3_nvl from mig_test")
    oracle_conn.close()


# Tibero 접속
def tibero_remote():
    
    # 기본 접속 정보
    driver = "{Tibero 7 ODBC Driver}"
    ip = "192.168.17.33"
    port = "12000"
    user = "tibero"
    pw = "tmax"
    sid = "tibero"

    tibero_conn = tibero.get_tibero_connection(driver, ip, port, user, pw, sid)

    tibero.truncate(tibero_conn, "drop table t270457_y;")
    tibero.create(tibero_conn, "create table t270457_y(c1 number, c2 varchar(10), c3 varchar2(10));")
    
    tibero.truncate(tibero_conn, "drop table t270457_n;")
    tibero.create(tibero_conn, "create table t270457_n(c1 number, c2 varchar(10), c3 varchar2(10));")
    
    tibero.truncate(tibero_conn, "drop table t270457_x;")
    tibero.create(tibero_conn, "create table t270457_x(c1 number, c2 varchar(10), c3 varchar2(10))")
    
    tibero_conn.close()
    
# Source DB Schema 수행
oracle_remote()

# Target DB Schema 수행
tibero_remote()

# Test Scenario

driver = "{Tibero 7 ODBC Driver}"
ip = "192.168.17.33"
port = "12000"
user = "tibero"
pw = "tmax"
sid = "tibero"

tb_route = '/home/tibero7/table_migrator'

# tablemigrator properties 기본값
file = 'migrator.properties_TUP_750'
 
# properties 옵션 추가 값
add_properties = [
    'INSERT_ZERO_LENGTH_STRING_AS_NULL=Y SOURCE_TABLE=mig_test TARGET_TABLE=t270457_y SOURCE_LOGIN_AS=normal',
    'INSERT_ZERO_LENGTH_STRING_AS_NULL=N SOURCE_TABLE=mig_test TARGET_TABLE=t270457_n SOURCE_LOGIN_AS=normal',
    'SOURCE_TABLE=mig_test TARGET_TABLE=t270457_x SOURCE_LOGIN_AS=normal'
]

count=0
    
TC1 = "select c3, length(c3) c3_len, nvl(c3, 'NULL') c3_nvl from t270457_y;"
TC2 = "select c3, length(c3) c3_len, nvl(c3, 'NULL') c3_nvl from t270457_n"
TC3 = "select c3, length(c3) c3_len, nvl(c3, 'NULL') c3_nvl from t270457_x;"

arr =[
    TC1,
    TC2,
    TC3
]

result = []
for row in add_properties:
    command = f'cd /home/tibero7/table_migrator && sh migrator.sh PROPERTY_FILE=./{file} {row}'

    output, error = execute_command_on_remote('192.168.17.33', 22, 'tibero7', 'tibero', command, file, tb_route)

    tibero_conn = tibero.get_tibero_connection(driver, ip, port, user, pw, sid)
    
    if tibero.select(tibero_conn, arr[0]) == tibero.select(tibero_conn, arr[count]):
        result.append(f"TC{count}: PASS")
    else:
        result.append(f"TC{count}: FAIL")

    print("Output:", output)
    
    count = count + 1
    
for row in result:
    print(row)