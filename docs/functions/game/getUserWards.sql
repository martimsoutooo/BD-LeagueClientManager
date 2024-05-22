CREATE FUNCTION GetUserWards(@UserID INT)
RETURNS TABLE
AS
RETURN (
    SELECT W.ID, W.Name AS Ward
    FROM LCM.Ward W
    JOIN LCM.User_Item UI ON W.ID = UI.ID_Item
    WHERE UI.ID_User = @UserID
);