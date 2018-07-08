USE [CentralMI]
GO

ALTER TABLE [dbo].[activity] DROP CONSTRAINT [FK__activity__teamna__08F5448B]
GO

ALTER TABLE [dbo].[activity] DROP CONSTRAINT [FK__activity__second__08012052]
GO

ALTER TABLE [dbo].[activity] DROP CONSTRAINT [FK__activity__primar__070CFC19]
GO

ALTER TABLE [dbo].[activity] DROP CONSTRAINT [FK__activity__freque__0618D7E0]
GO

ALTER TABLE [dbo].[activity] DROP CONSTRAINT [FK__activity__date_t__0524B3A7]
GO

ALTER TABLE [dbo].[activity] DROP CONSTRAINT [DF__activity__regist__04308F6E]
GO

/****** Object:  Table [dbo].[activity]    Script Date: 7/7/2018 10:19:38 AM ******/
DROP TABLE [dbo].[activity]
GO

/****** Object:  Table [dbo].[activity]    Script Date: 7/7/2018 10:19:38 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[activity](
	[reportid] [int] IDENTITY(1,1) NOT NULL,
	[registereddate] [datetime] NOT NULL,
	[name] [varchar](255) NULL,
	[frequency] [int] NULL,
	[date_types] [int] NULL,
	[delivery_days] [int] NULL,
	[deliverytime] [time](7) NOT NULL,
	[teamname] [int] NULL,
	[primaryowner] [int] NULL,
	[secondaryowner] [int] NULL,
	[description] [varchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[reportid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[activity] ADD  DEFAULT (getdate()) FOR [registereddate]
GO

ALTER TABLE [dbo].[activity]  WITH CHECK ADD FOREIGN KEY([date_types])
REFERENCES [dbo].[date_types] ([date_typesid])
GO

ALTER TABLE [dbo].[activity]  WITH CHECK ADD FOREIGN KEY([frequency])
REFERENCES [dbo].[frequency] ([frequencyid])
GO

ALTER TABLE [dbo].[activity]  WITH CHECK ADD FOREIGN KEY([primaryowner])
REFERENCES [dbo].[mimember] ([mimemberid])
GO

ALTER TABLE [dbo].[activity]  WITH CHECK ADD FOREIGN KEY([secondaryowner])
REFERENCES [dbo].[mimember] ([mimemberid])
GO

ALTER TABLE [dbo].[activity]  WITH CHECK ADD FOREIGN KEY([teamname])
REFERENCES [dbo].[teamdetail] ([teamid])
GO


