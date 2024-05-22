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