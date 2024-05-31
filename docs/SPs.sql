CREATE OR ALTER PROCEDURE BuyChampion
    @UserID INT,
    @ChampionID INT,
    @BECost INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;

        DECLARE @UserBE INT;
        SELECT @UserBE = BE FROM LCM.[User] WHERE ID = @UserID;

        BEGIN
            UPDATE LCM.[User] SET BE = BE - @BECost WHERE ID = @UserID;
            INSERT INTO LCM.User_Item (ID_User, ID_Item, Data, Hora)
            VALUES (@UserID, @ChampionID, GETDATE(), CONVERT(VARCHAR, GETDATE(), 108));

            COMMIT TRANSACTION;
            SELECT 'Success' AS Result, 'Champion purchased successfully' AS Message;
        END
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        SELECT 'Error' AS Result, ERROR_MESSAGE() AS Message;
    END CATCH
END;
GO

CREATE OR ALTER PROCEDURE BuyChest
    @UserID INT,
    @ChestID INT,
    @RPCost INT,
    @ChestType VARCHAR(50) 
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @UserRP INT;
    DECLARE @CurrentQty INT;

    SELECT @UserRP = RP FROM LCM.[User] WHERE ID = @UserID;

    IF @UserRP >= @RPCost
    BEGIN
        UPDATE LCM.[User] SET RP = RP - @RPCost WHERE ID = @UserID;

        IF @ChestType = 'Skin'
        BEGIN
            SELECT @CurrentQty = chestsSkin_qty FROM LCM.[User] WHERE ID = @UserID;
            IF @CurrentQty IS NOT NULL
            BEGIN
                UPDATE LCM.[User] SET chestsSkin_qty = chestsSkin_qty + 1 WHERE ID = @UserID;
            END
            ELSE
            BEGIN
                UPDATE LCM.[User] SET chestsSkin_qty = 1 WHERE ID = @UserID;
            END
        END
        ELSE IF @ChestType = 'Champion'
        BEGIN
            SELECT @CurrentQty = chestsChampion_qty FROM LCM.[User] WHERE ID = @UserID;
            IF @CurrentQty IS NOT NULL
            BEGIN
                UPDATE LCM.[User] SET chestsChampion_qty = chestsChampion_qty + 1 WHERE ID = @UserID;
            END
            ELSE
            BEGIN
                UPDATE LCM.[User] SET chestsChampion_qty = 1 WHERE ID = @UserID;
            END
        END
        ELSE IF @ChestType = 'Ward'
        BEGIN
            SELECT @CurrentQty = chestsWard_qty FROM LCM.[User] WHERE ID = @UserID;
            IF @CurrentQty IS NOT NULL
            BEGIN
                UPDATE LCM.[User] SET chestsWard_qty = chestsWard_qty + 1 WHERE ID = @UserID;
            END
            ELSE
            BEGIN
                UPDATE LCM.[User] SET chestsWard_qty = 1 WHERE ID = @UserID;
            END
        END

        SELECT 'Success' AS Result, 'Chest purchased successfully' AS Message;
    END
    ELSE
    BEGIN
        SELECT 'Error' AS Result, 'Not enough Riot Points' AS Message;
    END
END;
GO

CREATE OR ALTER PROCEDURE BuySkin
    @UserID INT,
    @SkinID INT,
    @RPCost INT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @UserRP INT;
    SELECT @UserRP = RP FROM LCM.[User] WHERE ID = @UserID;

    IF @UserRP >= @RPCost
    BEGIN
        UPDATE LCM.[User] SET RP = RP - @RPCost WHERE ID = @UserID;
        INSERT INTO LCM.User_Item (ID_User, ID_Item, Data, Hora)
        VALUES (@UserID, @SkinID, GETDATE(), CONVERT(VARCHAR, GETDATE(), 108)); -- Corrige a inserção de Data e Hora

        SELECT 'Success' AS Result, 'Skin purchased successfully' AS Message;
    END
	ELSE
		SELECT 'Error' AS Result, ERROR_MESSAGE() AS Message;	
END
GO

CREATE OR ALTER PROCEDURE BuyWard
    @UserID INT,
    @WardID INT,
    @RPCost INT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @UserRP INT;
    SELECT @UserRP = RP FROM LCM.[User] WHERE ID = @UserID;

    IF @UserRP >= @RPCost
    BEGIN
        UPDATE LCM.[User] SET RP = RP - @RPCost WHERE ID = @UserID;
        INSERT INTO LCM.User_Item (ID_User, ID_Item, Data, Hora)
        VALUES (@UserID, @WardID, GETDATE(), GETDATE());

        SELECT 'Success' AS Result, 'Ward purchased successfully' AS Message;
    END
    ELSE
    BEGIN
        SELECT 'Error' AS Result, 'Not enough Riot Points' AS Message;
    END
END;
GO

CREATE OR ALTER PROCEDURE CreateUser
    @Name NVARCHAR(50),
    @Email NVARCHAR(100),
    @Password NVARCHAR(100)
AS
BEGIN
    INSERT INTO LCM.[User] (Name, Email, Password, BE)
    VALUES (@Name, @Email, dbo.HashPassword(@Password), 5000);
END;
GO

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
GO

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
GO

CREATE OR ALTER PROCEDURE sp_InsertUserSelection
    @UserID INT,
    @SkinID INT,
    @ChampionID INT,
    @WardID INT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @OutputTable TABLE (ID INT);

    INSERT INTO LCM.User_Select (ID_User, ID_Skin, ID_Champion, ID_Ward)
    OUTPUT INSERTED.ID INTO @OutputTable
    VALUES (@UserID, @SkinID, @ChampionID, @WardID);

    SELECT ID FROM @OutputTable;
END;
GO

CREATE OR ALTER PROCEDURE PurchaseRP
    @UserID INT,
    @RPAmount INT
AS
BEGIN
    SET NOCOUNT ON;

    IF @RPAmount > 0
    BEGIN
        UPDATE LCM.[User] SET RP = RP + @RPAmount WHERE ID = @UserID;
        SELECT 'Success' AS Result, CAST(@RPAmount AS NVARCHAR(10)) + ' RP added successfully' AS Message;
    END
    ELSE
    BEGIN
        SELECT 'Error' AS Result, 'Invalid amount' AS Message;
    END
END;
GO

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
END;
GO

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
END;
GO

CREATE OR ALTER PROCEDURE sp_StartGame
    @ID_Map INT,
    @ID_User_Select INT
AS
BEGIN
    DECLARE @Duration INT, @Result VARCHAR(10), @Outcome_RP INT, @Data DATE, @Hora TIME, @Outcome_BE INT, @UserID INT;
    
    -- Retrieve User ID based on User_Select ID
    SELECT @UserID = ID_User FROM LCM.User_Select WHERE ID = @ID_User_Select;
    
    -- Generate random duration between 15 and 40 minutes
    SET @Duration = ROUND((RAND() * (40 - 20)) + 20, 0);
    
    -- Randomly determine the result as "Victory" or "Loss"
    IF (RAND() > 0.5)
    BEGIN
        SET @Result = 'Victory';
        SET @Outcome_RP = 50;
        SET @Outcome_BE = 750;
    END
    ELSE
    BEGIN
        SET @Result = 'Loss';
        SET @Outcome_RP = -25;
        SET @Outcome_BE = 0;
    END

    SET @Data = GETDATE();
    SET @Hora = CONVERT(TIME, GETDATE());

    INSERT INTO LCM.Game (Duration, Result, Outcome_RP, Outcome_BE, ID_Map, ID_User_Select, Data, Hora)
    VALUES (@Duration, @Result, @Outcome_RP, @Outcome_BE, @ID_Map, @ID_User_Select, @Data, @Hora);

    UPDATE LCM.[User]
    SET Rank_Points = CASE 
            WHEN Rank_Points + @Outcome_RP < 0 THEN 0 
            ELSE Rank_Points + @Outcome_RP 
         END,
    BE = BE + @Outcome_BE
    WHERE ID = @UserID;

    IF @@ERROR <> 0
    BEGIN
        RETURN;
    END

    COMMIT;
END;
GO

CREATE OR ALTER PROCEDURE VerifyUser
    @Name NVARCHAR(50),
    @Password NVARCHAR(100)
AS
BEGIN
    SELECT * FROM LCM.[User]
    WHERE Name = @Name AND Password = dbo.HashPassword(@Password);
END;
GO
