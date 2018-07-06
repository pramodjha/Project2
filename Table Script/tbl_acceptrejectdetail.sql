USE [CentralMI]
GO

ALTER TABLE [dbo].[acceptrejectdetail] DROP CONSTRAINT [FK__acceptrej__reque__07420643]
GO

ALTER TABLE [dbo].[acceptrejectdetail] DROP CONSTRAINT [FK__acceptrej__estac__064DE20A]
GO

ALTER TABLE [dbo].[acceptrejectdetail] DROP CONSTRAINT [DF__acceptrej__estac__0559BDD1]
GO

/****** Object:  Table [dbo].[acceptrejectdetail]    Script Date: 7/6/2018 11:52:06 AM ******/
DROP TABLE [dbo].[acceptrejectdetail]
GO

/****** Object:  Table [dbo].[acceptrejectdetail]    Script Date: 7/6/2018 11:52:06 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[acceptrejectdetail](
	[estacceptrejectid] [int] IDENTITY(1,1) NOT NULL,
	[estacceptrejectdate] [datetime] NOT NULL,
	[estacceptrejectby] [int] NOT NULL,
	[requestdetail] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[estacceptrejectid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[acceptrejectdetail] ADD  DEFAULT (getdate()) FOR [estacceptrejectdate]
GO

ALTER TABLE [dbo].[acceptrejectdetail]  WITH CHECK ADD FOREIGN KEY([estacceptrejectby])
REFERENCES [dbo].[auth_user] ([id])
GO

ALTER TABLE [dbo].[acceptrejectdetail]  WITH CHECK ADD FOREIGN KEY([requestdetail])
REFERENCES [dbo].[requestdetail] ([requestid])
GO


