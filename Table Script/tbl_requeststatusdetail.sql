USE [CentralMI]
GO

ALTER TABLE [dbo].[requeststatusdetail] DROP CONSTRAINT [FK__requestst__usern__569ECEE8]
GO

ALTER TABLE [dbo].[requeststatusdetail] DROP CONSTRAINT [FK__requestst__statu__5792F321]
GO

ALTER TABLE [dbo].[requeststatusdetail] DROP CONSTRAINT [FK__requestst__reque__5887175A]
GO

ALTER TABLE [dbo].[requeststatusdetail] DROP CONSTRAINT [DF__requestst__reque__55AAAAAF]
GO

/****** Object:  Table [dbo].[requeststatusdetail]    Script Date: 7/6/2018 12:10:05 PM ******/
DROP TABLE [dbo].[requeststatusdetail]
GO

/****** Object:  Table [dbo].[requeststatusdetail]    Script Date: 7/6/2018 12:10:05 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[requeststatusdetail](
	[requeststatusid] [int] IDENTITY(1,1) NOT NULL,
	[requeststatusdate] [datetime] NOT NULL,
	[username] [int] NOT NULL,
	[statusdetail] [int] NULL,
	[requestdetail] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[requeststatusid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[requeststatusdetail] ADD  DEFAULT (getdate()) FOR [requeststatusdate]
GO

ALTER TABLE [dbo].[requeststatusdetail]  WITH CHECK ADD FOREIGN KEY([requestdetail])
REFERENCES [dbo].[requestdetail] ([requestid])
GO

ALTER TABLE [dbo].[requeststatusdetail]  WITH CHECK ADD FOREIGN KEY([statusdetail])
REFERENCES [dbo].[statusdetail] ([statusnameid])
GO

ALTER TABLE [dbo].[requeststatusdetail]  WITH CHECK ADD FOREIGN KEY([username])
REFERENCES [dbo].[auth_user] ([id])
GO


