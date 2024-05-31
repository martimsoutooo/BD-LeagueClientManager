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