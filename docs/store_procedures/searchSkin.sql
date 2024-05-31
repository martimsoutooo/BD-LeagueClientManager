CREATE OR ALTER PROCEDURE SearchSkins
    @UserID INT,
    @SearchQuery NVARCHAR(255),
    @MaxResults INT = 50 
AS
BEGIN
    SET NOCOUNT ON;

    SELECT TOP(@MaxResults) S.ID, S.Name AS skin, C.Name as champion, S.RP_Price
    FROM LCM.Skin S
    JOIN LCM.Champion C ON S.Champion_ID = C.ID
    WHERE S.Name LIKE '%' + @SearchQuery + '%'
    AND S.ID NOT IN (SELECT ID_Item FROM LCM.User_Item WHERE ID_User = @UserID)
    ORDER BY S.Name;
END