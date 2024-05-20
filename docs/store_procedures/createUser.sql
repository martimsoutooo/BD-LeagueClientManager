CREATE PROCEDURE CreateUser
    @Name NVARCHAR(50),
    @Email NVARCHAR(100),
    @Password NVARCHAR(100)
AS
BEGIN
    INSERT INTO LCM.[User] (Name, Email, Password)
    VALUES (@Name, @Email, dbo.HashPassword(@Password));
END;
