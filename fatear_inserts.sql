INSERT INTO user VALUES ('jacksmith','2a3df22f79112966080cccac1406622d','Jack','Smith','2023-05-01','jack'),('janesmith','1358117abb6eade69e82b7360017117d','Jane','Smith','2023-05-05','jane'),('jillsmith','4d215602009218b17167fe453ab6c542','Jill','Smith','2023-03-17','jill'),('johnsmith','19d3e4f8f8e8f54325acbb86ca6c14e9','John','Smith','2022-10-01','john');


INSERT INTO artist VALUES ('a1','First','One','Singer One','https://www.singerone.com/'),('a2','Second','Two','Singer Two','https://www.singertwo.com/'),('a3','Third','Three','Singer Three','https://www.singerthree.com/'),('a4','Fourth','Four','Singer Four','https://www.singerfour.com/');


INSERT INTO song VALUES ('s1','Song 1','2023-05-01','/song1/'),('s2','Song 2','2023-01-02','/song2/'),('s3','Song 3','2022-05-03','/song3/'),('s4','Song 4','2023-01-04','/song4/');


INSERT INTO artistperformssong VALUES ('a1','s1'),('a2','s2'),('a3','s3'),('a4','s4');


INSERT INTO album VALUES ('b1','Album 1'),('b2','Album 2'),('b3','Album 3'),('b4','Album 4');


INSERT INTO songinalbum VALUES ('b1','s1'),('b2','s2'),('b3','s3'),('b4','s4');


INSERT INTO songgenre VALUES ('s1','Jazz'),('s2','Jazz'),('s3','Pop'),('s4','Rock');


INSERT INTO userfanofartist VALUES ('jacksmith','a1'),('johnsmith','a1'),('jacksmith','a2'),('johnsmith','a2'),('johnsmith','a3');


INSERT INTO ratealbum VALUES ('jacksmith','b1',4),('jacksmith','b2',3),('jacksmith','b3',2),('jacksmith','b4',1),('johnsmith','b1',5),('johnsmith','b2',4),('johnsmith','b3',3),('johnsmith','b4',2);


INSERT INTO ratesong VALUES ('jacksmith','s1',4,'2023-01-13'),('jacksmith','s2',3,'2023-01-14'),('jacksmith','s3',2,'2023-01-15'),('jacksmith','s4',1,'2023-01-16'),('johnsmith','s1',4,'2023-05-04'),('johnsmith','s2',4,'2023-05-04'),('johnsmith','s3',3,'2023-01-11'),('johnsmith','s4',2,'2023-01-12');


INSERT INTO reviewalbum VALUES ('jacksmith','b1','Good','2023-01-05'),('jacksmith','b2','Good','2023-01-06'),('jacksmith','b3','Good','2023-01-07'),('jacksmith','b4','Good','2023-01-08'),('johnsmith','b1','Great','2023-01-01'),('johnsmith','b2','Great','2023-01-02'),('johnsmith','b3','Great','2023-01-03'),('johnsmith','b4','Great','2023-01-04');


INSERT INTO reviewsong VALUES ('jacksmith','s1','Good song 1','2023-01-21'),('jacksmith','s2','Good song 2','2023-01-22'),('jacksmith','s3','Good song 3','2023-01-23'),('jacksmith','s4','Good song 4','2023-01-24'),('janesmith','s1','Nice song 1','2023-04-01'),('jillsmith','s2','Great song 2','2023-04-01'),('johnsmith','s1','Review of song 1','2023-05-03'),('johnsmith','s2','Review of song 2','2023-05-04'),('johnsmith','s3','Review of song 3','2023-05-03'),('johnsmith','s4','Review of song 4','2023-01-20');


INSERT INTO follows VALUES ('jacksmith','jillsmith','2021-01-11 09:09:09'),('jacksmith','johnsmith','2021-01-10 08:08:08'),('janesmith','jillsmith','2021-01-12 10:10:10'),('johnsmith','jacksmith','2021-01-08 06:06:06'),('johnsmith','janesmith','2021-01-09 07:07:07');


INSERT INTO friend VALUES ('jacksmith','janesmith','Accepted','jacksmith','2021-01-04 03:03:03','2021-01-05 03:03:03'),('janesmith','jillsmith','Accepted','jillsmith','2021-01-06 05:05:05','2021-01-07 05:05:05'),('johnsmith','jacksmith','Accepted','johnsmith','2021-01-01 00:00:00','2021-01-02 00:00:00'),('johnsmith','jillsmith','Pending','jillsmith','2021-01-02 01:01:01',NULL);