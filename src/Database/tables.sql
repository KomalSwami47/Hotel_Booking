--
-- Database : `Hotel`
--

--------------------------------

--Table structure for database--
--------------------------------

--creating table to store information of the new user in the table called `Bookingdata`--

create table Bookingdata(
name varchar(255),
mobilenum varchar(255),
email varchar(255),
password varchar(255),
adharid varchar(255),
checkin varchar(255),
checkout varchar(255),
adult int(11),
child int(11),
days int(11),
roomnum int(11)
);

------------------------------------------------------------------------------------------

--creating table to store feedback from the user in the table called `Feedback`--

create table Feedback(
name varchar(255),
mobilenum varchar(255),
email varchar(255),
message varchar(255)
);

------------------------------------------------------------------------------------------