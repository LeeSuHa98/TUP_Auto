import paramiko
import os

# 리눅스 원격 접속 함수
def execute_shell(host, port, username, password, command, file, tb_route):
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
        local_file = os.path.join(current_dir, '../scenario/properties', file)  # Python 코드가 실행되는 로컬 파일 경로
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



# 미리 ssh 커넥션 맺고 sh 스크립트만 수행할 수 있도록 코드 구성
def execute_sql(host, port, username, password, file):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
    try:
        ssh.connect(host, port=port, username=username, password=password)
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        local_file = os.path.join(current_dir, '../scenario/scripts/', file)
        remote_file = '/home/tibero7/table_migrator'
        sftp = ssh.open_sftp()

        sftp.put(local_file, remote_file+'/'+file)

        sftp.close()
        
        stdin, stdout, stderr = ssh.exec_command(f'bash -l -c "cd {remote_file} && sh {file}"')
        
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        print("Output:", output)
        print("Error:", error)      
            
        ssh.exec_command(f'rm -rf {remote_file}/{file}')
    except Exception as e:
        print()
    finally:
        ssh.close()
    
    return