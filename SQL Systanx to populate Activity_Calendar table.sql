	DECLARE @calendar_table_len AS int
	DECLARE @activity_table_len AS int
	DECLARE @calendar_loop_counter AS int
	DECLARE @activity_loop_counter AS int
	DECLARE @daystype AS varchar(50)
	DECLARE @frequency AS varchar(50)
	DECLARE @deliverydays AS int
	DECLARE @sqlText AS varchar(1000)
	
	select @calendar_table_len= count(*) from tbl_Calendar
	select @activity_table_len= count(*) from activity
	---truncate table activity_calendar

	SET @activity_loop_counter  = 1
	select @activity_table_len
	WHILE (@activity_loop_counter <= @activity_table_len)
		BEGIN
		select @daystype = A.[date_types] from [date_types] A where [date_typesid] in (select date_types from activity where activityid in (@activity_loop_counter)) 
		select @frequency = B.frequency from [frequency] B where [frequencyid] in (select frequency from activity where activityid in (@activity_loop_counter))
		select @deliverydays = delivery_days from activity where activityid in (@activity_loop_counter)
		select @frequency
		select @daystype 
		select @deliverydays
	
		if @frequency = 'Daily'
			Begin
			SET @sqlText = 'Insert into activity_calendar(date,daytype,weekname,activityid,
			frequency,CD_WD_days) Select date, [days type],[weekname],''' 
			+ cast(@activity_loop_counter as varchar(50)) + ''','''
			 
			+ cast(@frequency as varchar(50)) + ''',' 
			+ @frequency + ' from tbl_Calendar where ([days type] = ' + '''' 
			+ @daystype + '''' + ' and ' 
			+ @frequency + ' Not in (0))'  
			End
		Else
			Begin
			SET @sqlText = 'Insert into activity_calendar(date,daytype,weekname,activityid,
			frequency,CD_WD_days) Select date, [days type],[weekname],''' 
			+ cast(@activity_loop_counter as varchar(50)) 
			+ ''',''' + cast(@frequency as varchar(50)) 
			+ ''',' + @frequency + ' from tbl_Calendar where ([days type] = ' + '''' 
			+ @daystype + '''' + ' and ' 
			+ @frequency + ' in (' +  cast(@deliverydays as varchar(50)) + '))'  
			
			End
		--select(@sqlText)
		exec(@sqlText)

		SET @activity_loop_counter = @activity_loop_counter + 1
	END
	
