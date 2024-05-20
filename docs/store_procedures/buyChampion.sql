CREATE PROCEDURE BuyChampion
    @UserID INT,
    @ChampionID INT,
    @BECost INT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @UserBE INT;
    SELECT @UserBE = BE FROM LCM.[User] WHERE ID = @UserID;

    IF @UserBE >= @BECost
    BEGIN
        UPDATE LCM.[User] SET BE = BE - @BECost WHERE ID = @UserID;
        INSERT INTO LCM.User_Item (ID_User, ID_Item, Data, Hora)
        VALUES (@UserID, @ChampionID, GETDATE(), GETDATE());

        SELECT 'Success' AS Result, 'Champion purchased successfully' AS Message;
    END
    ELSE
    BEGIN
        SELECT 'Error' AS Result, 'Not enough Blue Essence' AS Message;
    END
END;

