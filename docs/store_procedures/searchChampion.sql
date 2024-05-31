CREATE OR ALTER PROCEDURE SearchChampions
    @UserID INT,
    @SearchQuery NVARCHAR(255),
    @MaxResults INT = 50 
AS
BEGIN
    SET NOCOUNT ON;

    SELECT TOP(@MaxResults) C.ID, C.Name AS champion, C.Category, C.BE_Price, C.Kingdom
    FROM LCM.Champion C
    WHERE C.Name LIKE '%' + @SearchQuery + '%'
    AND C.ID NOT IN (SELECT ID_Item FROM LCM.User_Item WHERE ID_User = @UserID)
    ORDER BY C.Name;
END
GO