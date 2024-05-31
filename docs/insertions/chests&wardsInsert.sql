-- Inser��es na tabela Item para Wards
INSERT INTO LCM.Item (Name, Type, BE_Price, RP_Price) VALUES ('Ward of Vision', 'Ward', 0, 500);
INSERT INTO LCM.Item (Name, Type, BE_Price, RP_Price) VALUES ('Ward of Shadows', 'Ward', 0, 600);
INSERT INTO LCM.Item (Name, Type, BE_Price, RP_Price) VALUES ('Ward of Light', 'Ward', 0, 700);
INSERT INTO LCM.Item (Name, Type, BE_Price, RP_Price) VALUES ('Ward of Mystery', 'Ward', 0, 800);
INSERT INTO LCM.Item (Name, Type, BE_Price, RP_Price) VALUES ('Ward of Power', 'Ward', 0, 900);
INSERT INTO LCM.Item (Name, Type, BE_Price, RP_Price) VALUES ('Ward of Protection', 'Ward', 0, 1000);
INSERT INTO LCM.Item (Name, Type, BE_Price, RP_Price) VALUES ('Ward of Stealth', 'Ward', 0, 1100);
INSERT INTO LCM.Item (Name, Type, BE_Price, RP_Price) VALUES ('Ward of the Ancients', 'Ward', 0, 1200);
INSERT INTO LCM.Item (Name, Type, BE_Price, RP_Price) VALUES ('Ward of the Forest', 'Ward', 0, 1300);
INSERT INTO LCM.Item (Name, Type, BE_Price, RP_Price) VALUES ('Ward of the Sea', 'Ward', 0, 1400);

-- Inser��es na tabela Item para Chests
INSERT INTO LCM.Item (Name, Type, BE_Price, RP_Price) VALUES ('Champion Chest', 'Chest', 0, 1000);
INSERT INTO LCM.Item (Name, Type, BE_Price, RP_Price) VALUES ('Skin Chest', 'Chest', 0, 1500);
INSERT INTO LCM.Item (Name, Type, BE_Price, RP_Price) VALUES ('Ward Chest', 'Chest', 0, 500);

-- Inser��es na tabela Ward
INSERT INTO LCM.Ward (ID, Name) VALUES ((SELECT ID FROM LCM.Item WHERE Name = 'Ward of Vision'), 'Ward of Vision');
INSERT INTO LCM.Ward (ID, Name) VALUES ((SELECT ID FROM LCM.Item WHERE Name = 'Ward of Shadows'), 'Ward of Shadows');
INSERT INTO LCM.Ward (ID, Name) VALUES ((SELECT ID FROM LCM.Item WHERE Name = 'Ward of Light'), 'Ward of Light');
INSERT INTO LCM.Ward (ID, Name) VALUES ((SELECT ID FROM LCM.Item WHERE Name = 'Ward of Mystery'), 'Ward of Mystery');
INSERT INTO LCM.Ward (ID, Name) VALUES ((SELECT ID FROM LCM.Item WHERE Name = 'Ward of Power'), 'Ward of Power');
INSERT INTO LCM.Ward (ID, Name) VALUES ((SELECT ID FROM LCM.Item WHERE Name = 'Ward of Protection'), 'Ward of Protection');
INSERT INTO LCM.Ward (ID, Name) VALUES ((SELECT ID FROM LCM.Item WHERE Name = 'Ward of Stealth'), 'Ward of Stealth');
INSERT INTO LCM.Ward (ID, Name) VALUES ((SELECT ID FROM LCM.Item WHERE Name = 'Ward of the Ancients'), 'Ward of the Ancients');
INSERT INTO LCM.Ward (ID, Name) VALUES ((SELECT ID FROM LCM.Item WHERE Name = 'Ward of the Forest'), 'Ward of the Forest');
INSERT INTO LCM.Ward (ID, Name) VALUES ((SELECT ID FROM LCM.Item WHERE Name = 'Ward of the Sea'), 'Ward of the Sea');

-- Inser��es na tabela Chest
INSERT INTO LCM.Chest (ID) VALUES ((SELECT ID FROM LCM.Item WHERE Name = 'Champion Chest'));
INSERT INTO LCM.Chest (ID) VALUES ((SELECT ID FROM LCM.Item WHERE Name = 'Skin Chest'));
INSERT INTO LCM.Chest (ID) VALUES ((SELECT ID FROM LCM.Item WHERE Name = 'Ward Chest'));

-- Inser��es na tabela Map
INSERT INTO LCM.Map (ID, Name) VALUES (1, 'Summoners Rift');
INSERT INTO LCM.Map (ID, Name) VALUES (2, 'Howling Abyss');
INSERT INTO LCM.Map (ID, Name) VALUES (3, 'Twisted Treeline');

