USE [CentralMI]
GO
/****** Object:  StoredProcedure [dbo].[usp_activity_calendar]    Script Date: 8/28/2018 11:11:01 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
ALTER PROCEDURE [dbo].[usp_activity_calendar]
@inputdate varchar(50),
@inputfreq varchar(50)
AS
SELECT A.[date]
      ,A.[daytype]
      ,A.[weekname]
      ,A.[CD_WD_days]
      ,A.[activityid]
      ,A.[frequency]
	  ,B.deliverytime
	  ,B.description
	  ,B.name
	  ,B.requestcategorys
	  ,B.primaryowner
	  ,B.secondaryowner
	  ,c.activitystatusdate
	  ,c.activitystatus
	  ,c.activitycalendardate
	  ,c.reallocatedto
	  ,C.recordenteredby
	  ,D.teamname
	  ,G.activitystatus
	  ,H.statusname
  FROM [CentralMI].[dbo].[activity_calendar] A
  Left Join [CentralMI].[dbo].[activity] B on A.[activityid] = B.[activityid]
  Left Join [CentralMI].[dbo].[activitystatus_calendar] C on B.[activityid] = C.[activityid]
  Left Join [CentralMI].[dbo].[teamdetail] D on B.teamname = D.teamid
  Left Join  [CentralMI].[dbo].[activitystatus] G on B.activitystatus = G.activitystatusid
  Left Join  [CentralMI].[dbo].[statusdetail] H on C.activitystatus = H.statusnameid

 where A.date in (@inputdate)
  and A.frequency in (@inputfreq)
  and G.activitystatus not in ('Closed')
  and  (H.statusname not in ('Completed','Rejected') or H.statusname  is null) 

  