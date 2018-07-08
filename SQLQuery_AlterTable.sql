use CentralMI
GO

Alter table activity
add activitystatus int;


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
