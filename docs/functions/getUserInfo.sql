CREATE FUNCTION GetUserInfo(@UserID INT)
RETURNS TABLE
AS
RETURN (
    SELECT Rank_Points, RP, BE, Rank
    FROM LCM.[User]
    WHERE ID = @UserID
);