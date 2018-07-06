USE [CentralMI]
GO

ALTER TABLE [dbo].[ot_detail] DROP CONSTRAINT [FK__ot_detail__timet__64B7E415]
GO

ALTER TABLE [dbo].[ot_detail] DROP CONSTRAINT [FK__ot_detail__ot_st__65AC084E]
GO

/****** Object:  Table [dbo].[ot_detail]    Script Date: 7/6/2018 12:06:45 PM ******/
DROP TABLE [dbo].[ot_detail]
GO

/****** Object:  Table [dbo].[ot_detail]    Script Date: 7/6/2018 12:06:45 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[ot_detail](
	[ot_id] [int] IDENTITY(1,1) NOT NULL,
	[timetrackers] [int] NOT NULL,
	[ot_startdatetime] [datetime] NULL,
	[ot_enddatetime] [datetime] NULL,
	[ot_hrs] [int] NULL,
	[ot_status] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[ot_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[ot_detail]  WITH CHECK ADD FOREIGN KEY([ot_status])
REFERENCES [dbo].[ot_status] ([ot_statusid])
GO

ALTER TABLE [dbo].[ot_detail]  WITH CHECK ADD FOREIGN KEY([timetrackers])
REFERENCES [dbo].[timetrackers] ([timetrackerid])
GO


