-- create database naver_movie;
use naver_movie;

create table movie(
	movie_id int unsigned,
    -- 길이검사
    title char(40) not null,
    
    playtime smallint unsigned,
    open_date char(8),
    
    movie_rate char(10),
    
    exp_score int unsigned,
    non_exp_score int unsigned,
    
    netizen_score decimal(4,2),
    netizen_count int unsigned,
    journal_score decimal(4,2),
    journal_count int unsigned,
    
    enter_date datetime default now(),
    
    primary key(movie_id)
);

create table movie_nation(
	movie_id int unsigned,
	nation varchar(30),
    primary key(movie_id, nation),
    foreign key (movie_id) references movie(movie_id) on update cascade on delete cascade
);

create table movie_genre(
	movie_id int unsigned,
    genre char(8),
    primary key(movie_id,genre),
    foreign key (movie_id) references movie(movie_id) on update cascade on delete cascade
);

create table movie_photo(
	movie_id int unsigned,
    photo_link varchar(200),
    primary key(movie_id,photo_link),
    foreign key (movie_id) references movie(movie_id) on update cascade on delete cascade
);

create table movie_netizen_review(
	movie_id int unsigned,
    user_name varchar(50),
    score tinyint,
    review varchar(200),
    good int unsigned,
    bad int unsigned,
    primary key(movie_id, user_name),
    foreign key (movie_id) references movie(movie_id) on update cascade on delete cascade
);

create table movie_journal_review(
	movie_id int unsigned,
    journal_name varchar(10),
    score tinyint unsigned,
    title varchar(100),
    review varchar(1000),
    primary key(movie_id, journal_name),
    foreign key (movie_id) references movie(movie_id) on update cascade on delete cascade
);

create table director(
	dir_id int unsigned,
    -- 길이검사
    dir_name char(30),
    dir_birth varchar(100),
    dir_awards varchar(100),
    dir_profile varchar(5000),
    enter_date datetime default now(),
    
    primary key(dir_id)
);

create table movie_dir(	
    movie_id int unsigned,
	dir_id int unsigned,
    primary key(movie_id, dir_id),
    foreign key (movie_id) references movie(movie_id) on update cascade on delete cascade,
    foreign key (dir_id) references director(dir_id) on update cascade on delete cascade
);

create table actor(
	act_id int unsigned,
    -- 길이검사
    act_name char(30),
    act_birth varchar(100),
    act_awards varchar(100),
    act_profile varchar(5000),
    enter_date datetime default now(),
    
    primary key(act_id)
);

create table movie_act(
    movie_id int unsigned,
	act_id int unsigned,
    casting varchar(50),
    is_Main tinyint	,
    foreign key (movie_id) references movie(movie_id) on update cascade on delete cascade,
    foreign key (act_id) references movie(movie_id) on update cascade on delete cascade
);

create table exception_table(
	movie_id int unsigned,
    _where varchar(20),
    err_msg varchar(100),
    enter_date datetime default now()
);











drop table movie_genre;
drop table movie_journal_review;
drop table movie_nation;
drop table movie_netizen_review;
drop table movie_photo;
drop table act_movie;
drop table dir_movie;
drop table actor;
drop table director;
drop table movie;

create table test_ex_many(
	id int unsigned
);
select * from test_ex_many;
drop table test_ex_many;
delete from test_ex_many;
















