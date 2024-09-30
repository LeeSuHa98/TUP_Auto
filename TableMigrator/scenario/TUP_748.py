import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import module.oracle_info as oracle 
import module.tibero_info as tibero
import module.execute_linux as execute
        
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

    oracle_conn = oracle.get_oracle_connection(ip, port, user, pw, sid)
    
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

    tibero_conn = tibero.get_tibero_connection(driver, ip, port, user, pw, sid)
    
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

    tb_route = '/home/tibero7/table_migrator'
    
    # tablemigrator properties 기본값
    file = 'migrator.properties_O2T'
    
    # properties 옵션 추가 값
    add_properties = 'INDEX_DISABLE=Y SOURCE_LOGIN_AS=normal SOURCE_TABLE=tibero.SALES TARGET_TABLE=tibero.SALES INSERT_PARTITION=sales_p1 SELECT_PARTITION=sales_p1'
    
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

# Test Scenario Pass or Fail Result
# 필터링 가능해보임 추후 리펙토링 필요 !
driver = "{Tibero 7 ODBC Driver}"
ip = "192.168.17.33"
port = "12000"
user = "tibero"
pw = "tmax"
sid = "tibero"

tibero_conn = tibero.get_tibero_connection(driver, ip, port, user, pw, sid)

test_query = "SELECT INDEX_NAME, PARTITION_NAME, STATUS FROM DBA_IDX_PARTITIONS WHERE PARTITION_NAME LIKE 'SALES_P1';"

for index, partition, status in tibero.select(tibero_conn, test_query):
    
    # 패치 후 결과
    if status == 'UNUSABLE':
        print('PASS')
    # 패치 전 결과
    else:
        print("FAIL")