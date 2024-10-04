tbsql tibero/tmax << EOF
-- 유저 삭제 및 생성
drop user src283075 cascade;
create user src283075 identified by 'tmax';
grant dba to src283075;

-- 유저 접속
conn src283075/tmax;

-- 테이블 생성 및 데이터 삽입
-- t283075_a 테이블
create table t283075_a (c1 number, c2 number, c3 number);
insert into t283075_a values(10, 20, 30);

-- t283075_aa 테이블
create table t283075_aa (c1 number, c2 number, c3 number);
insert into t283075_aa values(11, 22, 33);

-- t283075_b 테이블
create table t283075_b (c1 clob, c2 blob, c3 number, c4 varchar(10), c5 date);
insert into t283075_b values('aaaaaaaaaa', lpad('A',20,'A'), 30, 'fourty', sysdate);

-- 커밋
commit;

-- 데이터 조회
select * from t283075_a;
select * from t283075_aa;
select * from t283075_b;

-- 종료
quit;
EOF