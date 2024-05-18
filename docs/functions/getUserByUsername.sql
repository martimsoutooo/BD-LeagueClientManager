CREATE FUNCTION GetUserByUsername
    (@Username NVARCHAR(255))
RETURNS TABLE
AS
RETURN 
(
    SELECT ID, Name, Email, Password
    FROM LCM.[User]
    WHERE Name = @Username
);
GO