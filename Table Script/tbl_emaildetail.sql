USE [CentralMI]
GO

ALTER TABLE [dbo].[emaildetail] DROP CONSTRAINT [FK__emaildeta__reque__3E923B2D]
GO

ALTER TABLE [dbo].[emaildetail] DROP CONSTRAINT [DF__emaildeta__email__3F865F66]
GO

/****** Object:  Table [dbo].[emaildetail]    Script Date: 7/6/2018 11:59:42 AM ******/
DROP TABLE [dbo].[emaildetail]
GO

/****** Object:  Table [dbo].[emaildetail]    Script Date: 7/6/2018 11:59:42 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[emaildetail](
	[emailid] [int] IDENTITY(1,1) NOT NULL,
	[requestdetail] [int] NULL,
	[emaildate] [datetime] NOT NULL,
	[stage] [varchar](max) NOT NULL,
	[emailsubject] [varchar](max) NOT NULL,
	[emailbody] [varchar](max) NOT NULL,
	[emailto] [varchar](max) NOT NULL,
	[emailfrom] [varchar](max) NOT NULL,
	[emailstatus] [varchar](255) NULL,
	[RequestStatus] [varchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[emailid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[emaildetail] ADD  DEFAULT (getdate()) FOR [emaildate]
GO

ALTER TABLE [dbo].[emaildetail]  WITH CHECK ADD FOREIGN KEY([requestdetail])
REFERENCES [dbo].[requestdetail] ([requestid])
GO


