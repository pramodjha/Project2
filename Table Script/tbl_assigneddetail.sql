USE [CentralMI]
GO

ALTER TABLE [dbo].[assigneddetail] DROP CONSTRAINT [FK__assignedd__reque__6AA5C795]
GO

ALTER TABLE [dbo].[assigneddetail] DROP CONSTRAINT [FK__assignedd__assig__69B1A35C]
GO

ALTER TABLE [dbo].[assigneddetail] DROP CONSTRAINT [FK__assignedd__assig__68BD7F23]
GO

ALTER TABLE [dbo].[assigneddetail] DROP CONSTRAINT [DF__assignedd__assig__67C95AEA]
GO

/****** Object:  Table [dbo].[assigneddetail]    Script Date: 7/6/2018 11:53:32 AM ******/
DROP TABLE [dbo].[assigneddetail]
GO

/****** Object:  Table [dbo].[assigneddetail]    Script Date: 7/6/2018 11:53:32 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[assigneddetail](
	[assignedid] [int] IDENTITY(1,1) NOT NULL,
	[assignedDate] [datetime] NOT NULL,
	[assignedto] [int] NULL,
	[assignedby] [int] NULL,
	[requestdetail] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[assignedid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[assigneddetail] ADD  DEFAULT (getdate()) FOR [assignedDate]
GO

ALTER TABLE [dbo].[assigneddetail]  WITH CHECK ADD FOREIGN KEY([assignedto])
REFERENCES [dbo].[mimember] ([mimemberid])
GO

ALTER TABLE [dbo].[assigneddetail]  WITH CHECK ADD FOREIGN KEY([assignedby])
REFERENCES [dbo].[mimember] ([mimemberid])
GO

ALTER TABLE [dbo].[assigneddetail]  WITH CHECK ADD FOREIGN KEY([requestdetail])
REFERENCES [dbo].[requestdetail] ([requestid])
GO


