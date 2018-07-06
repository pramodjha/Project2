USE [CentralMI]
GO

ALTER TABLE [dbo].[completeddetail] DROP CONSTRAINT [FK__completed__reque__7FA0E47B]
GO

ALTER TABLE [dbo].[completeddetail] DROP CONSTRAINT [FK__completed__compl__7EACC042]
GO

ALTER TABLE [dbo].[completeddetail] DROP CONSTRAINT [DF__completed__compl__7DB89C09]
GO

/****** Object:  Table [dbo].[completeddetail]    Script Date: 7/6/2018 11:55:46 AM ******/
DROP TABLE [dbo].[completeddetail]
GO

/****** Object:  Table [dbo].[completeddetail]    Script Date: 7/6/2018 11:55:46 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[completeddetail](
	[completedid] [int] IDENTITY(1,1) NOT NULL,
	[completeddate] [datetime] NOT NULL,
	[completedby] [int] NULL,
	[requestdetail] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[completedid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[completeddetail] ADD  DEFAULT (getdate()) FOR [completeddate]
GO

ALTER TABLE [dbo].[completeddetail]  WITH CHECK ADD FOREIGN KEY([completedby])
REFERENCES [dbo].[mimember] ([mimemberid])
GO

ALTER TABLE [dbo].[completeddetail]  WITH CHECK ADD FOREIGN KEY([requestdetail])
REFERENCES [dbo].[requestdetail] ([requestid])
GO


