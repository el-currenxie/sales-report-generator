PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE reference_rate (currency text, rate numeric, date text);
INSERT INTO reference_rate VALUES('GBP',8.5399999999999991473,'2019-07-17');
INSERT INTO reference_rate VALUES('USD',6.8799999999999998934,'2019-07-17');
INSERT INTO reference_rate VALUES('EUR',7.7199999999999997513,'2019-07-17');
INSERT INTO reference_rate VALUES('JPY',0.064000000000000001332,'2019-07-17');
CREATE TABLE imported_files (file_name text, date text);
CREATE TABLE IF NOT EXISTS "sales" (
	id INTEGER NOT NULL PRIMARY KEY,
	client text,
	amazon_order_id text NOT NULL,
	product_name text,
	quantity numeric,
	unit_price numeric,
	purchase_date text,
	logistics text,
	logistics_number text,
	receiver text,
	receiver_address text,
	assignment text
, original_currency text, original_unit_price numeric, sales_channel text, payeco_assignment);
COMMIT;
