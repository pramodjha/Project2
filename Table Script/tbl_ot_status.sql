USE [CentralMI]
GO

/****** Object:  Table [dbo].[ot_status]    Script Date: 7/6/2018 12:07:09 PM ******/
DROP TABLE [dbo].[ot_status]
GO

/****** Object:  Table [dbo].[ot_status]    Script Date: 7/6/2018 12:07:09 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[ot_status](
	[ot_statusid] [int] IDENTITY(1,1) NOT NULL,
	[ot_status] [varchar](50) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[ot_statusid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO


