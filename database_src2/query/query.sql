-- create database naver_movie;
use naver_movie;

-- create table movie(
-- 	movie_id int unsigned,
--     -- 길이검사
--     title char(40) not null,
--     
--     playtime smallint unsigned,
--     open_date char(8),
--     
--     movie_rate char(10),
--     
-- 	   story varchar(5000),

--     exp_score int unsigned,
--     non_exp_score int unsigned,
--     
--     netizen_score decimal(4,2),
--     netizen_count int unsigned,
--     journal_score decimal(4,2),
--     journal_count int unsigned,
--     
--     enter_date datetime default now(),
--     
--     primary key(movie_id)
-- );

-- create table movie_nation(
-- 	movie_id int unsigned,
-- 	nation varchar(30),
--     primary key(movie_id, nation),
--     foreign key (movie_id) references movie(movie_id) on update cascade on delete cascade
-- );

-- create table movie_genre(
-- 	movie_id int unsigned,
--     genre char(8),
--     primary key(movie_id,genre),
--     foreign key (movie_id) references movie(movie_id) on update cascade on delete cascade
-- );

-- create table movie_photo(
-- 	movie_id int unsigned,
--     photo_link varchar(300),
--     foreign key (movie_id) references movie(movie_id) on update cascade on delete cascade
-- );

-- create table movie_netizen_review(
-- 	movie_id int unsigned,
--     user_name varchar(50),
--     score tinyint,
--     review varchar(300),
--     good int unsigned,
--     bad int unsigned,
--     foreign key (movie_id) references movie(movie_id) on update cascade on delete cascade
-- );

-- create table movie_journal_review(
-- 	movie_id int unsigned,
--     journal_name varchar(30),
--     score tinyint unsigned,
--     title varchar(100),
--     review varchar(1000),
--     foreign key (movie_id) references movie(movie_id) on update cascade on delete cascade
-- );

-- create table director(
-- 	dir_id int unsigned,
--     -- 길이검사
--     dir_name char(30),
--     dir_birth varchar(100),
--     dir_awards varchar(100),
--     dir_profile varchar(10000),
--     enter_date datetime default now(),
--     
--     primary key(dir_id)
-- );

-- create table movie_director(	
--     movie_id int unsigned,
-- 	dir_id int unsigned,
--     primary key(movie_id, dir_id),
--     foreign key (movie_id) references movie(movie_id) on update cascade on delete cascade,
--     foreign key (dir_id) references director(dir_id) on update cascade on delete cascade
-- );

-- create table actor(
-- 	act_id int unsigned,
--     -- 길이검사
--     act_name char(30),
--     act_birth varchar(100),
--     act_awards varchar(100),
--     act_profile varchar(10000),
--     enter_date datetime default now(),
--     
--     primary key(act_id)
-- );

-- create table movie_actor(
--     movie_id int unsigned,
-- 	act_id int unsigned,
--     casting varchar(50),
--     is_main tinyint	,
--     foreign key (movie_id) references movie(movie_id) on update cascade on delete cascade,
--     foreign key (act_id) references actor(act_id) on update cascade on delete cascade
-- );

-- create table exception_table(
-- 	movie_id int unsigned,
--     _where varchar(100),
--     err_msg varchar(2000),
--     enter_date datetime default now()
-- );

-- alter table movie modify story varchar(5000);
-- alter table movie add column story varchar(3000) after movie_rate;
-- alter table exception_table modify _where varchar(100);
-- alter table movie_act rename movie_actor;
-- alter table movie_dir rename movie_director;
-- alter table director modify dir_profile varchar(10000);
-- alter table actor modify act_profile varchar(10000);

create index movie_title on movie(title);
create index director_dir_name on director(dir_name);
create index actor_act_name on actor(act_name);

select * from movie where title = '시네마 천국';
select * from movie where netizen_count >= 100 order by netizen_score desc;



















-- delete from exception_table where movie_id = 31170;
-- delete from movie where movie_id = 50869;

-- delete from movie where movie_id = 39918;
-- delete from movie where movie_id = 16523;
 set sql_safe_updates = 0;
 set sql_safe_updates = 1;


use naver_movie;
select * from exception_table order by enter_date desc;

select * from movie order by enter_date desc;
select * from actor order by enter_date desc;
select * from director order by enter_date desc;
select count(*) from actor;
select count(*) from movie;
select count(*) from director;
select count(*) from exception_table;

select * from movie_netizen_review where movie_id = 101901good_score_list;
select * from movie_nation where movie_id = 39918;
select * from movie_journal_review where movie_id = 101901;
select * from movie_genre where movie_id = 39918;
select * from movie_director where movie_id = 39918;
select * from movie_photo where movie_id = 101901;
select count(*) from movie_photo where movie_id = 30776;
select * from movie_actor where movie_id = 39918;
select * from movie where movie_id = 39918;
select * from actor where act_id = 33374;
select * from director where dir_id = 26719;

select * from movie order by enter_date desc;
select * from actor order by enter_date desc;
select * from actor where act_name = '송강호';
select * from actor where act_id = 5256;
select * from actor where act_id = 22642;
select * from movie_act where act_id = 1824;
select * from movie where movie_id = 146469;
select * from movie_photo;
select * from movie where title like '미션%';
select * from movie_act where movie_id = 10100;
select * from actor where act_id = 1558;
select * from movie where movie_id = 50869;
select * from movie_photo where movie_id = 50869;
select * from movie_nation where movie_id = 50869;
select * from movie order by netizen_count desc;
select * from movie m where not exists(select 1 from movie_director d where d.movie_id = m.movie_id); 
select * from movie m where not exists(select 1 from movie_actor a where a.movie_id = m.movie_id);

select * from movie where movie_id in (select movie_id from movie_director where dir_id = (select dir_id from director where dir_name = ''));
select * from movie where movie_id = 101722;

select count(*) from movie_actor where movie_id = 191613;
select * from movie_actor where movie_id = 171539;
select * from movie_director where movie_id = 174830;
select * from director where dir_id = 130535;
select * from actor where act_id = 130535;

select * from movie_actor where movie_id = 144906;
select * from movie_photo where movie_id = 174830;

select * from movie where title = '시네마 천국';
select * from movie where title = '너는 내 운명';

select * from actor;
select * from movie;

create table test_ex_many(
	id int unsigned
);
select * from test_ex_many;
drop table test_ex_many;
delete from test_ex_many;

