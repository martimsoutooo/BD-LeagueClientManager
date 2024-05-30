CREATE OR ALTER PROCEDURE CreateUser
    @Name NVARCHAR(50),
    @Email NVARCHAR(100),
    @Password NVARCHAR(100)
AS
BEGIN
    INSERT INTO LCM.[User] (Name, Email, Password,BE)
    VALUES (@Name, @Email, dbo.HashPassword(@Password), 5000);
END;
