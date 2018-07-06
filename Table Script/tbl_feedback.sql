USE [CentralMI]
GO

ALTER TABLE [dbo].[feedback] DROP CONSTRAINT [FK__feedback__report__6A70BD6B]
GO

ALTER TABLE [dbo].[feedback] DROP CONSTRAINT [FK__feedback__feedba__5FF32EF8]
GO

ALTER TABLE [dbo].[feedback] DROP CONSTRAINT [DF__feedback__feedba__5EFF0ABF]
GO

/****** Object:  Table [dbo].[feedback]    Script Date: 7/6/2018 12:01:19 PM ******/
DROP TABLE [dbo].[feedback]
GO

/****** Object:  Table [dbo].[feedback]    Script Date: 7/6/2018 12:01:19 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[feedback](
	[feedback_id] [int] IDENTITY(1,1) NOT NULL,
	[feedback_date] [datetime] NOT NULL,
	[feedback_question] [int] NOT NULL,
	[feedback_integer] [int] NULL,
	[feedback_text] [varchar](255) NULL,
	[feedback_datetime] [datetime] NULL,
	[reports] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[feedback_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[feedback] ADD  DEFAULT (getdate()) FOR [feedback_date]
GO

ALTER TABLE [dbo].[feedback]  WITH CHECK ADD FOREIGN KEY([feedback_question])
REFERENCES [dbo].[feedback_question] ([feedback_questionid])
GO

ALTER TABLE [dbo].[feedback]  WITH CHECK ADD FOREIGN KEY([reports])
REFERENCES [dbo].[reports] ([reportid])
GO


