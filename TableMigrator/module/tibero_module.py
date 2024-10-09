import pyodbc as odbc

def get_tibero_connection(driver, ip, port, user, pw, sid):
    # DNS-less 설정을 통해 ODBC 드라이버 직접 지정하도록 수정.
    dsn = f"DRIVER={driver};SERVER={ip};PORT={port};UID={user};PWD={pw};DB={sid}"

    try:
        # ODBC를 통한 데이터베이스 연결
        tibero_conn = odbc.connect(dsn)
        print("Connected to Tibero database.")
        return tibero_conn
    except odbc.Error as e:
        print(f"Error connecting to Tibero: {e}")
        return None
    
    
def select(tibero_conn, select_query):
    cursor = tibero_conn.cursor()
    try:
        cursor.execute(select_query)
        # 모든 행을 가져옴
        rows = cursor.fetchall()
        
        int_rows = []   
        for row in rows:
            processed_row = []
            for item in row:
                if isinstance(item, float):
                    processed_row.append(int(item))  # float을 int로 변환
                elif isinstance(item, bytes):  # 이진 데이터인 경우
                    try:
                        processed_row.append(item.decode('utf-8'))  # utf-8로 디코딩
                    except UnicodeDecodeError:
                        processed_row.append(repr(item))  # 바이트 값을 문자열 형식으로 표시
                else:
                    processed_row.append(str(item))  # 나머지는 문자열로 변환
            int_rows.append(processed_row)
                    
        # 결과 출력 (또는 원하는 대로 처리)
        for row in int_rows:
            print(row)
        return int_rows  
    except odbc.Error as e:
        print(f"Error executing SELECT query: {e}")
        return None
    finally:
        cursor.close()
        
# 테이블 생성 함수
def create(tibero_conn, create_query):
    cursor = tibero_conn.cursor()
    
    try:
        cursor.execute(create_query)
        print("Table created successfully.")
    except odbc.Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()


# 테이블 삭제 함수
def drop(tibero_conn, drop_query):
    cursor = tibero_conn.cursor()
    try:
        cursor.execute(drop_query)
        print("Table dropped successfully.")
    except odbc.Error as e:
        print(f"Error dropping table: {e}")
    finally:
        cursor.close()
        
# 데이터 삽입 함수
# bind_values : batch 방식으로 data insert 하기 위한 bind value 값
# insert_query : 한번에 insert를 하기 위한 insert bind query
def insert(tibero_conn, insert_query, bind_values=None):
    cursor = tibero_conn.cursor()

    try:
        # 벌크 삽입을 위해 executemany 사용
        if bind_values:
            cursor.executemany(insert_query, bind_values)
        else: 
            cursor.execute(insert_query)
            
        tibero_conn.commit()
        print("Data inserted successfully.")
    except odbc.Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()

# 인덱스 생성 함수
def create_index(tibero_conn, create_index_query):
    cursor = tibero_conn.cursor()
    
    try:
        cursor.execute(create_index_query)
        print("Index created successfully.")
    except odbc.Error as e:
        print(f"Error creating Index: {e}")
    finally:
        cursor.close()
        
# 테이블 데이터 삭제 함수
def truncate(tibero_conn, truncate_query):
    cursor = tibero_conn.cursor()
    
    try:
        cursor.execute(truncate_query)
        print("Table Truncated successfully.")
    except odbc.Error as e:
        print(f"Error Truncated table: {e}")
    finally:
        cursor.close()

def create_user(tibero_conn, user, passwod):
    cursor = tibero_conn.cursor()
    
    try:
        cursor.execute('create user '+ user + ' identified by ' + passwod + ';')
        cursor.execute('grant dba to ' + user + ';')
        print("Create User successfully.")
    except odbc.Error as e:
        print(f"Error Create User: {e}")
    finally:
        cursor.close()

def drop_user(tibero_conn, user):
    cursor = tibero_conn.cursor()
    
    try:
        cursor.execute('drop user ' + user + ' cascade;')
        print("Drop User successfully.")
    except odbc.Error as e:
        print(f"Error Drop User: {e}")
    finally:
        cursor.close()
        
# 튜플을 비교하는 함수
def check_tuple_exists(tibero_conn, select_query, compare_tuple):
    results = select(tibero_conn, select_query)
    if results is None:
        return False

    if compare_tuple in [rows for rows in results]:
        return True
    return False