import oracledb

def get_oracle_connection(user, pw, ip, port, sid):
    dsn = f"{ip}:{port}/{sid}"

    # Oracle Instant Client 경로 설정
    # 프로그램 시작 전 static 고정값으로 수정 필요
    # 추후 자동화 시 install 과 연동되도록 경로값 수정
    oracledb.init_oracle_client(lib_dir=r"C:\Users\develop\instantclient-basic-windows.x64-19.24.0.0.0dbru\instantclient_19_24")
    
    # 데이터베이스 연결
    try:
        oracle_conn = oracledb.connect(user=user, password=pw, dsn=dsn)
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
def insert(oracle_conn, bind_values, insert_query):
    cursor = oracle_conn.cursor()

    try:
        # 벌크 삽입을 위해 executemany 사용
        cursor.executemany(insert_query, bind_values)
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
