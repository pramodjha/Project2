USE [CentralMI]
GO

ALTER TABLE [dbo].[estimationdetail] DROP CONSTRAINT [FK__estimatio__reque__7ADC2F5E]
GO

ALTER TABLE [dbo].[estimationdetail] DROP CONSTRAINT [FK__estimatio__estim__79E80B25]
GO

ALTER TABLE [dbo].[estimationdetail] DROP CONSTRAINT [DF__estimatio__estim__78F3E6EC]
GO

/****** Object:  Table [dbo].[estimationdetail]    Script Date: 7/6/2018 12:00:48 PM ******/
DROP TABLE [dbo].[estimationdetail]
GO

/****** Object:  Table [dbo].[estimationdetail]    Script Date: 7/6/2018 12:00:48 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[estimationdetail](
	[estimationid] [int] IDENTITY(1,1) NOT NULL,
	[estimationdate] [datetime] NOT NULL,
	[estimatedby] [int] NULL,
	[estimateddays] [int] NULL,
	[requestdetail] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[estimationid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[estimationdetail] ADD  DEFAULT (getdate()) FOR [estimationdate]
GO

ALTER TABLE [dbo].[estimationdetail]  WITH CHECK ADD FOREIGN KEY([estimatedby])
REFERENCES [dbo].[mimember] ([mimemberid])
GO

ALTER TABLE [dbo].[estimationdetail]  WITH CHECK ADD FOREIGN KEY([requestdetail])
REFERENCES [dbo].[requestdetail] ([requestid])
GO


