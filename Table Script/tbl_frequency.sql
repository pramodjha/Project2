USE [CentralMI]
GO

/****** Object:  Table [dbo].[frequency]    Script Date: 7/6/2018 12:05:51 PM ******/
DROP TABLE [dbo].[frequency]
GO

/****** Object:  Table [dbo].[frequency]    Script Date: 7/6/2018 12:05:51 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[frequency](
	[frequencyid] [int] IDENTITY(1,1) NOT NULL,
	[frequency] [varchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[frequencyid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO


