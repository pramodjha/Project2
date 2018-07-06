USE [CentralMI]
GO

/****** Object:  Table [dbo].[acceptrejectoption]    Script Date: 7/6/2018 11:52:48 AM ******/
DROP TABLE [dbo].[acceptrejectoption]
GO

/****** Object:  Table [dbo].[acceptrejectoption]    Script Date: 7/6/2018 11:52:48 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[acceptrejectoption](
	[acceptrejectoptionid] [int] IDENTITY(1,1) NOT NULL,
	[acceptrejectoptionname] [varchar](50) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[acceptrejectoptionid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[acceptrejectoptionname] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO


