-- ./init-db/init-db.sql
CREATE USER IF NOT EXISTS 'projeto_forum'@'%' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON *.* TO 'projeto_forum'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
