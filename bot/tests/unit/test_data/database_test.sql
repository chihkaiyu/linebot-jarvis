CREATE TABLE USER (
userID VARCHAR(64) NOT NULL,
favorite VARCHAR(64),
lastCmd VARCHAR(64),
PRIMARY KEY (userID)    
);

INSERT INTO USER
(userID, favorite, lastCmd)
VALUES
('test', 'lion', 'I love lion');