use CentralMI
GO

Alter table errorlog
add errordocument varchar(255);


Alter table ot_detail
add otdocument varchar(255);


Alter table activity
add activitydocument varchar(255);


Alter table activity
add activitystatus int;


Alter table activity
add activitystatus varchar(255);


Alter table mimember
add designationmaster int;


Alter table mimember
add DateofJoining date;

Alter table mimember
add DateofBirth date;

Alter table mimember
add DateofBirth date;

Alter table mimember
add Address varchar(max);

Alter table mimember
add PhoneNumber int;

Alter table mimember
add PhoneNumber int;

use CentralMI
ALTER TABLE mimember
ADD FOREIGN KEY (designationmaster) REFERENCES designationmaster(designationid);


Alter table mimember
add tl_master int;

Alter table mimember
add employeeid int


Alter table tl_master
add employeeid int

use CentralMI
ALTER TABLE mimember
ADD FOREIGN KEY (tl_master) REFERENCES tl_master(tl_id);


Alter table mimember
add managermaster int;

use CentralMI
ALTER TABLE mimember
ADD FOREIGN KEY (managermaster) REFERENCES managermaster(managerid);

use CentralMI
GO
Alter table statusdetail
add unique (statusname)


use CentralMI
GO
Alter table activity
alter column deliverytime time null;



Alter table internaltask
add [Owner] int;


use CentralMI
ALTER TABLE internaltask
ADD FOREIGN KEY ([Owner]) REFERENCES mimember(mimemberid);

use CentralMI
ALTER TABLE [mimember]
DROP COlumn [managermaster]

Alter table [CentralMI].[dbo].[mimember]
add  Avatar varchar(255);
Alter table [CentralMI].[dbo].[mimember]
add  aboutme varchar(max);

Alter table [CentralMI].[dbo].[mimember]
add  aboutme varchar(max);
