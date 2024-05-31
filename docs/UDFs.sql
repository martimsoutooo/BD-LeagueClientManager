CREATE FUNCTION GetChampionsByUser (@UserID INT)
RETURNS TABLE
AS
RETURN
(
    SELECT C.ID, C.Name, C.Category, C.Kingdom 
    FROM LCM.Champion C
    JOIN LCM.User_Item UI ON C.ID = UI.ID_Item
    WHERE UI.ID_User = @UserID
);
GO

CREATE FUNCTION GetSkinsByUser (@UserID INT)
RETURNS TABLE
AS
RETURN
(
    SELECT S.ID, S.Name AS skin, C.Name AS championName
    FROM LCM.Skin S
    JOIN LCM.Champion C ON S.Champion_ID = C.ID
    JOIN LCM.User_Item UI ON S.ID = UI.ID_Item
    WHERE UI.ID_User = @UserID
);
GO

CREATE FUNCTION GetWardsByUser (@UserID INT)
RETURNS TABLE
AS
RETURN
(
    SELECT W.ID, W.Name AS ward
    FROM LCM.Ward W
    JOIN LCM.User_Item UI ON W.ID = UI.ID_Item
    WHERE UI.ID_User = @UserID
);
GO

CREATE FUNCTION GetChestsByUser (@UserID INT)
RETURNS TABLE
AS
RETURN
(
    SELECT CH.ID, I.Name AS chest, I.RP_Price AS rp_price
    FROM LCM.Chest CH
    JOIN LCM.User_Item UI ON CH.ID = UI.ID_Item
    JOIN LCM.Item I ON CH.ID = I.ID
    WHERE UI.ID_User = @UserID
);
GO

CREATE FUNCTION GetAvailableChampionsForUser (@UserID INT)
RETURNS TABLE
AS
RETURN
(
    SELECT C.ID, C.Name, C.BE_Price, C.Category, C.Kingdom 
    FROM LCM.Champion C
    WHERE C.ID NOT IN (
        SELECT UI.ID_Item 
        FROM LCM.User_Item UI 
        WHERE UI.ID_User = @UserID
    )
);
GO

CREATE FUNCTION GetAvailableSkinsForUser (@UserID INT)
RETURNS TABLE
AS
RETURN
(
    SELECT S.ID, S.Name AS skin, C.Name AS champion, S.RP_Price as rp_price
    FROM LCM.Skin S
    JOIN LCM.Champion C ON S.Champion_ID = C.ID
    WHERE S.ID NOT IN (
        SELECT UI.ID_Item
        FROM LCM.User_Item UI
        WHERE UI.ID_User = @UserID
    ) AND S.Name <> 'default'
);
GO

CREATE FUNCTION GetAvailableWardsForUser (@UserID INT)
RETURNS TABLE
AS
RETURN
(
    SELECT W.ID, W.Name, I.RP_Price as rp_price 
    FROM LCM.Ward W
    JOIN LCM.Item I ON W.ID = I.ID
    WHERE W.ID NOT IN (
        SELECT UI.ID_Item 
        FROM LCM.User_Item UI 
        WHERE UI.ID_User = @UserID
    )
);
GO

CREATE FUNCTION GetChestsAndPrices()
RETURNS TABLE
AS
RETURN
(
    SELECT Ch.ID, I.Name, I.RP_Price as rp_price 
    FROM LCM.Chest Ch
    JOIN LCM.Item I ON Ch.ID = I.ID
);
GO

CREATE FUNCTION GetUserByEmail
    (@Email NVARCHAR(255))
RETURNS TABLE
AS
RETURN 
(
    SELECT ID, Name, Email, Password
    FROM LCM.[User]
    WHERE Email = @Email
);
GO

CREATE FUNCTION GetUserByUsername
    (@Username NVARCHAR(255))
RETURNS TABLE
AS
RETURN 
(
    SELECT ID, Name, Email, Password
    FROM LCM.[User]
    WHERE Name = @Username
);
GO

CREATE FUNCTION GetUserInfo(@UserID INT)
RETURNS TABLE
AS
RETURN (
    SELECT Rank_Points, RP, BE, Rank
    FROM LCM.[User]
    WHERE ID = @UserID
);
GO

CREATE OR ALTER FUNCTION GetUserSkinsFromChampion(@UserID INT, @ChampionID INT)
RETURNS TABLE
AS
RETURN (
    SELECT S.ID, S.Name AS Skin, C.Name AS ChampionName
    FROM LCM.Skin S
    JOIN LCM.Champion C ON S.Champion_ID = C.ID
    JOIN LCM.User_Item UI ON S.ID = UI.ID_Item
    WHERE UI.ID_User = @UserID AND C.ID = @ChampionID
);
GO

CREATE FUNCTION [dbo].[HashPassword](@Password NVARCHAR(4000))
RETURNS NVARCHAR(64)
AS
BEGIN
    DECLARE @HashThis NVARCHAR(4000)
    DECLARE @Hash VARBINARY(32)

    SET @HashThis = @Password
    SET @Hash = HASHBYTES('SHA2_256', @HashThis)

    RETURN CONVERT(NVARCHAR(64), @Hash, 1)
END
GO
