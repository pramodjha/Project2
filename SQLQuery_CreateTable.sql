
use CentralMI
create table requesttypedetail(
requesttypeid int not null primary key Identity(1,1),
requesttype varchar(50) not null unique 
);

use CentralMI
create table prioritydetail(
requestpriorityid int not null primary key Identity(1,1),
requestpriority varchar(50) not null unique
);

use CentralMI
create table requestdetail(
requestid int not null primary key Identity(1,1),
requestraiseddate datetime default getdate() not null,
requesttypedetail int foreign key references requesttypedetail(requesttypeid) not null,
prioritydetail  int foreign key references prioritydetail(requestpriorityid) not null,
username int foreign key references auth_user(id) not null,
requestdescription varchar(max) not null,

);






use CentralMI
create table statusdetail(
statusnameid int not null primary key Identity(1,1),
statusname varchar(50) not null unique
);


use CentralMI
create table requeststatusdetail(
requeststatusid int not null primary key Identity(1,1),
requeststatusdate datetime default getdate() not null,
username int foreign key references auth_user(id) not null,
statusdetail int foreign key references statusdetail(statusnameid),
requestdetail int foreign key references requestdetail(RequestId) not null,
);


use CentralMI
create table authoriserdetail(
authoriserid int not null primary key Identity(1,1),
username int foreign key references auth_user(id) not null
);


use CentralMI
create table teamdetail(
teamid int not null primary key Identity(1,1),
teamdatetime datetime default getdate() not null,
teamname varchar(100) null
);

use CentralMI
create table mimember(
mimemberid int not null primary key Identity(1,1),
username int foreign key references auth_user(id) not null, 
teamdetail int foreign key references teamdetail(teamid) not null, 
);

use CentralMI
create table options(
optionsid int not null primary key Identity(1,1),
optionsname varchar(50) not null unique
);


use CentralMI
create table assigneddetail(
assignedid int not null primary key Identity(1,1),
assignedDate datetime default getdate() not null,
assignedto int foreign key references mimember(mimemberId),
assignedby int foreign key references mimember(mimemberId),
requestdetail int foreign key references requestdetail(requestid) not null
);


use CentralMI
create table authorisedetail(
authorisedid int not null primary key Identity(1,1),
authoriseddate datetime default getdate() not null,
authoriserdetail int foreign key references authoriserdetail(authoriserid),
requestdetail int foreign key references requestdetail(Requestid) not null
);

use CentralMI
create table overviewdetail(
overviewid int not null primary key Identity(1,1),
overviewdate datetime default getdate() not null,
providedby int foreign key references auth_user(id) not null,
mimember int foreign key references mimember(mimemberid),
sopcreatedoptionsid int foreign key references options(optionsId),
requestdetail int foreign key references requestdetail(requestid) not null,
document varchar(255)
);


use CentralMI
create table estimationdetail(
estimationid int not null primary key Identity(1,1),
estimationdate datetime default getdate() not null,
estimatedby int foreign key references mimember(mimemberId),
estimateddays int,
requestdetail int foreign key references requestdetail(requestid) not null
);

use CentralMI
create table completeddetail(
completedid int not null primary key Identity(1,1),
completeddate datetime default getdate() not null,
completedby int foreign key references mimember(mimemberId),
requestdetail int foreign key references requestdetail(requestid) not null
);

use CentralMI
create table acceptrejectoption(
acceptrejectoptionid int not null primary key Identity(1,1),
acceptrejectoptionname varchar(50) not null unique
);

use CentralMI
create table acceptrejectdetail(
estacceptrejectid int not null primary key Identity(1,1),
estacceptrejectdate datetime default getdate() not null,
estacceptrejectby int foreign key references auth_user(id) not null,
requestdetail int foreign key references requestdetail(requestid) not null
);



use CentralMI
create table requestcategorys(
requestcategoryid int not null primary key Identity(1,1),
requestcategorydatetime datetime default getdate() not null,
requestcategorys varchar(100) null

);

use CentralMI
create table requestsubcategory(
requestsubcategoryid int not null primary key Identity(1,1),
requestsubcategorydatetime datetime default getdate() not null,
requestcategorys int foreign key references requestcategorys(requestcategoryid), 
requestsubcategory varchar(100) null
);

use CentralMI
create table timetrackers(
timetrackerid int not null primary key Identity(1,1),
registerdatetime datetime default getdate() not null,
trackingdatetime datetime default getdate() not null,
mimember int foreign key references mimember(mimemberid),
teamdetail int foreign key references teamdetail(teamid),
requestcategorys int foreign key references requestcategorys(requestcategoryid),
requestsubcategory int foreign key references requestsubcategory(requestsubcategoryid),
task varchar(100) null,
requestdetail int foreign key references requestdetail(requestid),
options int foreign key references options(optionsid),
description_text varchar(255) null,
totaltime int,
comments varchar(255) null,
startdatetime datetime default getdate() null,
stopdatetime  datetime default getdate() null
);


use CentralMI
create table deliverydays(
deliverydaysid int not null primary key Identity(1,1),
days varchar(255) null
)

use CentralMI
create table frequency(
frequencyid int not null primary key Identity(1,1),
frequency varchar(255) null
)


use CentralMI
create table reports(
reportid int not null primary key Identity(1,1),
registereddate datetime default getdate() not null,
name varchar(255),
frequency int foreign key references frequency(frequencyid),
deliverydays int foreign key references deliverydays(deliverydaysid),
deliverytime datetime default CURRENT_TIMESTAMP not null,
primaryowner int foreign key references mimember(mimemberId),
secondaryowner int foreign key references mimember(mimemberId),
description varchar(255)
)



use CentralMI
create table emaildetail(
emailid int not null primary key Identity(1,1),
requestdetail int foreign key references requestdetail(requestid),
emaildate datetime default getdate() not null,
stage varchar(max) not null,
emailsubject  varchar(max) not null,
emailbody  varchar(max) not null,
emailto varchar(max) not null,
emailfrom varchar(max) not null,
);


use CentralMI
create table fielddetail(
fieldid int not null primary key Identity(1,1),
tablename varchar(255) not null,
fieldname  varchar(255) not null,
);

use CentralMI
create table filteroption(
filterid int not null primary key Identity(1,1),
filteroption varchar(255) not null,
);

