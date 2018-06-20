use CentralMI
GO

Alter table [CentralMI].[dbo].[reports]
add deliverytime varchar(max) ;


use CentralMI
GO
Alter table statusdetail
add unique (statusname)


use CentralMI
GO
Alter table reports
alter column delivery_time int null;



use CentralMI
ALTER TABLE reports
ADD FOREIGN KEY (delivery_time) REFERENCES time_detail(timeid);

use CentralMI
ALTER TABLE reports
DROP COlumn deliverytime
