DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS job;
DROP TABLE IF EXISTS input;
DROP TABLE IF EXISTS result;
DROP TABLE IF EXISTS jobmanager;

create table user (
    id 					      integer primary key  autoincrement,
    username 		 varchar(50) UNIQUE NOT NULL,
    password 		 varchar(50) NOT NULL
);

create table job (
     id                  integer primary key  autoincrement,
    user_id 		integer not null,
    jobname 	     varchar(50) unique not null, 
    created	    timestamp not null DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

create table input (
    jobid 			  integer primary key  autoincrement,
    param1          double precision ,
    param2          double precision,      	
    param2          double precision,      
  );
create table result (
     job_id 					integer primary key  ,
    result1		            double precision ,
    result1		            double precision ,
    result1		            double precision ,
    -- x , y , z , ...
    FOREIGN KEY (job_id) REFERENCES user (job)
  
  );

/*
CREATE TABLE jobmanager (
  id 				INTEGER PRIMARY KEY AUTOINCREMENT,
  --user_id 		INTEGER NOT NULL,
  job_id 	    TEXT UNIQUE NOT NULL, 
  status			TEXT NOT NULL,
  starttime	    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  endtime		TIMESTAMP NULL 
);
*/