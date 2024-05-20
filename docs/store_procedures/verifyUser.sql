CREATE PROCEDURE VerifyUser
    @Name NVARCHAR(50),
    @Password NVARCHAR(100)
AS
BEGIN
    SELECT * FROM LCM.[User]
    WHERE Name = @Name AND Password = dbo.HashPassword(@Password);
END;
