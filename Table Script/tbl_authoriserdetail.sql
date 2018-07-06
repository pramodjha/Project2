USE [CentralMI]
GO

ALTER TABLE [dbo].[authoriserdetail] DROP CONSTRAINT [FK__authorise__usern__5B638405]
GO

/****** Object:  Table [dbo].[authoriserdetail]    Script Date: 7/6/2018 11:54:59 AM ******/
DROP TABLE [dbo].[authoriserdetail]
GO

/****** Object:  Table [dbo].[authoriserdetail]    Script Date: 7/6/2018 11:54:59 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[authoriserdetail](
	[authoriserid] [int] IDENTITY(1,1) NOT NULL,
	[username] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[authoriserid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[authoriserdetail]  WITH CHECK ADD FOREIGN KEY([username])
REFERENCES [dbo].[auth_user] ([id])
GO


