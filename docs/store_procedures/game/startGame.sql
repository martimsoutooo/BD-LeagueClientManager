CREATE PROCEDURE sp_StartGame
    @ID_Map INT,
    @ID_User_Select INT
AS
BEGIN
    DECLARE @Duration INT, @Result VARCHAR(10), @Outcome_RP INT, @Data DATE, @Hora TIME, @Outcome_BE INT;
    
    -- Generate random duration between 15 and 40 minutes
    SET @Duration = ROUND((RAND() * (40 - 15)) + 15, 0);
    
    -- Randomly determine the result as "Victory" or "Loss"
    IF (RAND() > 0.5)
    BEGIN
        SET @Result = 'Victory';
        SET @Outcome_RP = 50;
        SET @Outcome_BE = 750;
    END
    ELSE
    BEGIN
        SET @Result = 'Loss';
        SET @Outcome_RP = -40;
    END

    -- Set the current date and time
    SET @Data = GETDATE();
    SET @Hora = CONVERT(TIME, GETDATE());

    -- Insert into LCM.Game table
    INSERT INTO LCM.Game (Duration, Result, Outcome_RP, Outcome_BE, ID_Map, ID_User_Select, Data, Hora)
    VALUES (@Duration, @Result, @Outcome_RP, @Outcome_BE, @ID_Map, @ID_User_Select, @Data, @Hora);
END;
