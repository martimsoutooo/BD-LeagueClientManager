CREATE OR ALTER PROCEDURE GetFilteredData
    @UserID INT,
    @Type NVARCHAR(50),
    @Alphabetical BIT,
    @Filter1 NVARCHAR(50),
    @Filter2 NVARCHAR(50)
AS
BEGIN
    IF @Type = 'Champion'
    BEGIN
        SELECT ID, Name, Category, Kingdom 
        FROM GetChampionsByUser(@UserID)
        WHERE (@Filter1 = 'all' OR Kingdom = @Filter1)
        AND (@Filter2 = 'all' OR Category = @Filter2)
        ORDER BY 
            CASE WHEN @Alphabetical = 1 THEN Name END ASC,
            CASE WHEN @Alphabetical = 0 THEN ID END ASC
    END
    ELSE IF @Type = 'Skin'
    BEGIN
        SELECT ID, skin, championName 
        FROM GetSkinsByUser(@UserID)
        WHERE (@Filter1 = 'all' OR championName = @Filter1)
        ORDER BY 
            CASE WHEN @Alphabetical = 1 THEN skin END ASC,
            CASE WHEN @Alphabetical = 0 THEN ID END ASC
    END
    ELSE IF @Type = 'Ward'
    BEGIN
        SELECT ID, ward 
        FROM GetWardsByUser(@UserID)
        WHERE (@Filter1 = 'all' OR ward LIKE '%' + @Filter1 + '%')
        ORDER BY 
            CASE WHEN @Alphabetical = 1 THEN ward END ASC,
            CASE WHEN @Alphabetical = 0 THEN ID END ASC
    END
END
