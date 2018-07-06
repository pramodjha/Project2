USE [CentralMI]
GO

/****** Object:  Table [dbo].[field_detail]    Script Date: 7/6/2018 12:03:50 PM ******/
DROP TABLE [dbo].[field_detail]
GO

/****** Object:  Table [dbo].[field_detail]    Script Date: 7/6/2018 12:03:50 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[field_detail](
	[fieldid] [int] IDENTITY(1,1) NOT NULL,
	[tablename] [varchar](max) NOT NULL,
	[fieldname] [varchar](max) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[fieldid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO


