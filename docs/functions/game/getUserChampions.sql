CREATE FUNCTION GetUserChampions(@UserID INT)
RETURNS TABLE
AS
RETURN (
    SELECT C.ID, C.Name, C.Category, C.Kingdom 
    FROM LCM.Champion C
    JOIN LCM.User_Item UI ON C.ID = UI.ID_Item
    WHERE UI.ID_User = @UserID
);