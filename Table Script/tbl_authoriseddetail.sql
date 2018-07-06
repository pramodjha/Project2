USE [CentralMI]
GO

ALTER TABLE [dbo].[authorisedetail] DROP CONSTRAINT [FK__authorise__reque__6F6A7CB2]
GO

ALTER TABLE [dbo].[authorisedetail] DROP CONSTRAINT [FK__authorise__autho__6E765879]
GO

ALTER TABLE [dbo].[authorisedetail] DROP CONSTRAINT [DF__authorise__autho__6D823440]
GO

/****** Object:  Table [dbo].[authorisedetail]    Script Date: 7/6/2018 11:54:27 AM ******/
DROP TABLE [dbo].[authorisedetail]
GO

/****** Object:  Table [dbo].[authorisedetail]    Script Date: 7/6/2018 11:54:27 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[authorisedetail](
	[authorisedid] [int] IDENTITY(1,1) NOT NULL,
	[authoriseddate] [datetime] NOT NULL,
	[authoriserdetail] [int] NULL,
	[requestdetail] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[authorisedid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[authorisedetail] ADD  DEFAULT (getdate()) FOR [authoriseddate]
GO

ALTER TABLE [dbo].[authorisedetail]  WITH CHECK ADD FOREIGN KEY([authoriserdetail])
REFERENCES [dbo].[authoriserdetail] ([authoriserid])
GO

ALTER TABLE [dbo].[authorisedetail]  WITH CHECK ADD FOREIGN KEY([requestdetail])
REFERENCES [dbo].[requestdetail] ([requestid])
GO


