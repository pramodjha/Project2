USE [CentralMI]
GO

/****** Object:  Table [dbo].[time_detail]    Script Date: 7/6/2018 12:11:56 PM ******/
DROP TABLE [dbo].[time_detail]
GO

/****** Object:  Table [dbo].[time_detail]    Script Date: 7/6/2018 12:11:56 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[time_detail](
	[timeid] [int] IDENTITY(1,1) NOT NULL,
	[time] [varchar](max) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[timeid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO


