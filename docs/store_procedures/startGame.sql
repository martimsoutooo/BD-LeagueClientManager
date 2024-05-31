CREATE PROCEDURE sp_StartGame
    @ID_Map INT,
    @ID_User_Select INT
AS
BEGIN
    DECLARE @Duration INT, @Result VARCHAR(10), @Outcome_RP INT, @Data DATE, @Hora TIME, @Outcome_BE INT, @UserID INT;
    
    -- Retrieve User ID based on User_Select ID
    SELECT @UserID = ID_User FROM LCM.User_Select WHERE ID = @ID_User_Select;
    
    -- Generate random duration between 15 and 40 minutes
    SET @Duration = ROUND((RAND() * (40 - 20)) + 20, 0);
    
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
        SET @Outcome_RP = -25;
        SET @Outcome_BE = 0;
    END


    SET @Data = GETDATE();
    SET @Hora = CONVERT(TIME, GETDATE());

    INSERT INTO LCM.Game (Duration, Result, Outcome_RP, Outcome_BE, ID_Map, ID_User_Select, Data, Hora)
    VALUES (@Duration, @Result, @Outcome_RP, @Outcome_BE, @ID_Map, @ID_User_Select, @Data, @Hora);


    UPDATE LCM.[User]
    SET Rank_Points = CASE 
            WHEN Rank_Points + @Outcome_RP < 0 THEN 0 
            ELSE Rank_Points + @Outcome_RP 
         END,
    BE = BE + @Outcome_BE
WHERE ID = @UserID;
    

    IF @@ERROR <> 0
    BEGIN

        RETURN;
    END

    COMMIT;
END;