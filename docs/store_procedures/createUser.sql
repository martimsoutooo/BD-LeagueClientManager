CREATE PROCEDURE CreateUser
    @Username NVARCHAR(50),
    @Email NVARCHAR(50),
    @Password NVARCHAR(50)
AS
BEGIN
    DECLARE @HashedPassword NVARCHAR(256);
    SET @HashedPassword = HASHBYTES('SHA2_256', @Password); 

    INSERT INTO LCM.[User] (Name, Email, Password)
    VALUES (@Username, @Email, @HashedPassword);

    RETURN SCOPE_IDENTITY();
END;
