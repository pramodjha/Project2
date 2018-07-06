USE [CentralMI]
GO

/****** Object:  Table [dbo].[date_types]    Script Date: 7/6/2018 11:57:55 AM ******/
DROP TABLE [dbo].[date_types]
GO

/****** Object:  Table [dbo].[date_types]    Script Date: 7/6/2018 11:57:55 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[date_types](
	[date_typesid] [int] IDENTITY(1,1) NOT NULL,
	[date_types] [varchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[date_typesid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO


