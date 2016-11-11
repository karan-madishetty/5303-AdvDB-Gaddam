###Shravani Gaddam   
###67.205.143.163   
####http://67.205.143.163/phpmyadmin   
### gift_options.sql

```sql
CREATE TABLE IF NOT EXISTS gift_options(
	itemId INT( 10 ) NOT NULL ,
	allowGiftWrap BOOLEAN NOT NULL ,
	allowGiftMessage BOOLEAN NOT NULL ,
	allowGiftReceipt BOOLEAN NOT NULL ,
	PRIMARY KEY ( itemId ) ,
	FOREIGN KEY ( itemId ) REFERENCES products( itemId )
) ENGINE = INNODB DEFAULT CHARSET = latin1;
```

### image_entities.sql

```sql
CREATE TABLE IF NOT EXISTS image_entities (
	itemId INT(10) NOT NULL ,
        thumbnailImage tinyblob NOT NULL,
        mediumImage mediumblob NOT NULL,
        largeImage longblob NOT NULL,
        entityType varchar(9) NOT NULL,
    	PRIMARY KEY (itemId) ,
	FOREIGN KEY (itemId) REFERENCES products(itemId)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

### market_place_price.sql

```sql
CREATE TABLE IF NOT EXISTS market_place_price(
	itemId INT(10) NOT NULL ,
	price DOUBLE NOT NULL ,
	sellerInfo VARCHAR(44) NOT NULL ,
	standardShipRate DOUBLE NOT NULL ,
	twoThreeDayShippingRate DOUBLE NOT NULL ,
	availableOnline BOOLEAN NOT NULL ,
	clearance BOOLEAN NOT NULL ,
	offerType VARCHAR(16) NOT NULL ,
	PRIMARY KEY (itemId) ,
	FOREIGN KEY (itemId) REFERENCES products(itemId)
) ENGINE = INNODB DEFAULT CHARSET = latin1;
```	


### products.sql

```sql

CREATE TABLE IF NOT EXISTS products (
	itemId int(10) NOT NULL,
	parentItemId int(10) NOT NULL,
	name varchar(200) NOT NULL,
	salePrice float(6,2) NOT NULL,
	upc bigint(12) NOT NULL,
	categoryPath varchar(123) NOT NULL,
	shortDescription mediumtext NOT NULL,
	longDescription longtext NOT NULL,
	brandName varchar(36) NOT NULL,
	thumbnailImage blob NOT NULL,
	mediumImage mediumblob NOT NULL,
	largeImage longbolb NOT NULL,
	productTrackingUrl varchar(416) NOT NULL,
	modelNumber varchar(53) NOT NULL,
	productUrl varchar(345) NOT NULL,
	categoryNode varchar(23) NOT NULL,
	stock varchar(13) NOT NULL,
	addToCartUrl varchar(221) NOT NULL,
	affiliateAddToCartUrl varchar(296) NOT NULL,
	offerType varchar(16) NOT NULL,
	msrp double NOT NULL,
	standardShipRate double NOT NULL,
	color varchar(10) NOT NULL,
	customerRating varchar(5) NOT NULL,
	numRevieus int(5) NOT NULL,
	customerRatingImage blob NOT NULL,
	maxItemsInOrder int(6) NOT NULL,
	size varchar(49) NOT NULL,
	sellerInfo varchar(44) NOT NULL,
	age int(14) NOT NULL,
	gender varchar(6) NOT NULL,
	isbn bigint(13) NOT NULL,
	preOrderShipsOn varchar(19) NOT NULL,
	primary key(itemId,parentItemId)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```
