
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS input;
DROP TABLE IF EXISTS result;

create table task (
     id                 integer primary key  autoincrement,
    taskname 	 varchar(50) unique not null, 
    created	    timestamp not null DEFAULT CURRENT_TIMESTAMP,
    status           varchar(50) not null,  // result_ready , result_not_ready
  
);

create table input (
    id                  integer primary key  autoincrement,
    task_id 			  integer primary key  autoincrement,
    param1          double precision ,
    param2          double precision,      	
    param2          double precision,      
    FOREIGN KEY (job_id) REFERENCES user (task)
  );
create table result (
     id                        integer primary key  autoincrement,
     task_id 				integer primary key  ,
    result1		            double precision ,
    result1		            double precision ,
    result1		            double precision ,
  
    FOREIGN KEY (job_id) REFERENCES user (task)
  
  );
