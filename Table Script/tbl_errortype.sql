USE [CentralMI]
GO

/****** Object:  Table [dbo].[errortype]    Script Date: 7/6/2018 12:00:23 PM ******/
DROP TABLE [dbo].[errortype]
GO

/****** Object:  Table [dbo].[errortype]    Script Date: 7/6/2018 12:00:23 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[errortype](
	[error_typeid] [int] IDENTITY(1,1) NOT NULL,
	[error_type] [varchar](50) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[error_typeid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO


