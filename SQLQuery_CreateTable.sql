
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
create table internaltask(
internaltaskid int not null primary key Identity(1,1),
internaltaskdatetime datetime default getdate() not null,
internaltaskQuestion varchar(255) not null,
status int foreign key references internaltask(internaltaskid) not null,

);

use CentralMI
create table internaltaskchoice(
internaltaskchoiceid int not null primary key Identity(1,1),
internaltaskchoicedatetime datetime default getdate() not null,
internaltaskchoice varchar(255) not null,
internaltask int foreign key references internaltask(internaltaskid) not null,
);

use CentralMI

create table internaltaskstatus(
internaltaskstatusid int not null primary key Identity(1,1),
internaltaskstatusdatetime datetime default getdate() not null,
mimember int foreign key references mimember(mimemberId),
internaltask int foreign key references internaltask(internaltaskid),
internaltaskchoice int foreign key references internaltaskchoice(internaltaskchoiceid),
)

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
create table designationmaster(
designationid int not null primary key Identity(1,1),
designation varchar(100) null
)

use CentralMI
create table managermaster(
managerid int not null primary key Identity(1,1),
managername varchar(100) null
)

use CentralMI
create table managermaster(
managerid int not null primary key Identity(1,1),
managername varchar(100) null
)

use CentralMI
create table tl_master(
tl_id int not null primary key Identity(1,1),
tl_name varchar(100) null
)


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


use CentralMI
create table whatwedo(
id int not null primary key Identity(1,1),
Data varchar(255) not null,
Description varchar(max) not null,
Type varchar(100) not null,
Image varchar(100) null
);

use CentralMI
create table suggestion(
suggestiondatetime datetime default getdate() not null,
suggestionid int not null primary key Identity(1,1),
name varchar(255) not null,
suggestion varchar(max) not null,
reply int foreign key references reply(replyid),
);

use CentralMI
create table governance(
governancedatetime datetime default getdate() not null,
governanceid int not null primary key Identity(1,1),
teamdetail int foreign key references teamdetail(teamid) not null,
processimg varchar(100) not null,
);


use CentralMI
create table reply(
replydatetime datetime default getdate() not null,
replyid int not null primary key Identity(1,1),
mimember int foreign key references mimember(mimemberId),
reply varchar(100) not null
)



create table tbl_navbar_header_master(
navbar_header_id int not null primary key Identity(1,1),
navbar_header_name varchar(255),
navbar_header_url varchar(255),
)


create table tbl_navbar_footer_master(
navbar_footer_id int not null primary key Identity(1,1),
navbar_footer_name varchar(255),
navbar_header_url varchar(255),

)

Use CentralMI
create table tbl_navbar_master(
navbar_id int not null primary key Identity(1,1),
group_name int foreign key references auth_group(id) not null,
navbar_header_id int foreign key references tbl_navbar_header_master(navbar_header_id) not null,
navbar_footer_id int foreign key references tbl_navbar_footer_master(navbar_footer_id) not null,

)

Use CentralMI
create table tbl_conversation(
conversationid int not null primary key Identity(1,1),
date_time datetime default getdate() not null,
requestdetail int foreign key references requestdetail(requestid) not null,
userid int foreign key references auth_user(id) not null,
comments varchar(max)
)


create table tbl_leave_type(
leavetypeid int not null primary key Identity(1,1),
date_time datetime default getdate() not null,
leave_type varchar(100)
)


Use CentralMI
create table tbl_leave_record(
leaverecordid int not null primary key Identity(1,1),
date_time datetime default getdate() not null,
leave_date date not null,
userid int foreign key references auth_user(id) not null,
leave_type int foreign key references tbl_leave_type(leavetypeid) not null,
)


Use CentralMI
create table tbl_leave_record(
leaverecordid int not null primary key Identity(1,1),
date_time datetime default getdate() not null,
leave_date date not null,
userid int foreign key references auth_user(id) not null,
leave_type int foreign key references tbl_leave_type(leavetypeid) not null,
)


create table UAT_status(
UAT_status_id  int not null primary key Identity(1,1),
date_time datetime default getdate() not null,
UAT_status varchar(100)
);

drop table UAT_status

use CentralMI
create table UAT_detail(
uatid int not null primary key Identity(1,1),
date_time datetime default getdate() not null,
UAT_status int foreign key references UAT_status(UAT_status_id),
requestdetail int foreign key references requestdetail(requestid) not null
);

use CentralMI
create table tbl_Appreciation(
Appreciationid int not null primary key Identity(1,1),
date_time datetime default getdate() not null,
Appreciated_to int foreign key references mimember(mimemberId),
Appreciated_by varchar(100),
Description varchar(255)
);

use CentralMI
create table tbl_raw_team_master(
raw_team_id int not null primary key Identity(1,1),
date_time datetime default getdate() not null,
raw_team varchar(255),
raw_team_icon varchar(255),
raw_team_slogan varchar(255),

);

use CentralMI
drop table tbl_raw_team_member_master

create table tbl_raw_team_member_master(
raw_team_member_id int not null primary key Identity(1,1),
date_time datetime default getdate() not null,
raw_team int foreign key references tbl_raw_team_master(raw_team_id),
raw_member int foreign key references mimember(mimemberId),
);


drop table tbl_raw_score
use CentralMI
create table tbl_raw_score(
raw_score_id int not null primary key Identity(1,1),
date_time datetime default getdate() not null,
raw_team int foreign key references tbl_raw_team_master(raw_team_id),
score int,
Winner varchar(50),
description varchar(255)
);

use CentralMI
create table tbl_raw_activity_detail(
raw_activity_id int not null primary key Identity(1,1),
date_time datetime default getdate() not null,
raw_activity varchar(50),
raw_activity_description varchar(max),
raw_activity_img varchar(255),
raw_activity_scheduled date,
raw_activitystatus int foreign key references activitystatus(activitystatusid)
);




create table tbl_team_metrics(
metrics_id int not null primary key Identity(1,1),
date_time datetime default getdate() not null,
metrics_name varchar(255),
)

use CentralMI
create table team_metrics(
metrics_id int not null primary key Identity(1,1),
date_time datetime default getdate() not null,
teamdetail int foreign key references teamdetail(teamid),
metrics_name int foreign key references tbl_team_metrics(metrics_id),
requesttype int foreign key references  requesttypedetail(requesttypeid),
description varchar(255)
);


use CentralMI
create table tbl_useful_links(
linkid int not null primary key Identity(1,1),
date_time datetime default getdate() not null,
teamdetail int foreign key references teamdetail(teamid),
mimember int foreign key references mimember(mimemberId),
link varchar(max),
);





create table view_type (
view_id int not null primary key Identity(1,1),
viewname varchar(255),
)

create table assign_view (
viewassign_id int not null primary key Identity(1,1),
group_name int foreign key references auth_group(id) not null,
view_type int foreign key references view_type (view_id) not null,
)

Use CentralMI
create table tbl_navbar_view(
navbar_id int not null primary key Identity(1,1),
view_type int foreign key references view_type (view_id) not null,
navbar_header_id int foreign key references tbl_navbar_header_master(navbar_header_id) not null,
navbar_footer_id int foreign key references tbl_navbar_footer_master(navbar_footer_id) not null,
)

drop table team_metrics_data
drop column metrics_name

use CentralMI
create table team_metrics_data(
metrics_id int not null primary key Identity(1,1),
date_time datetime default getdate() not null,
teamdetail int foreign key references teamdetail(teamid),
requesttype int foreign key references  requesttypedetail(requesttypeid),
Total int,
WIP int,
UAT int,
Completed int,
Project int

);

use CentralMI
create table valid_invalid(
valid_invaidid int not null primary key Identity(1,1),
type varchar(255)
)


use 
create table PublicHolidays(
holidaysid int not null primary key Identity(1,1),
date date,
holidays_name varchar(255)
)

drop table Gallery

create table Gallery(
imgid int not null primary key Identity(1,1),
date_time  datetime default getdate() not null,
uploadedby int foreign key references mimember(mimemberId),
img varchar(255),
description varchar(max),
)

create table ShiftUpdate(
updateid int not null primary key Identity(1,1),
date_time datetime default getdate() not null,
updateinbrief varchar(max),
updatedrecordedby int foreign key references mimember(mimemberId),
updatestatus int foreign key references  activitystatus(activitystatusid),
)

create table Issue_Action(
Issue_Action_id int not null primary key Identity(1,1),
date_time datetime default getdate() not null,
Issue varchar(255),
Action_taken varchar(255),
targetdate date,
updatedby int foreign key references mimember(mimemberId),
status int foreign key references  activitystatus(activitystatusid),
)





