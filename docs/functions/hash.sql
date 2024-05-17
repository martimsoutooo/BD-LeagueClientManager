CREATE FUNCTION [dbo].[HashPassword](@Password NVARCHAR(4000))
RETURNS NVARCHAR(64)
AS
BEGIN
    DECLARE @HashThis NVARCHAR(4000)
    DECLARE @Hash VARBINARY(32)

    -- Use o algoritmo HASHBYTES para criar o hash SHA2_256 da senha
    SET @HashThis = @Password
    SET @Hash = HASHBYTES('SHA2_256', @HashThis)

    -- Converte o hash em uma string hexadecimal
    RETURN CONVERT(NVARCHAR(64), @Hash, 1)
END