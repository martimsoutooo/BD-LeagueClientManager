CREATE PROCEDURE sp_InsertUserSelection
    @UserID INT,
    @SkinID INT,
    @ChampionID INT,
    @WardID INT
AS
BEGIN
    INSERT INTO LCM.User_Select (ID_User, ID_Skin, ID_Champion, ID_Ward)
    VALUES (@UserID, @SkinID, @ChampionID, @WardID)
END
