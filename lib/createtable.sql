CREATE TABLE USER(
    UserId varchar(35) primary key,
    UserName varchar(20) NOT NULL,
    Uaddress varchar(100) NOT NULL,
    CollectionSum int default 0
)

CREATE TABLE Items(
    ItemId int primary key,
    ItemName varchar(20) NOT NULL,
    ImageUrl varchar(200) NOT NULL
)

//INSERT INTO Items VALUES (ItemId,ItemName,ImageUrl);