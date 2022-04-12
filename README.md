# Project of CFGS ASIR
MyHomeCloud is a cloud storage that works in local mode.

## **Index**
1. [Snapshots](#snapshots)
2. [How To Run](#howtorun)
	1. [Windows](#windows)
	2. [Linux](#linux)
## Snapshots <a name="snapshots"></a>
### Login/Register Page
![Login](docs/login-demo.png)

### Main Page
![Unit Page](docs/demo-1.png)

# How to Run <a name="howtorun"></a>
Install the requirements. You can use the following command:
```
python -m pip install -r requirement.txt
```
### Windows <a name="windows"></a>
MySQL Installer: https://dev.mysql.com/downloads/installer/

    - Select MySQL Server and Workbench in the installation

After the installation, connect to you MySQL and run this following SQL script:
```
CREATE DATABASE IF NOT EXISTS `applogin` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
```
```
USE `applogin`;
DROP TABLE IF EXISTS accounts;
CREATE TABLE IF NOT EXISTS `accounts` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    	`level` varchar(20) NOT NULL DEFAULT('user'),
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    `folder_name` varchar(1000) NOT NULL,
    CONSTRAINT UserID_folder PRIMARY KEY (`id`, `folder_name`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
```
Create a config.env file, copy the following lines into it and **edit them**:
```
export SECRET_KEY="YOUR SECRET KEY"
export MYSQL_USER="MYSQL USERNAME"
export MYSQL_PASSWORD="MYSQL PASSWORD"
export MYSQL_HOST="MYSQL HOST"
export MYSQL_DB="MYSQL DATABASE NAME"
export BASE_DIR="PATH WHERE YOU WANT TO STORAGE"
```
Now we need to generate some certificate for the website. I'm using this [repository](https://github.com/FiloSottile/mkcert) to generate the certificate more easily.

Follow the installation on they repository and run the following sentences:
```
mkcert -key-file key.pem -cert-file cert.pem myhomecloud.com *.myhomecloud.com
```

### Linux <a name="linux"></a>
**Ubuntu/Debian/PopOS/...**
```
$ sudo apt-get install mysql-server
```
Configure your MySQL Server and run this following SQL script:
```
CREATE DATABASE IF NOT EXISTS `applogin` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
```
```
USE `applogin`;
DROP TABLE IF EXISTS accounts;
CREATE TABLE IF NOT EXISTS `accounts` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    	`level` varchar(20) NOT NULL DEFAULT('user'),
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    `folder_name` varchar(1000) NOT NULL,
    CONSTRAINT UserID_folder PRIMARY KEY (`id`, `folder_name`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
```
Create a config.env file:
```
$ cd myhomecloud && touch config.env
```
copy the following lines into it and **edit them**:
```
export SECRET_KEY="YOUR SECRET KEY"
export MYSQL_USER="MYSQL USERNAME"
export MYSQL_PASSWORD="MYSQL PASSWORD"
export MYSQL_HOST="MYSQL HOST"
export MYSQL_DB="MYSQL DATABASE NAME"
export BASE_DIR="PATH WHERE YOU WANT TO STORAGE"
```
Now we need to generate some certificate for the website. I'm using this [repository](https://github.com/FiloSottile/mkcert) to generate the certificate more easily.

Follow the installation on they repository and run the following sentences:
```
mkcert -key-file key.pem -cert-file cert.pem myhomecloud.com *.myhomecloud.com
```
