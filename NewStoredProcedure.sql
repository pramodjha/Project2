
SELECT A.[requestid]
      ,A.[requestraiseddate]
      ,A.[requesttypedetail]
      ,A.[prioritydetail]
      ,A.[username]
      ,A.[requestdescription] 
	  ,B.[authoriseddate]
	  ,B.[authoriserdetail]
	  ,B.[requestdetail]
	  ,c.[assignedDate]
	  ,C.[assignedby]
	  ,C.[assignedto]
	  ,D.[overviewdate]
	  ,D.[providedby]
	  ,D.[mimember]
	  ,D.[sopcreatedoptionsid]
	  ,E.[estimationdate]
	  ,E.[estimatedby]
	  ,E.[estimateddays]
	  ,F.[estacceptrejectdate]
	  ,F.[estacceptrejectby]
	  ,G.[completeddate]
	  ,G.[completedby]
	  ,H.[requeststatusdate]
	  ,H.[username]
	  ,H.[statusdetail]
	  ,I.[statusname]
	   ,Case
			When  E.estimationdate is not null and I.[statusname] in ('Estimation Rejected') Then 'RejectionStage' 
			When  G.completeddate is not null Then 'CompletedStage'
			When  E.[estimationdate] is not null and I.[statusname] in ('Estimation Accepted') Then 'WIPStage' 
			When  E.[estimationdate]  is not null Then 'EstimateStage' 
			When  D.[overviewdate] is not null Then 'OverviewStage'
			When  c.[assignedDate] is not null then 'AssignedStage'
			When  B.[authoriseddate] is not null and I.[statusname] in ('Not Approved') Then  'RejectionStage'
			When  B.[authoriseddate] is not null and I.[statusname] in ('Approved') Then  'AuthorisedStage'
			When  A.[requestraiseddate] is not null then 'RequestStage'
	   End As Current_Stage   
	   FROM [requestdetail]  as A
	   left Join [authorisedetail]    as B on  A.[requestid] = B.[requestdetail] 
	   left Join [assigneddetail]     as c on  A.[requestid] = c.[requestdetail] 
	   left Join [overviewdetail]     as D on  A.[requestid] = D.[requestdetail] 
	   left Join [estimationdetail]   as E on  A.[requestid] = E.[requestdetail] 
	   left Join [acceptrejectdetail] as F on  A.[requestid] = F.[requestdetail] 
	   left Join [completeddetail]    as G on  A.[requestid] = G.[requestdetail]
	   left Join [requeststatusdetail]as H on  A.[requestid] = H.[requestdetail]
	   left Join [statusdetail] as I  on  H.statusdetail = I.[statusnameid]
	   Order by Current_Stage, A.requestid
	   
  