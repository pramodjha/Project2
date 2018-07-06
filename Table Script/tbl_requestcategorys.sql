USE [CentralMI]
GO

ALTER TABLE [dbo].[requestcategorys] DROP CONSTRAINT [DF__requestca__reque__0A1E72EE]
GO

/****** Object:  Table [dbo].[requestcategorys]    Script Date: 7/6/2018 12:09:16 PM ******/
DROP TABLE [dbo].[requestcategorys]
GO

/****** Object:  Table [dbo].[requestcategorys]    Script Date: 7/6/2018 12:09:16 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[requestcategorys](
	[requestcategoryid] [int] IDENTITY(1,1) NOT NULL,
	[requestcategorydatetime] [datetime] NOT NULL,
	[requestcategorys] [varchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[requestcategoryid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[requestcategorys] ADD  DEFAULT (getdate()) FOR [requestcategorydatetime]
GO


