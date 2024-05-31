CREATE PROCEDURE sp_InsertUserSelection
    @UserID INT,
    @SkinID INT,
    @ChampionID INT,
    @WardID INT
AS
BEGIN
    SET NOCOUNT ON

    DECLARE @OutputTable TABLE (ID INT);

    INSERT INTO LCM.User_Select (ID_User, ID_Skin, ID_Champion, ID_Ward)
    OUTPUT INSERTED.ID INTO @OutputTable
    VALUES (@UserID, @SkinID, @ChampionID, @WardID);

    SELECT ID FROM @OutputTable;
END
