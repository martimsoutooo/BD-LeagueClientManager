CREATE FUNCTION FilterChampions
    (@UserID INT, @Kingdom NVARCHAR(255), @Category NVARCHAR(255), @Alphabetical BIT)
RETURNS TABLE
AS
RETURN (
    SELECT C.ID, C.Name, C.BE_Price, C.Category, C.Kingdom 
    FROM LCM.Champion C
    WHERE C.ID NOT IN (
        SELECT UI.ID_Item FROM LCM.User_Item UI WHERE UI.ID_User = @UserID
    )
    AND (@Kingdom = 'all' OR C.Kingdom = @Kingdom)
    AND (@Category = 'all' OR C.Category = @Category)
    ORDER BY
        CASE WHEN @Alphabetical = 1 THEN C.Name ELSE C.ID END
);
GO
