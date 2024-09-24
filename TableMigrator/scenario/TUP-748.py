# 파이썬 DB 연동 코드 ( 컴포넌트화 가능함으로 폴더 분리 필요 )
# tibero의 경우 window 에서 odbc 실행 시 ODBC 데이터원본 수정이 필요하므로 추후 가이드 문서 작성 예정
# 파이썬의 경우 import pyodbc 라이브러리로 연동 가능 ( precondition 추가 필요 )
# oracle db 연동의 경우 pip install oracledb 프롬프트 명령어를 통해 oracledb 라이브러리 설치 ( precondition 추가 필요 )
# table migrator sh 을 수행하기 위해 import subprocess 라이브러리 추가 필요
# 원격으로 리눅스에 접속하여 sh 을 수행하기 위해 pip install paramiko 라이브러리 설치 ( precondition 추가 필요)

import sys
import os

# 현재 파일의 상위 디렉토리인 project를 PYTHONPATH에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import paramiko
import main.oracle_info as oracle 
import main.tibero_info as tibero

# 리눅스 원격 접속 함수

def execute_command_on_remote(host, port, username, password, command):
    # SSH 클라이언트 생성
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 원격 서버에 SSH 연결
        ssh.connect(host, port=port, username=username, password=password)

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
    create table tibero.SALES (
    sales_no       number,
    sale_year      number,
    sale_month     number,
    sale_day       number,
    customer_name  varchar2(30),
    birth_date     date,
    price          number
    )
    partition by range (sales_no)
    (
    partition SALES_P1 values less than (3),
    partition SALES_P2 values less than (5),
    partition SALES_P3 values less than (maxvalue)
    )
    '''

    oracle_conn = oracle.get_oracle_connection(user, pw, ip, port, sid)
    
    drop_query = "drop table tibero.SALES"
    
    oracle.drop(oracle_conn, drop_query)
    oracle.create(oracle_conn, create_query)
    
    # 삽입할 데이터를 튜플 형태로 준비
    bind_values = [
        (1, 2004, 5, 2, 'Sophia', '19740502', 65000),
        (2, 2005, 3, 2, 'Emily',  '19750302', 23000),
        (3, 2006, 8, 2, 'Olivia', '19760802', 34000),
        (4, 2007, 2, 2, 'Amelia', '19770202', 12000),
        (5, 2008, 4, 2, 'Chloe',  '19780402', 55000)
    ]
    
    insert_query = "insert into tibero.SALES (sales_no, sale_year, sale_month, sale_day, customer_name, birth_date, price) values (:1, :2, :3, :4, :5, to_date(:6, 'yyyymmdd'), :7)"
    
    oracle.insert(oracle_conn, bind_values, insert_query)
    
    create_index = "create index tibero.SALES_IDX on tibero.SALES ( sales_no, sale_year ) local"
    
    oracle.create_index(oracle_conn, create_index)
    
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

    tibero_conn = tibero.get_tibero_connection(driver, user, pw, ip, port, sid)
    
    drop_query = "drop table tibero.SALES;"
    tibero.drop(tibero_conn, drop_query)
    
    create_query = '''
    create table tibero.SALES (
    sales_no       number,
    sale_year      number,
    sale_month     number,
    sale_day       number,
    customer_name  varchar2(30),
    birth_date     date,
    price          number
    )
    partition by range (sales_no)
    (
    partition SALES_P1 values less than (3),
    partition SALES_P2 values less than (5),
    partition SALES_P3 values less than (maxvalue)
    );
    '''

    tibero.create(tibero_conn, create_query)
    
    # index 생성 
    create_index = "create index tibero.SALES_IDX on tibero.SALES ( sales_no, sale_year ) local;"

    tibero.create_index(tibero_conn, create_index)
    
    tibero_conn.close()

# tablemigrator 수행
def run_tablemigrator():
    host = '192.168.17.33'
    port = 22
    tb_user = 'tibero7'
    tb_pw = 'tibero'

    # 원격 명령어 실행 시 paramiko 라이브러리는 사용자의 홈 디렉터리에서 명령을 수행하기 때문에 jar 와 같은 파일을 읽어와야 하는 상황에선 class loading 에 실패한다. Error: 오류: 기본 클래스 com.m.migrator.Main을(를) 찾거나 로드할 수 없습니다. 와 같은
    # 오류가 출력되는 것은 정상이다. 따라서 명령어 sh 파일을 수행하는 명령어 이전에 해당 디렉터리로 이동 후 스크립트를 수행해야한다.
    # 이전 코드의 경우
    # sh {home 경로}/{디렉터리 경로}/migrator.sh -> 해당 sh 을 읽을 수 없으므로 실패
    # ssh 를 통해 명령어 수행 시에 비로그인셸로 수행되어 .bash_profile 설정이 로드되지 않아 실패되는 경우
    # command = 'export JAVA_HOME=/path/to/java && sh /home/tibero7/table_migrator/migrator.sh' -> 실패 (paramiko  라이브러리의 경우 명령어는 해당 디렉토리에서 수행됨 )
    
    # table migrator 수행
    # 기본 properties 설정 후 paramter 값 추가하는 방식으로
    # 따로 mock 파일 만들어서 관리

    command = 'cd /home/tibero7/table_migrator && sh migrator.sh PROPERTY_FILE=./migrator.properties_o2t INDEX_DISABLE=Y SOURCE_LOGIN_AS=normal SOURCE_TABLE=tibero.SALES TARGET_TABLE=tibero.SALES INSERT_PARTITION=sales_p1 SELECT_PARTITION=sales_p1'

    # tablemigrator properties 기본값 
    
    # tablemigrator properties 옵션 추가 값
    
    # 최종 tablemigrator properties
    
    output, error = execute_command_on_remote(host, port, tb_user, tb_pw, command)

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

tibero_conn = tibero.get_tibero_connection(driver, user, pw, ip, port, sid)

test_query = "SELECT INDEX_NAME, PARTITION_NAME, STATUS FROM DBA_IDX_PARTITIONS WHERE PARTITION_NAME LIKE 'SALES_P1';"

for index, partition, status in tibero.select(tibero_conn, test_query):
    if status == 'UNUSABLE':
        print('PASS')
    else:
        print("FAIL")