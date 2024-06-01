CREATE SCHEMA LCM
GO


CREATE TABLE LCM.[User] (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(255) UNIQUE NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Rank_Points INT DEFAULT 0,
    chestsSkin_qty INT DEFAULT 0,
    chestsChampion_qty INT DEFAULT 0,
    chestsWard_qty INT DEFAULT 0,
    BE INT DEFAULT 0,
    RP INT DEFAULT 0
);
GO


CREATE TABLE LCM.Item (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(50) NOT NULL,
    Type VARCHAR(50) NOT NULL,
    BE_Price INT DEFAULT 0,
    RP_Price INT DEFAULT 0
);
GO


CREATE TABLE LCM.User_Item (
    ID_User INT,
    ID_Item INT,
    Data DATE,
    Hora TIME,
    PRIMARY KEY (ID_User, ID_Item),
    FOREIGN KEY (ID_User) REFERENCES LCM.[User](ID),
    FOREIGN KEY (ID_Item) REFERENCES LCM.Item(ID)
);
GO


CREATE TABLE LCM.Champion (
    ID INT PRIMARY KEY,
    Name VARCHAR(50),
    BE_Price INT,
    Category VARCHAR(50),
    Kingdom VARCHAR(50),
    FOREIGN KEY (ID) REFERENCES LCM.Item(ID)
);
GO


CREATE TABLE LCM.Skin (
    ID INT PRIMARY KEY,
    Champion_ID INT,
    RP_Price INT,
    Name VARCHAR(50),
    FOREIGN KEY (Champion_ID) REFERENCES LCM.Item(ID)
);
GO


CREATE TABLE LCM.Chest (
    ID INT PRIMARY KEY,
    FOREIGN KEY (ID) REFERENCES LCM.Item(ID)
);
GO


CREATE TABLE LCM.Ward (
    ID INT PRIMARY KEY,
    Name VARCHAR(50),
    FOREIGN KEY (ID) REFERENCES LCM.Item(ID)
);
GO

CREATE TABLE LCM.User_Select (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    ID_User INT,
    ID_Skin INT,
    ID_Champion INT,
    ID_Ward INT,
    FOREIGN KEY (ID_User) REFERENCES LCM.[User](ID),
    FOREIGN KEY (ID_Skin) REFERENCES LCM.Skin(ID),
    FOREIGN KEY (ID_Champion) REFERENCES LCM.Champion(ID),
    FOREIGN KEY (ID_Ward) REFERENCES LCM.Ward(ID)
);
GO


CREATE TABLE LCM.Map (
    ID INT PRIMARY KEY,
    Name VARCHAR(50)
);
GO


CREATE TABLE LCM.Game (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Duration INT,
    Result VARCHAR(10),
    Outcome_RP INT,
    Outcome_BE INT,
    ID_Map INT,
    ID_User_Select INT,
    Data DATE,
    Hora TIME, 
    FOREIGN KEY (ID_Map) REFERENCES LCM.Map(ID),
    FOREIGN KEY (ID_User_Select) REFERENCES LCM.User_Select(ID)
);
GO


ALTER TABLE LCM.[User]
ADD Rank AS (
    CASE
        WHEN Rank_Points >= 800 THEN 'Challenger'
        WHEN Rank_Points >= 700 THEN 'Grandmaster'
        WHEN Rank_Points >= 600 THEN 'Master'
        WHEN Rank_Points >= 500 THEN 'Diamond'
        WHEN Rank_Points >= 400 THEN 'Platinum'
        WHEN Rank_Points >= 300 THEN 'Gold'
        WHEN Rank_Points >= 200 THEN 'Silver'
        WHEN Rank_Points >= 100 THEN 'Bronze'
        WHEN Rank_Points >= 1 THEN 'Iron'
        ELSE 'Unranked'
    END
);
GO