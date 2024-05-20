CREATE PROCEDURE PurchaseRP
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

