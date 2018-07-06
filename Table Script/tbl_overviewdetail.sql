USE [CentralMI]
GO

ALTER TABLE [dbo].[overviewdetail] DROP CONSTRAINT [FK__overviewd__sopcr__75235608]
GO

ALTER TABLE [dbo].[overviewdetail] DROP CONSTRAINT [FK__overviewd__reque__76177A41]
GO

ALTER TABLE [dbo].[overviewdetail] DROP CONSTRAINT [FK__overviewd__provi__733B0D96]
GO

ALTER TABLE [dbo].[overviewdetail] DROP CONSTRAINT [FK__overviewd__mimem__742F31CF]
GO

ALTER TABLE [dbo].[overviewdetail] DROP CONSTRAINT [DF__overviewd__overv__7246E95D]
GO

/****** Object:  Table [dbo].[overviewdetail]    Script Date: 7/6/2018 12:07:30 PM ******/
DROP TABLE [dbo].[overviewdetail]
GO

/****** Object:  Table [dbo].[overviewdetail]    Script Date: 7/6/2018 12:07:30 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[overviewdetail](
	[overviewid] [int] IDENTITY(1,1) NOT NULL,
	[overviewdate] [datetime] NOT NULL,
	[providedby] [int] NOT NULL,
	[mimember] [int] NULL,
	[sopcreatedoptionsid] [int] NULL,
	[requestdetail] [int] NOT NULL,
	[document] [varchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[overviewid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[overviewdetail] ADD  DEFAULT (getdate()) FOR [overviewdate]
GO

ALTER TABLE [dbo].[overviewdetail]  WITH CHECK ADD FOREIGN KEY([mimember])
REFERENCES [dbo].[mimember] ([mimemberid])
GO

ALTER TABLE [dbo].[overviewdetail]  WITH CHECK ADD FOREIGN KEY([providedby])
REFERENCES [dbo].[auth_user] ([id])
GO

ALTER TABLE [dbo].[overviewdetail]  WITH CHECK ADD FOREIGN KEY([requestdetail])
REFERENCES [dbo].[requestdetail] ([requestid])
GO

ALTER TABLE [dbo].[overviewdetail]  WITH CHECK ADD FOREIGN KEY([sopcreatedoptionsid])
REFERENCES [dbo].[options] ([optionsid])
GO


