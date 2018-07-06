USE [CentralMI]
GO

ALTER TABLE [dbo].[errorlog] DROP CONSTRAINT [FK__errorlog__error___5575A085]
GO

ALTER TABLE [dbo].[errorlog] DROP CONSTRAINT [FK__errorlog__error___54817C4C]
GO

ALTER TABLE [dbo].[errorlog] DROP CONSTRAINT [FK__errorlog__error___538D5813]
GO

ALTER TABLE [dbo].[errorlog] DROP CONSTRAINT [DF__errorlog__error___529933DA]
GO

ALTER TABLE [dbo].[errorlog] DROP CONSTRAINT [DF__errorlog__errorl__51A50FA1]
GO

/****** Object:  Table [dbo].[errorlog]    Script Date: 7/6/2018 12:00:05 PM ******/
DROP TABLE [dbo].[errorlog]
GO

/****** Object:  Table [dbo].[errorlog]    Script Date: 7/6/2018 12:00:05 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[errorlog](
	[error_id] [int] IDENTITY(1,1) NOT NULL,
	[errorlog_date] [datetime] NOT NULL,
	[error_occurancedate] [datetime] NOT NULL,
	[error_report] [int] NOT NULL,
	[error_reportedby] [varchar](50) NOT NULL,
	[error_reportedteam] [varchar](50) NOT NULL,
	[error_reportedto] [int] NOT NULL,
	[error_type] [int] NOT NULL,
	[error_description] [varchar](max) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[error_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[errorlog] ADD  DEFAULT (getdate()) FOR [errorlog_date]
GO

ALTER TABLE [dbo].[errorlog] ADD  DEFAULT (getdate()) FOR [error_occurancedate]
GO

ALTER TABLE [dbo].[errorlog]  WITH CHECK ADD FOREIGN KEY([error_report])
REFERENCES [dbo].[reports] ([reportid])
GO

ALTER TABLE [dbo].[errorlog]  WITH CHECK ADD FOREIGN KEY([error_reportedto])
REFERENCES [dbo].[auth_user] ([id])
GO

ALTER TABLE [dbo].[errorlog]  WITH CHECK ADD FOREIGN KEY([error_type])
REFERENCES [dbo].[errortype] ([error_typeid])
GO


