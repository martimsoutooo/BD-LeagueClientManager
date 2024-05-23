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

CREATE FUNCTION dbo.GetChestsAndPrices()
RETURNS TABLE
AS
RETURN
(
    SELECT Ch.ID, I.Name, I.RP_Price as rp_price 
    FROM LCM.Chest Ch
    JOIN LCM.Item I ON Ch.ID = I.ID
);

