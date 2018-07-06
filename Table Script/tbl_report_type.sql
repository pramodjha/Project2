USE [CentralMI]
GO

/****** Object:  Table [dbo].[report_type]    Script Date: 7/6/2018 12:08:25 PM ******/
DROP TABLE [dbo].[report_type]
GO

/****** Object:  Table [dbo].[report_type]    Script Date: 7/6/2018 12:08:25 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[report_type](
	[report_typid] [int] IDENTITY(1,1) NOT NULL,
	[report_type] [varchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[report_typid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO


