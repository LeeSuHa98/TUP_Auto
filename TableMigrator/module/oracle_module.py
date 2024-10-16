import oracledb

def get_oracle_connection(ip, port, user, pw,  sid, mode=None):
    dsn = f"{ip}:{port}/{sid}"

    # Oracle Instant Client 경로 설정
    # 프로그램 시작 전 static 고정값으로 수정 필요
    # 추후 자동화 시 install 과 연동되도록 경로값 수정
    oracledb.init_oracle_client(lib_dir=r"C:\Users\develop\instantclient-basic-windows.x64-19.24.0.0.0dbru\instantclient_19_24")
    
    # 데이터베이스 연결
    try:
        oracle_conn = oracledb.connect(user=user, password=pw, dsn=dsn, mode=mode)
        return oracle_conn
    except oracledb.DatabaseError as e:
        print(f"Error connecting to Oracle: {e}")
        return None

# 조회 함수
def select(oracle_conn, select_query):
    cursor = oracle_conn.cursor()
    try:
        cursor.execute(select_query)
        # 모든 행을 가져옴
        rows = cursor.fetchall()
        # 결과 출력 (또는 원하는 대로 처리)
        for row in rows:
            print(row)
        return rows  
    except oracledb.DatabaseError as e:
        print(f"Error executing SELECT query: {e}")
        return None
    finally:
        cursor.close()
        
# 테이블 삭제 함수
def drop(oracle_conn, drop_query):
    cursor = oracle_conn.cursor()
    cursor.execute(drop_query)
    try:
        cursor.execute(drop_query)
        print("Table dropped successfully.")
    except oracledb.DatabaseError as e:
        print(f"Error dropping table: {e}")
    finally:
        cursor.close()
        
# 테이블 생성 함수
def create(oracle_conn, create_query):
    cursor = oracle_conn.cursor()
    
    try:
        cursor.execute(create_query)
        print("Table created successfully.")
    except oracledb.DatabaseError as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()

# 데이터 삽입 함수
# bind_values : batch 방식으로 data insert 하기 위한 bind value 값
# insert_query : 한번에 insert를 하기 위한 insert bind query
def insert(oracle_conn, insert_query, bind_values=None):
    cursor = oracle_conn.cursor()

    try:
        # 벌크 삽입을 위해 executemany 사용
        if bind_values:
            cursor.executemany(insert_query, bind_values)
        else: 
            cursor.execute(insert_query)
            
        oracle_conn.commit()
        print("Data inserted successfully.")
    except oracledb.DatabaseError as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()

# 인덱스 생성 함수
def create_index(oracle_conn, create_index_query):
    cursor = oracle_conn.cursor()
    
    try:
        cursor.execute(create_index_query)
        print("Index created successfully.")
    except oracledb.DatabaseError as e:
        print(f"Error creating Index: {e}")
    finally:
        cursor.close()

# 테이블 데이터 삭제 함수
def truncate(oracle_conn, truncate_query):
    cursor = oracle_conn.cursor()
    cursor.execute(truncate_query)
    try:
        cursor.execute(truncate_query)
        print("Table Truncated successfully.")
    except oracledb.DatabaseError as e:
        print(f"Error Truncated table: {e}")
    finally:
        cursor.close()
        
# alter 함수
def alter(oracle_conn, alter_query):
    cursor = oracle_conn.cursor()
    cursor.execute(alter_query)
    try:
        cursor.execute(alter_query)
        print("ALTER query executed successfully.")
    except oracledb.DatabaseError as e:
        print(f"Error ALTER query: {e}")
    finally:
        cursor.close()
        
def create_user(oracle_conn, user, password):
    cursor = oracle_conn.cursor()
    
    cursor.execute("SELECT name FROM v$pdbs WHERE OPEN_MODE LIKE '%READ WRITE%'")
    pdb_list = cursor.fetchall()
    
    if not pdb_list:
        print("No PDB found in READ WRITE mode.")
        return

    pdb_name = pdb_list[0][0]
    
    try:
        cursor.execute(f"ALTER SESSION SET CONTAINER = {pdb_name}")
        cursor.execute(f'create user {user} identified by {password}')
        cursor.execute(f'grant CONNECT to {user}')
        cursor.execute(f'grant RESOURCE to {user}')
        cursor.execute(f'alter user {user} default tablespace users')
        cursor.execute(f'alter user {user} quota unlimited on users')
        print("Create User successfully.")
    except oracledb.DatabaseError as e:
        print(f"Error Create User: {e}")
    finally:
        cursor.close()

def drop_user(oracle_conn, user):
    cursor = oracle_conn.cursor()
    
    try:
        cursor.execute('drop user ' + user + ' cascade')
        print("Drop User successfully.")
    except oracledb.DatabaseError as e:
        print(f"Error Drop User: {e}")
    finally:
        cursor.close()