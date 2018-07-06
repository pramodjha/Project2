USE [CentralMI]
GO

ALTER TABLE [dbo].[mimember] DROP CONSTRAINT [FK__mimember__userna__611C5D5B]
GO

ALTER TABLE [dbo].[mimember] DROP CONSTRAINT [FK__mimember__teamde__62108194]
GO

/****** Object:  Table [dbo].[mimember]    Script Date: 7/6/2018 12:06:06 PM ******/
DROP TABLE [dbo].[mimember]
GO

/****** Object:  Table [dbo].[mimember]    Script Date: 7/6/2018 12:06:06 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[mimember](
	[mimemberid] [int] IDENTITY(1,1) NOT NULL,
	[username] [int] NOT NULL,
	[teamdetail] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[mimemberid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[mimember]  WITH CHECK ADD FOREIGN KEY([teamdetail])
REFERENCES [dbo].[teamdetail] ([teamid])
GO

ALTER TABLE [dbo].[mimember]  WITH CHECK ADD FOREIGN KEY([username])
REFERENCES [dbo].[auth_user] ([id])
GO


