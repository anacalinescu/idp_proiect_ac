use idp_banking;
delimiter //

CREATE TABLE IF NOT EXISTS users (username VARCHAR(255) PRIMARY KEY, password VARCHAR(255), accountno INT);
CREATE TABLE IF NOT EXISTS personal_information (username VARCHAR(255) PRIMARY KEY, lastname VARCHAR(255), firstname VARCHAR(255), address VARCHAR(255), mobileno INT, email VARCHAR(255));
CREATE TABLE IF NOT EXISTS cards (iban VARCHAR(255) PRIMARY KEY, pin INT, accountno INT, money INT);
CREATE TABLE IF NOT EXISTS transactions (sourceiban VARCHAR(255), destinationiban VARCHAR(255), comments VARCHAR(255), money INT, transactiondate date);
CREATE TABLE IF NOT EXISTS coin (iban VARCHAR(255) PRIMARY KEY, coint varchar(255));

DROP FUNCTION IF EXISTS `findUser`//
CREATE FUNCTION `findUser`(usernameI varchar(255), passwordI varchar(255)) RETURNS int(11)
    READS SQL DATA
BEGIN
	DECLARE result int(11);
	SELECT count(*) into result from users WHERE username=usernameI and password=passwordI;
	RETURN result;
END//

DROP FUNCTION IF EXISTS `correctTransfer`//
CREATE FUNCTION `correctTransfer`(ibanI varchar(255), accountnoI int, pinI int) RETURNS int(11)
    READS SQL DATA
BEGIN
	DECLARE result int(11);
	SELECT count(*) into result from cards WHERE iban=ibanI and accountno=accountnoI and pin=pinI;
	RETURN result;
END//

DROP FUNCTION IF EXISTS `enoughMoney`//
CREATE FUNCTION `enoughMoney`(ibanI varchar(255), accountnoI int, pinI int, moneyI int) RETURNS int(11)
    READS SQL DATA
BEGIN
	DECLARE result int(11);
	DECLARE currMoney int(11);
	SELECT money into currMoney from cards WHERE iban=ibanI and accountno=accountnoI and pin=pinI;
	IF currMoney > moneyI THEN
		SET result = 1;
	ELSE SET result = 0;
	END IF;
	RETURN result;
END//

DROP FUNCTION IF EXISTS `correctUsername`//
CREATE FUNCTION `correctUsername`(usernameI varchar(255)) RETURNS int(11)
    READS SQL DATA
BEGIN
	DECLARE result int(11);
	SELECT count(*) into result from users WHERE username=usernameI;
	RETURN result;
END//

DROP FUNCTION IF EXISTS `correctIban`//
CREATE FUNCTION `correctIban`(ibanI varchar(255), accountnoI int) RETURNS int(11)
    READS SQL DATA
BEGIN
	DECLARE result int(11);
	SELECT count(*) into result from cards WHERE iban=ibanI and accountno=accountnoI;
	RETURN result;
END//

DROP FUNCTION IF EXISTS `getAccountNo`//
CREATE FUNCTION `getAccountNo`(usernameI varchar(255), passwordI varchar(255)) RETURNS int(11)
    READS SQL DATA
BEGIN
	DECLARE result int(11);
	SELECT accountno into result from users WHERE username=usernameI and password=passwordI;
	RETURN result;
END//

DROP TRIGGER IF EXISTS `updateSum`//
CREATE TRIGGER `updateSum` BEFORE INSERT ON transactions FOR EACH ROW
BEGIN
	UPDATE cards set money=money-NEW.money WHERE iban=NEW.sourceiban;
	UPDATE cards set money=money+NEW.money WHERE iban=NEW.destinationiban;
END//
delimiter ;

