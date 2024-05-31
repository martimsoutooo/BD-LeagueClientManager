CREATE VIEW LCM.View_UserBuyHistory AS
SELECT
    ui.ID_User,
    ui.ID_Item,
    i.Name,
    i.Type,
    ui.Data,
    ui.Hora
FROM LCM.User_Item ui
INNER JOIN LCM.Item i ON ui.ID_Item = i.ID;
GO

CREATE VIEW LCM.View_UserGameHistory AS
SELECT
    g.ID,
    g.Duration,
    g.Result,
    g.Outcome_RP,
    g.Outcome_BE,
    m.Name AS MapName,
    g.Data,
    g.Hora,
    us.ID_User
FROM LCM.Game g
INNER JOIN LCM.Map m ON g.ID_Map = m.ID
INNER JOIN LCM.User_Select us ON g.ID_User_Select = us.ID;
GO
