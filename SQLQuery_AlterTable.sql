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

ALTER table mimember
drop column suggestedby


Alter table [CentralMI].[dbo].[suggestion]
add  suggestedby int;

ALTER TABLE [suggestion]
ADD FOREIGN KEY (suggestedby) REFERENCES auth_user(id);


Alter table [CentralMI].[dbo].[team_metrics]
add  volume int;


Alter table [CentralMI].[dbo].[UAT_detail]
add  testedby int;

Alter table [CentralMI].[dbo].[UAT_detail]
add  updatedby int;

Alter table [CentralMI].[dbo].[UAT_detail]
ADD FOREIGN KEY ([testedby]) REFERENCES auth_user(id);

Alter table [CentralMI].[dbo].[UAT_detail]
ADD FOREIGN KEY ([updatedby]) REFERENCES auth_user(id);


ALTER TABLE mimember
ALTER COLUMN PhoneNumber varchar(10);


ALTER TABLE timetrackers
ADD  OT_id int;

Alter table [CentralMI].[dbo].[timetrackers]
ADD FOREIGN KEY ([OT_id]) REFERENCES ot_detail(ot_id);

ALTER TABLE timetrackers
ADD  valid_invalid int;

Alter table [CentralMI].[dbo].[timetrackers]
ADD FOREIGN KEY ([valid_invalid]) REFERENCES valid_invalid(valid_invaidid);

ALTER TABLE tbl_raw_team_master
ADD  valid_invalid int;

Alter table [CentralMI].[dbo].[tbl_raw_team_master]
ADD FOREIGN KEY ([valid_invalid]) REFERENCES valid_invalid(valid_invaidid);

ALTER TABLE [tbl_raw_team_master]
ADD  raw_management int;

Alter table [CentralMI].[dbo].[tbl_raw_team_master]
ADD FOREIGN KEY ([raw_management]) REFERENCES options(optionsid);

