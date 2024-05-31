CREATE TRIGGER trg_check_skin_purchase
ON LCM.User_Item
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @user_id INT, @item_id INT, @champion_id INT;

    SELECT @user_id = inserted.ID_User, @item_id = inserted.ID_Item
    FROM inserted
    JOIN LCM.Skin ON inserted.ID_Item = LCM.Skin.ID;

    IF @item_id IS NULL
        RETURN;

    SELECT @champion_id = Champion_ID
    FROM LCM.Skin
    WHERE ID = @item_id;

    IF NOT EXISTS (
        SELECT 1
        FROM LCM.User_Item
        WHERE ID_User = @user_id
        AND ID_Item = @champion_id
    )
    BEGIN
        RAISERROR ('You do not own the required champion to purchase this skin', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
GO

CREATE TRIGGER trg_check_points
ON LCM.[User]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @user_id INT, @new_rp INT, @new_be INT;

    SELECT @user_id = ID, @new_rp = RP, @new_be = BE
    FROM inserted;

    IF (@new_rp < 0 OR @new_be < 0)
    BEGIN
        RAISERROR ('RP or BE cannot be negative', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
GO
