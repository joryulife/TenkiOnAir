CREATE TABLE USER(
    UserId varchar(35) primary key,
    UserName varchar(20) NOT NULL,
    Uaddress varchar(8) NOT NULL,
    CollectionSum int default 0
)

CREATE TABLE Items(
    ItemId int primary key,
    ItemName varchar(20) NOT NULL,
    ImageUrl varchar(200) NOT NULL
)

INSERT INTO Items
VALUES (1,'dandelions', 'https://drive.google.com/uc?id=1W5wHMTK7R5PelrLmk01BCHf3OLe68_NE'),
(2, 'cherry_blossoms', 'https://drive.google.com/uc?id=1_rVcXp7Hj4pqrTou-Icu9vq3jdXCrHKn'),
(3, 'hydrangea', 'https://drive.google.com/uc?id=1GUjbvzr-00ggBBVjG__7xbOj_e3F7m0X'),
(4, 'sunflower', 'https://drive.google.com/uc?id=1NTx4rzNkXzu13icYbWM3jRVUPLbZy4Rn'),
(5, 'cosmos', 'https://drive.google.com/uc?id=1xPh5zcbv19Wc-Fl2nAujAqPgIGfs2_k4'),
(6, 'dianthus', 'https://drive.google.com/uc?id=1d5w_SQlAuglaZ2PqzU-qng5XEDgHutI9'),
(7, 'cyclamen', 'https://drive.google.com/uc?id=1UCYF3iKBi-owJnUN3y7GkJswlDtlAXHz'),
(8, 'christmas_rose', 'https://drive.google.com/uc?id=12g3PSQlmGCNI6br10OxllLOG1Eea9Z7K');
