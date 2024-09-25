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
    ip = "192.168.17.33"
    port = "12000"
    user = "tibero"
    pw = "tmax"
    sid = "tibero"

    tibero_conn = tibero.get_tibero_connection(driver, ip, port, user, pw, sid)
    
    drop_query = ""

    tibero_conn.close()

# tablemigrator 수행
def run_tablemigrator():
    host = '192.168.17.33'
    port = 22
    tb_user = 'tibero7'
    tb_pw = 'tibero'

    tb_route = '/home/tibero7/table_migrator'
    
    # tablemigrator properties 기본값
    file = 'migrator.properties_TUP_750'
    
    # properties 옵션 추가 값
    add_properties = ' INSERT_ZERO_LENGTH_STRING_AS_NULL=Y  SOURCE_TABLE=TIBERO.t270457_y TARGET_TABLE=TIBERO.t270457_y'
    
    # 최종 tablemigrator properties
    command = f'cd /home/tibero7/table_migrator && sh migrator.sh PROPERTY_FILE=./{file} {add_properties}'
    
    print(command)
    output, error = execute_command_on_remote(host, port, tb_user, tb_pw, command, file, tb_route)

    print("Output:", output)
    print("Error:", error)
    

# Source DB Schema 수행
oracle_remote()

# Target DB Schema 수행
tibero_remote()

# table migrator 수행
# properties 값 파라미터로 입력 받기
run_tablemigrator()

# Test Scenario Pass or Fail Result
# 필터링 가능해보임 추후 리펙토링 필요 !
driver = "{Tibero 7 ODBC Driver}"
ip = "192.168.17.33"
port = "12000"
user = "tibero"
pw = "tmax"
sid = "tibero"

tibero_conn = tibero.get_tibero_connection(driver, ip, port, user, pw, sid)
