USE [CentralMI]
GO

ALTER TABLE [dbo].[requestsubcategory] DROP CONSTRAINT [FK__requestsu__reque__0DEF03D2]
GO

ALTER TABLE [dbo].[requestsubcategory] DROP CONSTRAINT [DF__requestsu__reque__0CFADF99]
GO

/****** Object:  Table [dbo].[requestsubcategory]    Script Date: 7/6/2018 12:10:20 PM ******/
DROP TABLE [dbo].[requestsubcategory]
GO

/****** Object:  Table [dbo].[requestsubcategory]    Script Date: 7/6/2018 12:10:20 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[requestsubcategory](
	[requestsubcategoryid] [int] IDENTITY(1,1) NOT NULL,
	[requestsubcategorydatetime] [datetime] NOT NULL,
	[requestcategorys] [int] NULL,
	[requestsubcategory] [varchar](100) NULL,
	[core_noncore] [varchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[requestsubcategoryid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[requestsubcategory] ADD  DEFAULT (getdate()) FOR [requestsubcategorydatetime]
GO

ALTER TABLE [dbo].[requestsubcategory]  WITH CHECK ADD FOREIGN KEY([requestcategorys])
REFERENCES [dbo].[requestcategorys] ([requestcategoryid])
GO


