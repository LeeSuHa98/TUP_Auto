# T-UP(TableMigrator) Test Scenario Auto Project

T-UP(TableMigrator)는 Tibero DB 전환 과정에서 호환성 평가 기능과 스키마 오브젝트 및 데이터를 마이그레이션하는 기능을 제공하는 Tool이다. </br>
본 프로젝트는 Source DB to Target DB 이관 기능에 대한 테스트 시나리오를 자동화하는 프로젝트이다.

# Requirements

## Precondition

### Install Library

```
pip install oracledb
pip install paramiko
pip install pyodbc
```

Python으로 ssh 원격 접속하기 위한 paramiko 설치를 진행한다. [Paramiko 메뉴얼] </br>
Tibero 의 경우 window 에선 odbc를 통해 DB 통신을 함으로 pyodbc 설치를 진행한다. </br>
Oracle DBMS 연동을 위해 oracledb 라이브러리 설치를 진행한다. </br>


## TableMigrator

TableMigrator의 경우 Tibero 설치 시 $TB_HOME/client/bin 경로에 T-UP.zip 파일로 떨궈진다.</br>
T-UP.zip 압축 해제 시 아래와 같이 디렉터리 및 스크립트 파일을 볼 수 있다. ( 각 디렉터리 및 파일은 [T-UP 매뉴얼] 에서 자세한 설명을 확인할 수 있다. ) </br>


```
installation-file.zip
  |--images
  |--lib
  |--log
  |--loader_bin (deprecated)
  |--T-Up.x86
  |--T-Up.x86_64
  |--T-Up.x86.bat
  |--T-Up.x86_64.bat
  |--Analyzer_history.xml
  |--Migrator_history.xml
  |--tableMigrator.zip
```

이 중 tableMigrator.zip 을 압축 해제 시 데이터 이관에 필요한 라이브러리 및 파일을 확인할 수 있다. </br>

```
toolcom.jar 
readme.txt 
postgresql-42.2.27.jre6.jar 
pgjdbc_License.txt 
msllogger-14.jar 
migrator_cli.jar 
migrator.sh 
migrator.properties.eg 
migrator.bat 
internal-jdbc-16.jar 
ANTLR4_License.txt 
antlr-4.3-complete.jar
```

이 중 Oracle DBMS 이관이 필요하다면 ojdbc6.jar (기본 설정 값) 을 필수로 해당 경로에 추가해줘야 한다. 자세한 설명은 [Trouble Shooting Guide] 에서 확인 가능하다. </br>

---


# Install (추후 추가 예정)

# Trouble Shooting Guide

### Oracle DBMS 데이터 이관 시 (추후 추가 예정)
[T-UP 메뉴얼]: https://technet.tmax.co.kr/ko/front/download/findDownloadList.do
[Paramiko 메뉴얼]: https://www.paramiko.org/installing.html
