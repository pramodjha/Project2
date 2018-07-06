USE [CentralMI]
GO

ALTER TABLE [dbo].[reports] DROP CONSTRAINT [FK__reports__seconda__3AC1AA49]
GO

ALTER TABLE [dbo].[reports] DROP CONSTRAINT [FK__reports__report___697C9932]
GO

ALTER TABLE [dbo].[reports] DROP CONSTRAINT [FK__reports__primary__39CD8610]
GO

ALTER TABLE [dbo].[reports] DROP CONSTRAINT [FK__reports__frequen__36F11965]
GO

ALTER TABLE [dbo].[reports] DROP CONSTRAINT [FK__reports__deliver__453F38BC]
GO

ALTER TABLE [dbo].[reports] DROP CONSTRAINT [FK__reports__deliver__37E53D9E]
GO

ALTER TABLE [dbo].[reports] DROP CONSTRAINT [DF__reports__deliver__38D961D7]
GO

ALTER TABLE [dbo].[reports] DROP CONSTRAINT [DF__reports__registe__35FCF52C]
GO

/****** Object:  Table [dbo].[reports]    Script Date: 7/6/2018 12:08:56 PM ******/
DROP TABLE [dbo].[reports]
GO

/****** Object:  Table [dbo].[reports]    Script Date: 7/6/2018 12:08:56 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[reports](
	[reportid] [int] IDENTITY(1,1) NOT NULL,
	[registereddate] [datetime] NOT NULL,
	[name] [varchar](255) NULL,
	[frequency] [int] NULL,
	[deliverydays] [int] NULL,
	[deliverytime] [datetime] NOT NULL,
	[primaryowner] [int] NULL,
	[secondaryowner] [int] NULL,
	[description] [varchar](255) NULL,
	[delivery_time] [int] NULL,
	[report_type] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[reportid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[reports] ADD  DEFAULT (getdate()) FOR [registereddate]
GO

ALTER TABLE [dbo].[reports] ADD  DEFAULT (getdate()) FOR [deliverytime]
GO

ALTER TABLE [dbo].[reports]  WITH CHECK ADD FOREIGN KEY([deliverydays])
REFERENCES [dbo].[deliverydays] ([deliverydaysid])
GO

ALTER TABLE [dbo].[reports]  WITH CHECK ADD FOREIGN KEY([delivery_time])
REFERENCES [dbo].[time_detail] ([timeid])
GO

ALTER TABLE [dbo].[reports]  WITH CHECK ADD FOREIGN KEY([frequency])
REFERENCES [dbo].[frequency] ([frequencyid])
GO

ALTER TABLE [dbo].[reports]  WITH CHECK ADD FOREIGN KEY([primaryowner])
REFERENCES [dbo].[mimember] ([mimemberid])
GO

ALTER TABLE [dbo].[reports]  WITH CHECK ADD FOREIGN KEY([report_type])
REFERENCES [dbo].[report_type] ([report_typid])
GO

ALTER TABLE [dbo].[reports]  WITH CHECK ADD FOREIGN KEY([secondaryowner])
REFERENCES [dbo].[mimember] ([mimemberid])
GO


