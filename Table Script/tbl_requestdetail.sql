USE [CentralMI]
GO

ALTER TABLE [dbo].[requestdetail] DROP CONSTRAINT [FK__requestde__usern__4FF1D159]
GO

ALTER TABLE [dbo].[requestdetail] DROP CONSTRAINT [FK__requestde__reque__4E0988E7]
GO

ALTER TABLE [dbo].[requestdetail] DROP CONSTRAINT [FK__requestde__prior__4EFDAD20]
GO

ALTER TABLE [dbo].[requestdetail] DROP CONSTRAINT [DF__requestde__reque__4D1564AE]
GO

/****** Object:  Table [dbo].[requestdetail]    Script Date: 7/6/2018 12:09:48 PM ******/
DROP TABLE [dbo].[requestdetail]
GO

/****** Object:  Table [dbo].[requestdetail]    Script Date: 7/6/2018 12:09:48 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[requestdetail](
	[requestid] [int] IDENTITY(1,1) NOT NULL,
	[requestraiseddate] [datetime] NOT NULL,
	[requesttypedetail] [int] NOT NULL,
	[prioritydetail] [int] NOT NULL,
	[username] [int] NOT NULL,
	[requestdescription] [varchar](max) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[requestid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[requestdetail] ADD  DEFAULT (getdate()) FOR [requestraiseddate]
GO

ALTER TABLE [dbo].[requestdetail]  WITH CHECK ADD FOREIGN KEY([prioritydetail])
REFERENCES [dbo].[prioritydetail] ([requestpriorityid])
GO

ALTER TABLE [dbo].[requestdetail]  WITH CHECK ADD FOREIGN KEY([requesttypedetail])
REFERENCES [dbo].[requesttypedetail] ([requesttypeid])
GO

ALTER TABLE [dbo].[requestdetail]  WITH CHECK ADD FOREIGN KEY([username])
REFERENCES [dbo].[auth_user] ([id])
GO


