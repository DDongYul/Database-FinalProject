insert into rate_test(rate) values(10.00);
insert into rate_test(rate) values(9.75);

create table rate_test(
	rate decimal(4,2)
);

drop table rate_test;
select * from rate_test;

create table test_title(
	id int unsigned,
    title char(30),
    primary key(id)
);

set sql_safe_updates = 0;
set sql_safe_updates = 1;

delete from test_title;
drop table test_title;

select * from test_title;









create table movie_list(
	id int not null,
    
    title char(30) not null,
    
    country char(10),
    playtime smallint unsigned,
    opening_date char(8),
    
    director char(20),
    
    movie_rate char(10),
    
    audience_count int unsigned,
    
    photo_link varchar(70),
    
    video_link varchar(70),
    
	exp_score mediumint unsigned,
    non_exp_score mediumint unsigned,
    
    netizen_rate decimal(4,2),
    netizen_count mediumint unsigned,
    
    journal_rate decimal(4,2),
    journal_count tinyint unsigned,
        
    enter_date datetime default now(),
    
    primary key(id)
);




create table scope_table(
	id int not null,
    scope char(6) not null,
    
    primary key(id, scope),
    foreign key (id) references movie_list(id) on update cascade on delete cascade
);




create table actor_table(
	id int not null,
    actor char(20) not null,
    
    primary key(id, actor),
    foreign key (id) references movie_list(id) on update cascade on delete cascade
);


create table exception_table(
	id int not null,
    err_msg varchar(100) not null,
    
    primary key(id)
);


select * from movie_list;
select * from scope_table;
select * from actor_table;
select * from exception_table;
select count(*)from movie_list;
select * from movie_list order by enter_date desc;
select * from scope_table where id = 167569;
select * from actor_table where id = 167569;
select * from movie_list where id = 167569;

select * from movie_list orde


















-- drop table exception_table;
-- drop table scope_table;
-- drop table actor_table;
-- drop table movie_list;


-- delete from movie_list;
-- delete from scope_table;
-- delete from actor_table;
--  delete from exception_table;