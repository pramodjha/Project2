

USE [CentralMI]
GO

ALTER TABLE [dbo].[reports1] DROP CONSTRAINT [FK__reports1__teamna__7E77B618]
GO

ALTER TABLE [dbo].[reports1] DROP CONSTRAINT [FK__reports1__second__005FFE8A]
GO

ALTER TABLE [dbo].[reports1] DROP CONSTRAINT [FK__reports1__primar__7F6BDA51]
GO

ALTER TABLE [dbo].[reports1] DROP CONSTRAINT [FK__reports1__freque__7AA72534]
GO

ALTER TABLE [dbo].[reports1] DROP CONSTRAINT [FK__reports1__delive__7C8F6DA6]
GO

ALTER TABLE [dbo].[reports1] DROP CONSTRAINT [FK__reports1__date_t__7B9B496D]
GO

ALTER TABLE [dbo].[reports1] DROP CONSTRAINT [DF__reports1__delive__7D8391DF]
GO

ALTER TABLE [dbo].[reports1] DROP CONSTRAINT [DF__reports1__regist__79B300FB]
GO

/****** Object:  Table [dbo].[reports1]    Script Date: 7/6/2018 11:46:56 AM ******/
DROP TABLE [dbo].[reports1]
GO

/****** Object:  Table [dbo].[reports1]    Script Date: 7/6/2018 11:46:56 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[reports1](
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

ALTER TABLE [dbo].[reports1] ADD  DEFAULT (getdate()) FOR [registereddate]
GO

ALTER TABLE [dbo].[reports1] ADD  DEFAULT (getdate()) FOR [deliverytime]
GO

ALTER TABLE [dbo].[reports1]  WITH CHECK ADD FOREIGN KEY([date_types])
REFERENCES [dbo].[date_types] ([date_typesid])
GO

ALTER TABLE [dbo].[reports1]  WITH CHECK ADD FOREIGN KEY([delivery_days])
REFERENCES [dbo].[delivery_days] ([delivery_daysid])
GO

ALTER TABLE [dbo].[reports1]  WITH CHECK ADD FOREIGN KEY([frequency])
REFERENCES [dbo].[frequency] ([frequencyid])
GO

ALTER TABLE [dbo].[reports1]  WITH CHECK ADD FOREIGN KEY([primaryowner])
REFERENCES [dbo].[mimember] ([mimemberid])
GO

ALTER TABLE [dbo].[reports1]  WITH CHECK ADD FOREIGN KEY([secondaryowner])
REFERENCES [dbo].[mimember] ([mimemberid])
GO

ALTER TABLE [dbo].[reports1]  WITH CHECK ADD FOREIGN KEY([teamname])
REFERENCES [dbo].[teamdetail] ([teamid])
GO




