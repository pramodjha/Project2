USE [CentralMI]
GO

/****** Object:  Table [dbo].[deliverydays]    Script Date: 7/6/2018 11:59:15 AM ******/
DROP TABLE [dbo].[deliverydays]
GO

/****** Object:  Table [dbo].[deliverydays]    Script Date: 7/6/2018 11:59:15 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[deliverydays](
	[deliverydaysid] [int] IDENTITY(1,1) NOT NULL,
	[days] [varchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[deliverydaysid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO


