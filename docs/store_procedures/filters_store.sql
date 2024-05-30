CREATE OR ALTER PROCEDURE GetFilteredDataStore
    @UserID INT,
    @Type NVARCHAR(50),
    @Alphabetical BIT,
    @Filter1 NVARCHAR(50),
    @Filter2 NVARCHAR(50)
AS
BEGIN
    IF @Type = 'Champion'
    BEGIN
        SELECT ID, Name, Category, BE_Price, Kingdom
        FROM GetAvailableChampionsForUser(@UserID)
        WHERE (@Filter1 = 'all' OR Kingdom = @Filter1)
        AND (@Filter2 = 'all' OR Category = @Filter2)
        ORDER BY 
            CASE WHEN @Alphabetical = 1 THEN Name END ASC,
            CASE WHEN @Alphabetical = 0 THEN ID END ASC
    END
    ELSE IF @Type = 'Skin'
    BEGIN
        SELECT ID, skin, champion, rp_price
        FROM GetAvailableSkinsForUser(@UserID)
        WHERE (@Filter1 = 'all' OR champion = @Filter1)
        ORDER BY 
            CASE WHEN @Alphabetical = 1 THEN skin END ASC,
            CASE WHEN @Alphabetical = 0 THEN ID END ASC
    END
    ELSE IF @Type = 'Ward'
    BEGIN
        SELECT Name, ID, rp_price
        FROM GetAvailableWardsForUser(@UserID)
        WHERE (@Filter1 = 'all' OR Name LIKE '%' + @Filter1 + '%')
        ORDER BY 
            CASE WHEN @Alphabetical = 1 THEN Name END ASC,
            CASE WHEN @Alphabetical = 0 THEN ID END ASC
    END
END