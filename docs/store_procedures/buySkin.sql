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
