USE [CentralMI]
GO

/****** Object:  Table [dbo].[delivery_days]    Script Date: 7/6/2018 11:58:49 AM ******/
DROP TABLE [dbo].[delivery_days]
GO

/****** Object:  Table [dbo].[delivery_days]    Script Date: 7/6/2018 11:58:49 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[delivery_days](
	[delivery_daysid] [int] IDENTITY(1,1) NOT NULL,
	[delivery_days] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[delivery_daysid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO


