USE [CentralMI]
GO

/****** Object:  Table [dbo].[filteroption]    Script Date: 7/6/2018 12:05:25 PM ******/
DROP TABLE [dbo].[filteroption]
GO

/****** Object:  Table [dbo].[filteroption]    Script Date: 7/6/2018 12:05:25 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[filteroption](
	[filterid] [int] IDENTITY(1,1) NOT NULL,
	[filteroption] [varchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[filterid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO


