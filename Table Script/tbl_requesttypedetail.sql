USE [CentralMI]
GO

/****** Object:  Table [dbo].[requesttypedetail]    Script Date: 7/6/2018 12:10:49 PM ******/
DROP TABLE [dbo].[requesttypedetail]
GO

/****** Object:  Table [dbo].[requesttypedetail]    Script Date: 7/6/2018 12:10:49 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[requesttypedetail](
	[requesttypeid] [int] IDENTITY(1,1) NOT NULL,
	[requesttype] [varchar](50) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[requesttypeid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[requesttype] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO


