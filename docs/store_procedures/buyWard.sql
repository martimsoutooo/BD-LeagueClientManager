CREATE PROCEDURE BuyWard
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