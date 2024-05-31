CREATE PROCEDURE BuyChest
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