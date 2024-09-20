# 파이썬 DB 연동 코드 ( 컴포넌트화 가능함으로 폴더 분리 필요 )
# tibero의 경우 window 에서 odbc 실행 시 ODBC 데이터원본 수정이 필요하므로 추후 가이드 문서 작성 예정
# 파이썬의 경우 import pyodbc 라이브러리로 연동 가능 ( precondition 추가 필요 )
# oracle db 연동의 경우 pip install oracledb 프롬프트 명령어를 통해 oracledb 라이브러리 설치 ( precondition 추가 필요 )
# table migrator sh 을 수행하기 위해 import subprocess 라이브러리 추가 필요

import stat
import pyodbc as odbc
import oracledb
import subprocess
import os


# oracle 접속 정보

oracle_user = "tibero" 
oracle_pw = "tmax"
oracle_ip = "192.168.17.31"
oracle_port = "1521"
oracle_sid = "cdb1"

dsn = f"{oracle_ip}:{oracle_port}/{oracle_sid}"

# oracle instant client path 지정
oracledb.init_oracle_client(lib_dir="TableMigrator\instantclient_19_24")
oracle_conn = oracledb.connect(user=oracle_user, password=oracle_pw, dsn=dsn)  
cursor = oracle_conn.cursor() 


cursor.execute("drop table sales")

# 실제 시나리오 코드

# oracle db table 생성
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

cursor.execute(create_query)

# oracle db data insert
# insert 쿼리의 경우 단건으로 insert 해야함
cursor.execute("insert into tibero.SALES values (1, 2004, 05, 02, 'Sophia', to_date('19740502','yyyymmdd'), 65000)")
cursor.execute("insert into tibero.SALES values (2, 2005, 03, 02, 'Emily',  to_date('19750302','yyyymmdd'), 23000)")
cursor.execute("insert into tibero.SALES values (3, 2006, 08, 02, 'Olivia', to_date('19760802','yyyymmdd'), 34000)")
cursor.execute("insert into tibero.SALES values (4, 2007, 02, 02, 'Amelia', to_date('19770202','yyyymmdd'), 12000)")
cursor.execute("insert into tibero.SALES values (5, 2008, 04, 02, 'Chloe',  to_date('19780402','yyyymmdd'), 55000)")

#oracle db index insert
create_index = '''
create index tibero.SALES_IDX on tibero.SALES ( sales_no, sale_year ) local
'''

cursor.execute(create_index)
oracle_conn.commit()

cursor.close()
oracle_conn.close()

# 기본 접속 정보
dsn = "tibero7"
user = "tibero"
pw = "tmax"

conn = odbc.connect('DSN='+dsn+';UID='+user+';PWD='+pw)
cursor = conn.cursor()

cursor.execute('drop table tibero.SALES;')

# tibero partition table 생성

t_create_query = '''
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

# index 생성 
t_create_index = '''
create index tibero.SALES_IDX on tibero.SALES ( sales_no, sale_year ) local;
'''

cursor.execute(t_create_query)

cursor.execute('select * from tibero.SALES;')

if not cursor.fetchall():
    cursor.execute(t_create_index)
    print("TC3 :  PASS")
else:
    print("TC3 :  FAIL")


# table migrator 수행
# 기본 properties 설정 후 paramter 값 추가하는 방식으로
# 따로 mock 파일 만들어서 관리

# source table, target table 추가 필요
# 추가된 파라미터 함께 추가 본 시나리오에선 INDEX_DISABLE=Y,INSERT_PARTITION=sales_p1,SELECT_PARTITION=sales_p1 추가 필요


# 현재 스크립트 파일의 디렉터리 경로
current_dir = os.path.dirname(os.path.abspath(__file__))

# # 상대 경로를 절대 경로로 변환
# migrator_script = os.path.abspath("./TableMigrator/table_migrator/migrator.bat")

# # 쉘 명령
# cmd = [
#     "call", migrator_script,
#     "PROPERTY_FILE=./TableMigrator/table_migrator/migrator.properties_O2T",
#     "SOURCE_TABLE=SALES",
#     "TARGET_TABLE=SALES",
#     "INDEX_DISABLE=Y",
#     "INSERT_PARTITION=sales_p1",
#     "SELECT_PARTITION=sales_p1"
# ]

classpath = "migrator_cli.jar;ojdbc8.jar;postgresql-42.2.27.jre6.jar;msllogger-14.jar;toolcom.jar;internal-jdbc-16.jar;antlr-4.3-complete.jar"

# 쉘 명령
cmd = [
    "java", "-classpath", classpath,
    "com.m.migrator.Main",
    "PROPERTY_FILE=./TableMigrator/table_migrator/migrator.properties_O2T",
    "SOURCE_TABLE=SALES",
    "TARGET_TABLE=SALES",
    "INDEX_DISABLE=Y",
    "INSERT_PARTITION=sales_p1",
    "SELECT_PARTITION=sales_p1"
]


result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')


print("Command executed with exit code:", result)
    
# DB 커넥션 종료
cursor.close()
conn.close()
