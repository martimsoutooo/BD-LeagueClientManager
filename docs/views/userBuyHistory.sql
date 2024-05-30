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