
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS input;
DROP TABLE IF EXISTS result;

create table task (
     id                 serial primary key ,
    taskname 	 varchar(50) unique not null, 
    created	    timestamp not null DEFAULT CURRENT_TIMESTAMP,
    status           varchar(50) not null  
  
);

create table input (
    id                     serial primary key ,
    task_id 	       integer not null,
    param1          double precision ,
    
    FOREIGN KEY (task_id) REFERENCES task (id)
  );
  
create table result (
     id                       serial primary key ,
     task_id 				integer not null  ,
     symbol                varchar(50) not null,
    result		            double precision ,
  
    FOREIGN KEY (task_id) REFERENCES task (id)
  
  );
