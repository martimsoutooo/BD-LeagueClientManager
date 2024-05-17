CREATE SCHEMA LCM
GO

-- Tabela User
CREATE TABLE LCM.[User] (
	ID INT PRIMARY KEY IDENTITY(1,1),
	Name VARCHAR(255) UNIQUE NOT NULL,
	Email VARCHAR(255) UNIQUE NOT NULL,
	Password VARCHAR(255) NOT NULL,
	Rank_Points INT DEFAULT 0,
	BE INT DEFAULT 0,
	RP INT DEFAULT 0
)

-- Tabela Item
CREATE TABLE LCM.Item (
    ID INT PRIMARY KEY,
    Name VARCHAR(36)
);

-- Tabela User_Item
CREATE TABLE LCM.User_Item (
    ID_User INT,
    ID_Item INT,
    Data DATE,
    Hora TIME,
    PRIMARY KEY (ID_User, ID_Item),
    FOREIGN KEY (ID_User) REFERENCES LCM.[User](ID),
    FOREIGN KEY (ID_Item) REFERENCES LCM.Item(ID)
);

-- Tabela Item_Type
CREATE TABLE LCM.Item_Type (
    ID INT PRIMARY KEY,
    Name VARCHAR(50),
    RP_Price INT
);

--Tabela Champion
CREATE TABLE LCM.Champion (
    ID_Item_Type INT PRIMARY KEY,
    Name VARCHAR(50),
    BE_Price INT,
    Category VARCHAR(50),
    Kingdom VARCHAR(50),
    FOREIGN KEY (ID_Item_Type) REFERENCES LCM.Item_Type(ID)
);

--Tabela Skin
CREATE TABLE LCM.Skin (
	Skin_ID INT PRIMARY KEY,
    Champion_ID INT,
	RP_Price INT,
    Name VARCHAR(50),
	FOREIGN KEY (Champion_ID) REFERENCES LCM.Champion(ID_Item_Type)
);

--Tabela Chest
CREATE TABLE LCM.Chest (
	ID_Item_Type INT PRIMARY KEY,
	FOREIGN KEY (ID_Item_Type) REFERENCES LCM.Item_Type(ID),  
);

--Tabela Ward
CREATE TABLE LCM.Ward (
	ID_Item_Type INT PRIMARY KEY,
	Name VARCHAR(8),
	FOREIGN KEY (ID_Item_Type) REFERENCES LCM.Item_Type(ID),  
);

--Tabela User_Select--
CREATE TABLE LCM.User_Select (
    ID INT PRIMARY KEY,
    ID_User INT,
    ID_Skin_User INT,
    ID_Champion INT,
    ID_Ward INT,
    FOREIGN KEY (ID_User) REFERENCES LCM.[User](ID),
    FOREIGN KEY (ID_Skin_User) REFERENCES LCM.Skin(Skin_ID),
    FOREIGN KEY (ID_Champion) REFERENCES LCM.Champion(ID_Item_Type),
    FOREIGN KEY (ID_Ward) REFERENCES LCM.Ward(ID_Item_Type)
);

--Tabela Map
CREATE TABLE LCM.Map (
    ID INT PRIMARY KEY,
    Name VARCHAR(50)
);

--Tabela Game
CREATE TABLE LCM.Game (
    ID INT PRIMARY KEY,
    Duration TIME,
    Outcome INT,
    ID_Map INT,
    ID_User_Select INT,
    Data DATE,
    Hora TIME,
    FOREIGN KEY (ID_Map) REFERENCES LCM.Map(ID),
    FOREIGN KEY (ID_User_Select) REFERENCES LCM.User_Select(ID)
);










