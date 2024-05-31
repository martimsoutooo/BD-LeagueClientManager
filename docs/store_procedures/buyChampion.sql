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
