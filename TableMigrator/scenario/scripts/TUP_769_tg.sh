tbsql tibero/tmax << EOF
        drop user trg283075 cascade;
        create user trg283075 identified by 'tmax';
        grant dba to trg283075;
        conn trg283075/tmax
       
        //t283075_1
        create table t283075_1 (col1 number, col2 number, col3 number);
        desc t283075_1;

        //t283075_11
        create table t283075_11 (col1 number, col2 number, col3 number);
        desc t283075_11;

        //t283075_1_notnull
        create table t283075_1_notnull(col1 number not null, col2 number not null, col3 number);
        desc t283075_1_notnull;

        //t283075_2
        create table t283075_2 (col1 clob, col2 blob, col3 number, col4 varchar(10), col5 date);
        desc t283075_2;

        quit;
EOF
