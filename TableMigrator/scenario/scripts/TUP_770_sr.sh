tbsql tibero/tmax << EOF
drop user src283075 cascade;
        create user src283075 identified by 'tmax';
        grant dba to src283075;
        conn src283075/tmax
//t283075_a
        create table t283075_a (c1 number, c2 number, c3 number);
        insert into t283075_a values(10, 20, 30);
//t283075_aa
        create table t283075_aa (c1 number, c2 number, c3 number);
        insert into t283075_aa values(11, 22, 33);
//t283075_b
        create table t283075_b (c1 clob, c2 blob, c3 number, c4 varchar(10), c5 date);
        insert into t283075_b values('aaaaaaaaaa', lpad('A',20,'A'), 30, 'fourty', sysdate);
        commit;
        select * from t283075_a;
        select * from t283075_aa;
        select * from t283075_b;
        
        quit;
EOF
