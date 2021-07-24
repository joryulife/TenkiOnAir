DROP TABLE USER;
DROP TABLE Items;

CREATE TABLE USER(
    UserId varchar(35) primary key,
    Uaddress varchar(8) NOT NULL default "ddd-dddd",
    CollectionSum int default 0,
    ScheduledTime datetime,
    remindTime datetime,
    flag varchar(20) NOT NULL
);



CREATE TABLE Items(
    ItemId int primary key,
    ItemName varchar(20) NOT NULL,
    ImageUrl varchar(200) NOT NULL
);

INSERT INTO Items
VALUES (2,'dandelions', 'https://drive.google.com/uc?id=1W5wHMTK7R5PelrLmk01BCHf3OLe68_NE'),
(4, 'cherry_blossoms', 'https://drive.google.com/uc?id=1_rVcXp7Hj4pqrTou-Icu9vq3jdXCrHKn'),
(8, 'hydrangea', 'https://drive.google.com/uc?id=1GUjbvzr-00ggBBVjG__7xbOj_e3F7m0X'),
(16, 'sunflower', 'https://drive.google.com/uc?id=1NTx4rzNkXzu13icYbWM3jRVUPLbZy4Rn'),
(32, 'cosmos', 'https://drive.google.com/uc?id=1xPh5zcbv19Wc-Fl2nAujAqPgIGfs2_k4'),
(64, 'dianthus', 'https://drive.google.com/uc?id=1d5w_SQlAuglaZ2PqzU-qng5XEDgHutI9'),
(128, 'cyclamen', 'https://drive.google.com/uc?id=1UCYF3iKBi-owJnUN3y7GkJswlDtlAXHz'),
(256, 'christmas_rose', 'https://drive.google.com/uc?id=12g3PSQlmGCNI6br10OxllLOG1Eea9Z7K'),
(512, 'withered_flower', 'https://drive.google.com/uc?id=1qLkgxd22O_Hs7RkQq9lLwhRvmTLsc-Bm'),
(1024, 'seedling', 'https://drive.google.com/uc?id=12TzjT4panj-GK91TX-2swngJ8EVCag9y'),
(2048, 'watering', 'https://drive.google.com/uc?id=1-Ndn_zdMwmav5XYS4XNzZzxKF4BQxY2J');
