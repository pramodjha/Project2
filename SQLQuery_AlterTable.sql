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



use CentralMI
GO
Alter table statusdetail
add unique (statusname)


use CentralMI
GO
Alter table activity
alter column deliverytime time null;



use CentralMI
ALTER TABLE activity
ADD FOREIGN KEY (activitystatus) REFERENCES activitystatus(activitystatusid);

use CentralMI
ALTER TABLE reports
DROP COlumn deliverytime
