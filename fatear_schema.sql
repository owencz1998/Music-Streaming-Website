DROP TABLE IF EXISTS user;
CREATE TABLE `user` (
  `username` varchar(10) NOT NULL,
  `pwd` varchar(40) DEFAULT NULL,
  `fname` varchar(20) NOT NULL,
  `lname` varchar(20) NOT NULL,
  `lastlogin` date DEFAULT NULL,
  `nickname` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`username`)
);



DROP TABLE IF EXISTS artist;
CREATE TABLE `artist` (
  `artistID` varchar(5) NOT NULL,
  `fname` varchar(20) NOT NULL,
  `lname` varchar(20) NOT NULL,
  `artistBio` varchar(100) DEFAULT NULL,
  `artistURL` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`artistID`)
);


DROP TABLE IF EXISTS song;
CREATE TABLE `song` (
  `songID` varchar(5) NOT NULL,
  `title` varchar(20) NOT NULL,
  `releaseDate` date DEFAULT NULL,
  `songURL` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`songID`)
);


DROP TABLE IF EXISTS artistperformssong;
CREATE TABLE `artistperformssong` (
  `artistID` varchar(5) NOT NULL,
  `songID` varchar(5) NOT NULL,
  PRIMARY KEY (`artistID`,`songID`),
  KEY `songID` (`songID`),
  CONSTRAINT `artistperformssong_ibfk_1` FOREIGN KEY (`artistID`) REFERENCES `artist` (`artistID`) ON DELETE CASCADE,
  CONSTRAINT `artistperformssong_ibfk_2` FOREIGN KEY (`songID`) REFERENCES `song` (`songID`) ON DELETE CASCADE
);


DROP TABLE IF EXISTS album;
CREATE TABLE `album` (
  `albumID` varchar(5) NOT NULL,
  `albumName` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`albumID`)
);


DROP TABLE IF EXISTS songinalbum;
CREATE TABLE `songinalbum` (
  `albumID` varchar(5) NOT NULL,
  `songID` varchar(5) NOT NULL,
  PRIMARY KEY (`albumID`,`songID`),
  KEY `songID` (`songID`),
  CONSTRAINT `songinalbum_ibfk_1` FOREIGN KEY (`albumID`) REFERENCES `album` (`albumID`) ON DELETE CASCADE,
  CONSTRAINT `songinalbum_ibfk_2` FOREIGN KEY (`songID`) REFERENCES `song` (`songID`) ON DELETE CASCADE
);


DROP TABLE IF EXISTS songgenre;
CREATE TABLE `songgenre` (
  `songID` varchar(5) NOT NULL,
  `genre` varchar(10) NOT NULL,
  PRIMARY KEY (`songID`,`genre`),
  CONSTRAINT `songgenre_ibfk_1` FOREIGN KEY (`songID`) REFERENCES `song` (`songID`) ON DELETE CASCADE
);


DROP TABLE IF EXISTS userfanofartist;
CREATE TABLE `userfanofartist` (
  `username` varchar(10) NOT NULL,
  `artistID` varchar(5) NOT NULL,
  PRIMARY KEY (`username`,`artistID`),
  KEY `artistID` (`artistID`),
  CONSTRAINT `userfanofartist_ibfk_1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE CASCADE,
  CONSTRAINT `userfanofartist_ibfk_2` FOREIGN KEY (`artistID`) REFERENCES `artist` (`artistID`) ON DELETE CASCADE
);


DROP TABLE IF EXISTS ratealbum;
CREATE TABLE `ratealbum` (
  `username` varchar(10) NOT NULL,
  `albumID` varchar(5) NOT NULL,
  `stars` int DEFAULT NULL,
  PRIMARY KEY (`username`,`albumID`),
  KEY `albumID` (`albumID`),
  CONSTRAINT `ratealbum_ibfk_1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE CASCADE,
  CONSTRAINT `ratealbum_ibfk_2` FOREIGN KEY (`albumID`) REFERENCES `album` (`albumID`) ON DELETE CASCADE,
  CONSTRAINT `ratealbum_chk_1` CHECK ((`stars` in (1,2,3,4,5)))
);


DROP TABLE IF EXISTS ratesong;
CREATE TABLE `ratesong` (
  `username` varchar(10) NOT NULL,
  `songID` varchar(5) NOT NULL,
  `stars` int DEFAULT NULL,
  `ratingDate` date DEFAULT NULL,
  PRIMARY KEY (`username`,`songID`),
  KEY `songID` (`songID`),
  CONSTRAINT `ratesong_ibfk_1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE CASCADE,
  CONSTRAINT `ratesong_ibfk_2` FOREIGN KEY (`songID`) REFERENCES `song` (`songID`) ON DELETE CASCADE,
  CONSTRAINT `ratesong_chk_1` CHECK ((`stars` in (1,2,3,4,5)))
);


DROP TABLE IF EXISTS reviewalbum;
CREATE TABLE `reviewalbum` (
  `username` varchar(10) NOT NULL,
  `albumID` varchar(5) NOT NULL,
  `reviewText` varchar(100) DEFAULT NULL,
  `reviewDate` date DEFAULT NULL,
  PRIMARY KEY (`username`,`albumID`),
  KEY `albumID` (`albumID`),
  CONSTRAINT `reviewalbum_ibfk_1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE CASCADE,
  CONSTRAINT `reviewalbum_ibfk_2` FOREIGN KEY (`albumID`) REFERENCES `album` (`albumID`) ON DELETE CASCADE
);


DROP TABLE IF EXISTS reviewsong;
CREATE TABLE `reviewsong` (
  `username` varchar(10) NOT NULL,
  `songID` varchar(5) NOT NULL,
  `reviewText` varchar(100) DEFAULT NULL,
  `reviewDate` date DEFAULT NULL,
  PRIMARY KEY (`username`,`songID`),
  KEY `songID` (`songID`),
  CONSTRAINT `reviewsong_ibfk_1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE CASCADE,
  CONSTRAINT `reviewsong_ibfk_2` FOREIGN KEY (`songID`) REFERENCES `song` (`songID`) ON DELETE CASCADE
);


DROP TABLE IF EXISTS follows;
CREATE TABLE `follows` (
  `follower` varchar(10) NOT NULL,
  `follows` varchar(10) NOT NULL,
  `createdAt` datetime DEFAULT NULL,
  PRIMARY KEY (`follower`,`follows`),
  KEY `follows` (`follows`),
  CONSTRAINT `follows_ibfk_1` FOREIGN KEY (`follower`) REFERENCES `user` (`username`) ON DELETE CASCADE,
  CONSTRAINT `follows_ibfk_2` FOREIGN KEY (`follows`) REFERENCES `user` (`username`) ON DELETE CASCADE
);


DROP TABLE IF EXISTS friend;
CREATE TABLE `friend` (
  `user1` varchar(10) NOT NULL,
  `user2` varchar(10) NOT NULL,
  `acceptStatus` varchar(12) DEFAULT NULL,
  `requestSentBy` varchar(10) DEFAULT NULL,
  `createdAt` datetime DEFAULT NULL,
  `updatedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`user1`,`user2`),
  KEY `user2` (`user2`),
  CONSTRAINT `friend_ibfk_1` FOREIGN KEY (`user1`) REFERENCES `user` (`username`) ON DELETE CASCADE,
  CONSTRAINT `friend_ibfk_2` FOREIGN KEY (`user2`) REFERENCES `user` (`username`) ON DELETE CASCADE,
  CONSTRAINT `friend_chk_1` CHECK ((`acceptStatus` in (_utf8mb4'Accepted',_utf8mb4'Not accepted',_utf8mb4'Pending')))
);