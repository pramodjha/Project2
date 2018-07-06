USE [CentralMI]
GO

ALTER TABLE [dbo].[timetrackers] DROP CONSTRAINT [FK__timetrack__teamd__13A7DD28]
GO

ALTER TABLE [dbo].[timetrackers] DROP CONSTRAINT [FK__timetrack__reque__168449D3]
GO

ALTER TABLE [dbo].[timetrackers] DROP CONSTRAINT [FK__timetrack__reque__1590259A]
GO

ALTER TABLE [dbo].[timetrackers] DROP CONSTRAINT [FK__timetrack__reque__149C0161]
GO

ALTER TABLE [dbo].[timetrackers] DROP CONSTRAINT [FK__timetrack__repor__3BB5CE82]
GO

ALTER TABLE [dbo].[timetrackers] DROP CONSTRAINT [FK__timetrack__optio__17786E0C]
GO

ALTER TABLE [dbo].[timetrackers] DROP CONSTRAINT [FK__timetrack__mimem__12B3B8EF]
GO

ALTER TABLE [dbo].[timetrackers] DROP CONSTRAINT [DF__timetrack__stopd__1960B67E]
GO

ALTER TABLE [dbo].[timetrackers] DROP CONSTRAINT [DF__timetrack__start__186C9245]
GO

ALTER TABLE [dbo].[timetrackers] DROP CONSTRAINT [DF__timetrack__track__11BF94B6]
GO

ALTER TABLE [dbo].[timetrackers] DROP CONSTRAINT [DF__timetrack__regis__10CB707D]
GO

/****** Object:  Table [dbo].[timetrackers]    Script Date: 7/6/2018 12:12:31 PM ******/
DROP TABLE [dbo].[timetrackers]
GO

/****** Object:  Table [dbo].[timetrackers]    Script Date: 7/6/2018 12:12:31 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[timetrackers](
	[timetrackerid] [int] IDENTITY(1,1) NOT NULL,
	[registerdatetime] [datetime] NOT NULL,
	[trackingdatetime] [datetime] NOT NULL,
	[mimember] [int] NULL,
	[teamdetail] [int] NULL,
	[requestcategorys] [int] NULL,
	[requestsubcategory] [int] NULL,
	[task] [varchar](100) NULL,
	[requestdetail] [int] NULL,
	[options] [int] NULL,
	[description_text] [varchar](255) NULL,
	[totaltime] [int] NULL,
	[comments] [varchar](255) NULL,
	[startdatetime] [datetime] NULL,
	[stopdatetime] [datetime] NULL,
	[reports] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[timetrackerid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[timetrackers] ADD  DEFAULT (getdate()) FOR [registerdatetime]
GO

ALTER TABLE [dbo].[timetrackers] ADD  DEFAULT (getdate()) FOR [trackingdatetime]
GO

ALTER TABLE [dbo].[timetrackers] ADD  DEFAULT (getdate()) FOR [startdatetime]
GO

ALTER TABLE [dbo].[timetrackers] ADD  DEFAULT (getdate()) FOR [stopdatetime]
GO

ALTER TABLE [dbo].[timetrackers]  WITH CHECK ADD FOREIGN KEY([mimember])
REFERENCES [dbo].[mimember] ([mimemberid])
GO

ALTER TABLE [dbo].[timetrackers]  WITH CHECK ADD FOREIGN KEY([options])
REFERENCES [dbo].[options] ([optionsid])
GO

ALTER TABLE [dbo].[timetrackers]  WITH CHECK ADD FOREIGN KEY([reports])
REFERENCES [dbo].[reports] ([reportid])
GO

ALTER TABLE [dbo].[timetrackers]  WITH CHECK ADD FOREIGN KEY([requestcategorys])
REFERENCES [dbo].[requestcategorys] ([requestcategoryid])
GO

ALTER TABLE [dbo].[timetrackers]  WITH CHECK ADD FOREIGN KEY([requestsubcategory])
REFERENCES [dbo].[requestsubcategory] ([requestsubcategoryid])
GO

ALTER TABLE [dbo].[timetrackers]  WITH CHECK ADD FOREIGN KEY([requestdetail])
REFERENCES [dbo].[requestdetail] ([requestid])
GO

ALTER TABLE [dbo].[timetrackers]  WITH CHECK ADD FOREIGN KEY([teamdetail])
REFERENCES [dbo].[teamdetail] ([teamid])
GO


