CREATE FUNCTION GetUserByEmail
    (@Email NVARCHAR(255))
RETURNS TABLE
AS
RETURN 
(
    SELECT ID, Name, Email, Password
    FROM LCM.[User]
    WHERE Email = @Email
);
GO