

DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS io;



create table task (
     id                 serial primary key ,
    taskname 	 		varchar(50) unique not null, 
    created	    		timestamp not null DEFAULT CURRENT_TIMESTAMP,
    status            	integer not null DEFAULT 0
  
);

create table io (
    id                  serial primary key ,
    task_id 	       	integer not null,
    type                integer not null DEFAULT 0,
    symbol           	varchar(10) not null,
    value              	double precision ,
    
    FOREIGN KEY (task_id) REFERENCES task (id)
  );
  
