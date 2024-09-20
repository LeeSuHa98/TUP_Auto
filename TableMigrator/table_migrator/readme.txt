
####################################
# 1. 실행환경 및 JDBC 라이브러리 설치
#    Execution Environment and JDBC Library Installation 
####################################

Table migrator는 Java 6 또는 그 이후 버전의 Java를 필요로 합니다.
DB접속시에는 파라미터 또는 properties 파일의 속성을 통해 지정한 포트를 이용한 TCP 통신으로 접속을 하므로, 방화벽 등으로 인해 해당 포트가 막혀있지 않아야 합니다. 
접속할 DB의 JDBC Driver 파일을 확보하여 실행 스크립트의 classpath의 파일 경로에 추가해 주어야 합니다.

The table migrator requires Java 6 or later version. 
When connecting to the DB, the port must not be blocked by a firewall since TCP communication is used through a port specified by using a parameter or the properties file. 
To access the DB, the JDBC driver file of the DB must be added to the classpath in the execution script.


####################################
# 2. source/target 데이터베이스 준비
#    Source/Target Database Preparation
####################################

이관 작업을 수행하기 전에 원본 테이블과 동일한 컬럼 이름과 데이터 타입을 가지는 테이블을 타깃 데이터베이스 측에 미리 생성해두어야 합니다.
이때 테이블의 컬럼 이름들은 대소문자까지 동일한 형태로 생성되어 있어야 합니다.
SOURCE DB에 로그인 할 때 사용되는 계정에는 이관할 테이블에 대한 select 권한이 필요합니다.
SOURCE DB의 타입을 Oracle로 지정한 경우에는 추가로 SELECT ANY DICTIONARY 권한이 필요합니다.
SOURCE DB의 타입을 Tibero로 지정한 경우에도 DD 뷰를 조회할 수 있는 권한이 필요합니다. (ex. DBA_TAB_TABLES, ALL_TAB_PARTITIONS)  
TARGET DB에 로그인 할 때 사용되는 계정에는 이관 대상 테이블에 대한 insert 권한이 필요합니다.

Before migrating the DB, tables with the same column names and data types as the source tables must be created in the target database in advance. 
The table column names are case-sensitive.
The account that is used to log into the SOURCE DB must have the SELECT privilege on the source tables.
If the SOURCE DB is Oracle, the SELECT ANY DICTIONARY privilege is also required.
If the SOURCE DB is Tibero, the SELECT privilege for DD views is also required. (e.g., DBA_TAB_TABLES, ALL_TAB_PARTITIONS)  
The account that is used to log into the TARGET DB must have the INSERT privilege on the target tables. 


####################################
# 3. 실행
#    Execution
####################################

실행 스크립트는 POSIX계열에서는 migrator.sh, 윈도우즈에서는 migrator.bat를 사용하시면 됩니다.
사용시 접속 정보와 옮길 테이블에 대한 정보를 프로퍼티 파일이나 실행파일의 인자로 지정할 수 있습니다.
PROPERTY_FILE 속성으로 특정 프로퍼티 파일을 지정할 수 있으며, 이 속성을 지정하지 않는 경우 기본값은 migration.properties 입니다. 
지정된 properties 파일과 실행시 부여한 인자에 동일한 속성이 있는 경우, 인자로 부여한 속성값이 우선됩니다.
User나 Table 이름이 대소문자 구분이 필요한 경우에는 "TableName" 형태로 쌍따옴표를 이용하여 지정해 주어야 합니다.

For an execution script, use 'migrator.sh' in POSIX and 'migrator.bat' in Windows.
The connection and source table information can be specified by using a properties file or parameters of execution script.
The PROPERTY_FILE specifies a properties file. The default value is 'migration.properties'.
If a parameter specified when executing the script is also set in the specified properties file, the parameter has a priority.
When executing the properties file, if a parameter specifies a duplicate property, the parameter has higher priority.
If a User or Table name includes both upper and lower case letters, wrap the name in double quotes as in "TableName". 


usage:
migrator.sh[.bat] SOURCE_TYPE=ORACLE SOURCE_URL=jdbc:oracle:thin:@192.1.1.1:1521:ORCL SOURCE_USER=scott SOURCE_PASSWORD=tiger SOURCE_LOGIN_AS=NORMAL SOURCE_SCHEMA=scott SOURCE_TABLE=emp TARGET_URL=jdbc:tibero:thin:@192.1.1.2:8025:tb4sp1 TARGET_USER=tibero TARGET_PASSWORD=tmax INSERT_METHOD=DPL

migrator.sh[.bat] PROPERTY_FILE=migration.properties SOURCE_USER=scott SOURCE_PASSWORD=tiger SOURCE_TABLE=emp TARGET_USER=tibero TARGET_PASSWORD=tmax

migrator.sh[.bat] PROPERTY_FILE=migration.properties

migrator.sh[.bat]
