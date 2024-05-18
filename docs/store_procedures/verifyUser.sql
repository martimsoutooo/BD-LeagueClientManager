CREATE PROCEDURE VerifyUser
    @Username NVARCHAR(255),
    @Password NVARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @HashedPassword NVARCHAR(255);

    SET @HashedPassword = CONVERT(NVARCHAR(255), HASHBYTES('SHA2_256', @Password), 2);

    SELECT *
    FROM LCM.[User]
    WHERE Name = @Username AND Password = @HashedPassword;
END;
GO