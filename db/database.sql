use idp_banking;
delimiter //

CREATE TABLE IF NOT EXISTS users (username VARCHAR(255) PRIMARY KEY, password VARCHAR(255), accountno INT);
CREATE TABLE IF NOT EXISTS personal_information (username VARCHAR(255) PRIMARY KEY, lastname VARCHAR(255), firstname VARCHAR(255), address VARCHAR(255), mobileno INT, email VARCHAR(255));
CREATE TABLE IF NOT EXISTS cards (iban VARCHAR(255) PRIMARY KEY, pin INT, accountno INT, money INT);
CREATE TABLE IF NOT EXISTS transactions (sourceiban VARCHAR(255), destinationiban VARCHAR(255), comments VARCHAR(255), money INT, transactiondate date);
CREATE TABLE IF NOT EXISTS coin (iban VARCHAR(255) PRIMARY KEY, coin varchar(255));

DROP PROCEDURE IF EXISTS insertPersonalData;
CREATE PROCEDURE insertPersonalData(IN username varchar(255), IN lastname varchar(255), IN firstname varchar(255), IN address varchar(255), IN mobileno int, IN email varchar(255))
	BEGIN
		INSERT INTO personal_information VALUES(username, lastname, firstname, address, mobileno, email);
	END//

DROP PROCEDURE IF EXISTS insertUser;
CREATE PROCEDURE insertUser(IN username varchar(255), IN password varchar(255), IN accountno int)
	BEGIN
		INSERT INTO users VALUES(username, password, accountno);
	END//

DROP PROCEDURE IF EXISTS insertCard;
CREATE PROCEDURE insertCard(IN iban varchar(255), IN pin int, IN accountno int, IN coin varchar(255))
	BEGIN
		INSERT INTO cards VALUES(iban, pin, accountno, 0);
		INSERT INTO coin VALUES(iban, coin);
	END//

DROP PROCEDURE IF EXISTS addMoney;
CREATE PROCEDURE addMoney(IN ibanI varchar(255), IN accountnoI int, IN moneyI int)
	BEGIN
		UPDATE cards set money=money + moneyI WHERE iban=ibanI and accountno=accountnoI;
	END//

DROP PROCEDURE IF EXISTS insertTransaction;
CREATE PROCEDURE insertTransaction(IN ibansrc varchar(255), IN ibandst varchar(255), IN comm varchar(255), IN money int, IN currentdate date)
	BEGIN
		INSERT INTO transactions VALUES(ibansrc, ibandst, comm, money, currentdate);
	END//

DROP PROCEDURE IF EXISTS changePin;
CREATE PROCEDURE changePin(IN ibanI varchar(255), IN oldpin int, IN newpin int)
	BEGIN
		UPDATE cards set pin=newpin WHERE iban=ibanI and pin=oldpin;
	END//

DROP PROCEDURE IF EXISTS displayTransactions;
CREATE PROCEDURE displayTransactions(IN ibanI varchar(255))
	BEGIN
		SELECT * from transactions WHERE sourceiban=ibanI;	
	END//

DROP PROCEDURE IF EXISTS displayCards;
CREATE PROCEDURE displayCards(IN accountnoI int)
	BEGIN
		SELECT c1.iban, c1.pin, c1.money, c2.coin from cards c1 JOIN coin c2 ON c1.iban=c2.iban WHERE c1.accountno=accountnoI;	
	END//

delimiter ;

