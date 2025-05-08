CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	PRIMARY KEY (version_num)
);
INSERT INTO "alembic_version" VALUES('dd0bf3dbf300');

CREATE TABLE users (
	id INTEGER NOT NULL, 
	username VARCHAR(60), 
	email VARCHAR(100), 
	phone VARCHAR(10), 
	password VARCHAR(10000) NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO "users" VALUES(1,'biasedai','bias@abc.com','9899878454','');
INSERT INTO "users" VALUES(2,'yugaljain1999','yj@abc.com',NULL,'');
INSERT INTO "users" VALUES(3,'yj03','yj@outlook.com','987874454','');
INSERT INTO "users" VALUES(4,'jain03','yj@yjsports.com','8548752237','$2b$12$7d5gnRwljdzrV1X8UyYxYuTOLxNnHn0aZpKjZwaLjg9iZ7s3fxgti');
INSERT INTO "users" VALUES(7,'jain103','yj@yjsports3.com','8548752237','$2b$12$o6wXk8TeiT.fCpXh7o79m.xTaaxY.ikezLUtR6DpBddIE5XmDc3uO');
INSERT INTO "users" VALUES(9,'biasedai03','bias@abcd.com','9478964657','$2b$12$OQdKlnEbkYQatcrv9tyEruIRk2b4nMXMCDa7jq3EQQXIhDkGkShBC');

CREATE SEQUENCE users_id_seq;
ALTER TABLE users ALTER COLUMN id SET DEFAULT nextval('users_id_seq');
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
ALTER TABLE users ADD PRIMARY KEY (id);

CREATE TABLE blogs (
	id SERIAL PRIMARY KEY, 
	title VARCHAR(60), 
	body VARCHAR(200), 
	author VARCHAR(30), 
	user_id INTEGER, 
	CONSTRAINT blogs_ibfk_1 FOREIGN KEY(user_id) REFERENCES users (id)
);
INSERT INTO "blogs" VALUES(3,'Togetherness','We are family','deepti',2);
INSERT INTO "blogs" VALUES(4,'zero to one','startup stories','peter thiel',NULL);
INSERT INTO "blogs" VALUES(5,'better than best friends','not going well','marsh',3);

CREATE UNIQUE INDEX email ON users (email);
CREATE UNIQUE INDEX username ON users (username);
CREATE INDEX ix_users_id ON users (id);
CREATE INDEX ix_blogs_id ON blogs (id);
CREATE INDEX user_id ON blogs (user_id);
