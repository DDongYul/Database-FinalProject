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
    
    director char(10),
    
    movie_rate char(10),
    
    audience_count int unsigned,
    
    photo_link varchar(70),
    
    video_link varchar(70),
    
	exp_score mediumint unsigned,
    non_exp_score mediumint unsigned,
    
    netizen_rate decimal(3,2),
    netizen_count mediumint unsigned,
    
    journal_rate decimal(3,2),
    journal_count tinyint unsigned,
        
    enter_date datetime default now(),
    
    primary key(id)
);

select * from movie_list;


create table scope_table(
	id int not null,
    scope char(6) not null,
    
    primary key(id, scope),
    foreign key (id) references movie_list(id) on update cascade on delete cascade
);

select * from scope_table;


create table actor_table(
	id int not null,
    actor char(20) not null,
    
    primary key(id, actor),
    foreign key (id) references movie_list(id) on update cascade on delete cascade
);

select * from actor_table;



drop table movie_list;
drop table scope_table;
drop table actor_table;
delete from movie_list;
delete from scope_table;
delete from actor_table;