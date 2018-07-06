USE [CentralMI]
GO

ALTER TABLE [dbo].[teamdetail] DROP CONSTRAINT [DF__teamdetai__teamd__5E3FF0B0]
GO

/****** Object:  Table [dbo].[teamdetail]    Script Date: 7/6/2018 12:11:34 PM ******/
DROP TABLE [dbo].[teamdetail]
GO

/****** Object:  Table [dbo].[teamdetail]    Script Date: 7/6/2018 12:11:34 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[teamdetail](
	[teamid] [int] IDENTITY(1,1) NOT NULL,
	[teamdatetime] [datetime] NOT NULL,
	[teamname] [varchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[teamid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[teamdetail] ADD  DEFAULT (getdate()) FOR [teamdatetime]
GO


