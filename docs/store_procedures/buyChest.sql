CREATE PROCEDURE BuyChest
    @UserID INT,
    @ChestID INT,
    @RPCost INT,
    @ChestType VARCHAR(50)  -- Tipo do chest: 'Skin', 'Champion', ou 'Ward'
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @UserRP INT;
    DECLARE @CurrentQty INT;

    -- Obter a quantidade atual de Riot Points (RP) do usuário
    SELECT @UserRP = RP FROM LCM.[User] WHERE ID = @UserID;

    -- Verificar se o usuário tem RP suficiente
    IF @UserRP >= @RPCost
    BEGIN
        -- Decrementar a quantidade de RP do usuário
        UPDATE LCM.[User] SET RP = RP - @RPCost WHERE ID = @UserID;

        -- Verificar a quantidade atual do tipo de chest e atualizar conforme necessário
        IF @ChestType = 'Skin'
        BEGIN
            SELECT @CurrentQty = chestsSkin_qty FROM LCM.[User] WHERE ID = @UserID;
            IF @CurrentQty IS NOT NULL
            BEGIN
                UPDATE LCM.[User] SET chestsSkin_qty = chestsSkin_qty + 1 WHERE ID = @UserID;
            END
            ELSE
            BEGIN
                UPDATE LCM.[User] SET chestsSkin_qty = 1 WHERE ID = @UserID;
            END
        END
        ELSE IF @ChestType = 'Champion'
        BEGIN
            SELECT @CurrentQty = chestsChampion_qty FROM LCM.[User] WHERE ID = @UserID;
            IF @CurrentQty IS NOT NULL
            BEGIN
                UPDATE LCM.[User] SET chestsChampion_qty = chestsChampion_qty + 1 WHERE ID = @UserID;
            END
            ELSE
            BEGIN
                UPDATE LCM.[User] SET chestsChampion_qty = 1 WHERE ID = @UserID;
            END
        END
        ELSE IF @ChestType = 'Ward'
        BEGIN
            SELECT @CurrentQty = chestsWard_qty FROM LCM.[User] WHERE ID = @UserID;
            IF @CurrentQty IS NOT NULL
            BEGIN
                UPDATE LCM.[User] SET chestsWard_qty = chestsWard_qty + 1 WHERE ID = @UserID;
            END
            ELSE
            BEGIN
                UPDATE LCM.[User] SET chestsWard_qty = 1 WHERE ID = @UserID;
            END
        END

        -- Retornar mensagem de sucesso
        SELECT 'Success' AS Result, 'Chest purchased successfully' AS Message;
    END
    ELSE
    BEGIN
        -- Retornar mensagem de erro
        SELECT 'Error' AS Result, 'Not enough Riot Points' AS Message;
    END
END;