USE swiftrail;

INSERT INTO users VALUES
(1, 'ashish@gmail.com', 'ashish', AES_ENCRYPT('Ashish123', 'secret'), 'Ashish', 'Kumar', 'm', '2000-01-01', 'India', '6205144592', 'C.V. Raman Hostel'),
(2, 'sachin@gmail.com', 'sachin', AES_ENCRYPT('Sachin123', 'secret'), 'Sachin', 'Srivastava', 'm', '2000-01-01', 'India', '7985518670', 'C.V. Raman Hostel'),
(3, 'manav@gmail.com', 'manav', AES_ENCRYPT('Manav123', 'secret'), 'Manav', 'Jain', 'm', '2000-01-01', 'India', '8080007703', 'C.V. Raman Hostel');

insert into station values 
('KIK','KARAIKAL'),
('NCR','NAGORE'),
('NGT','NAGAPPATTINAM'),
('TVR','THIRUVARUR JN'),
('PEM','PERALAM JN'),
('MV','MAYILADUTURAJ JN'),
('SY','SIRKAZHI'),
('CDM','CHIDAMBRAM'),
('CUPJ','CUDDALORE PORT'),
('TDPR','TIRUPADRIPULYUR'),
('VM','VILLUPURAM JN'),
('TMV','TINDIVANAM'),
('MLMR','MELMARUVATTUR'),
('CGL','CHENGALPATTU'),
('TBM','TAMBARAM'),
('MS','CHEENAI EGMORE'),
('DBG','DARBHANGA JN'),
('SPJ','SAMASTIPUR JN'),
('MFP','MUZZAFARPUR JN'),
('HJP','HAJIPUR JN'),
('SEE','SONPUR JN'),
('CPR','CHHAPRA'),
('SV','SIWAN JN'),
('GKP','GORAKHPUR JN'),
('LKO','LUCKNOW NR'),
('CNB','KANPUR CENTRAL'),
('NDLS','NEW DELHI'),
('CSTM','MUMBAI CST'),
('DR','DADAR'),
('TNA','THANE'),
('PNVL','PANVEL'),
('MNI','MANGAON'),
('KHED','KHED'),
('CHI','CHIPLUN'),
('SGR','SANGMESHWAR'),
('RN','RATNAGIRI'),
('ADVI','ADAVALI'),
('RAJP','RAJAPUR ROAD'),
('VBW','VAIBHAVWADI RD'),
('KKW','KANKAVALI'),
('SNDD','SINDHUDURG'),
('KUDL','KUDAL'),
('SWV','SWANTWADI ROAD'),
('PERN','PERNEM'),
('THVM','THIVIM'),
('KRMI','KARMALI'),
('MAO','MADGAON'),
('BJU','BARAUNI JN'),
('DSS','DALSINGH SARAI'),
('DEOS','DEORIA SADAR'),
('KLD','KHALILABAD'),
('BST','BASTI'),
('GD','GONDA JN'),
('BBK','BARABANKI JN'),
('ETW','ETAWAH'),
('TDL','TUNDLA JN'),
('ALJN','ALIGARH JN'),
('GZB','GHAZIABAD');

insert into train values
('10103','MANDOVI EXP'),
('12553','VAISHALI EXP'),
('12565','BIHAR S KRANTI'),
('16176','CHENNAI EXP');

insert into train_details values
('10103','CSTM','MAO','SUN MON TUE WED THU FRI SAT','1A 2A 3A SL 2S'),
('12553','BJU','NDLS','SUN MON TUE WED THU FRI SAT','1A 2A 3A SL 2S'),
('12565','DBG','NDLS','SUN MON TUE WED THU FRI SAT','1A 2A 3A SL 2S'),
('16176','KIK','MS','SUN MON TUE WED THU FRI SAT','1A 2A 3A SL 2S');

insert into schedule(train_no, station_code, arrival, departure, day, distance) values
('16176','KIK','21:00','21:00',1,0),
('16176','NCR','21:08','21:10',1,11),
('16176','NGT','21:25','21:35',1,19),
('16176','TVR','22:15','22:25',1,42),
('16176','PEM','22:50','22:51',1,65),
('16176','MV','23:18','23:20',1,81),
('16176','SY','23:46','23:47',1,101),
('16176','CDM','00:05','00:06',2,117),
('16176','CUPJ','00:41','00:42',2,156),
('16176','TDPR','00:49','00:50',2,160),
('16176','VM','02:00','02:10',2,202),
('16176','TMV','02:44','02:45',2,240),
('16176','MLMR','03:09','03:10',2,270),
('16176','CGL','03:43','03:45',2,305),
('16176','TBM','04:14','04:15',2,336),
('16176','MS','05:15','05:15',2,361);

insert into schedule(train_no,station_code,arrival,departure,day,distance) values
('10103','CSTM','7:10','7:10',1,0),
('10103','DR','07:22','07:25',1,9),
('10103','TNA','07:47','07:50',1,34),
('10103','PNVL','08:25','08:30',1,69),
('10103','MNI','10:33','10:35',1,188),
('10103','KHED','11:25','11:27',1,284),
('10103','CHI','11:57','11:59',1,325),
('10103','SGR','12:35','12:36',1,384),
('10103','RN','13:10','13:15',1,431),
('10103','ADVI','13:43','13:44',1,475),
('10103','RAJP','14:17','14:18',1,520),
('10103','VBW','14:39','14:40',1,543),
('10103','KKW','15:19','15:20',1,587),
('10103','SNDD','15:35','15:36',1,612),
('10103','KUDL','15:49','15:50',1,626),
('10103','SWV','16:15','16:16',1,655),
('10103','PERN','16:41','16:42',1,686),
('10103','THVM','16:53','16:55',1,701),
('10103','KRMI','17:13','17:14',1,725),
('10103','MAO','18:45','18:45',1,765);

insert into schedule(train_no,station_code,arrival,departure,day,distance) values

('12553','BJU','9:30','9:30',1,0),
('12553','DSS','10:00','10:01',1,28),
('12553','SPJ','10:25','10:30',1,51),
('12553','MFP','11:15','11:20',1,103),
('12553','HJP','12:08','12:10',1,157),
('12553','SEE','12:20','12:22',1,163),
('12553','CPR','13:40','13:45',1,216),
('12553','SV','14:30','14:30',1,277),
('12553','DEOS','15:29','15:30',1,347),
('12553','GKP','16:50','17:05',1,396),
('12553','KLD','17:43','17:45',1,431),
('12553','BST','18:10','18:15',1,460),
('12553','GD','19:35','19:40',1,550),
('12553','BBK','21:08','21:10',1,638),
('12553','LKO','21:55','22:05',1,674),
('12553','CNB','23:40','23:50',1,748),
('12553','ETW','01:41','01:43',2,886),
('12553','TDL','03:05','03:10',2,978),
('12553','ALJN','04:11','04:16',2,1056),
('12553','GZB','05:55','05:57',2,1162),
('12553','NDLS','06:45','06:45',2,1187);

insert into schedule(train_no,station_code,arrival,departure,day,distance) values
('12565','DBG','8:35','8:35',1,0),
('12565','SPJ','09:25','09:45',1,38),
('12565','MFP','10:35','10:40',1,90),
('12565','HJP','11:23','11:25',1,143),
('12565','SEE','11:38','11:40',1,149),
('12565','CPR','12:45','12:50',1,203),
('12565','SV','13:40','13:45',1,263),
('12565','GKP','15:50','16:10',1,383),
('12565','LKO','20:55','21:10',1,661),
('12565','CNB','22:48','22:58',1,735),
('12565','NDLS','05:35','05:35',2,1174);

insert into seating values
('16176',10,'1A'),
('16176',74,'2A'),
('16176',144,'3A'),
('16176',560,'SL');

insert into seating values
('10103',10,'1A'),
('10103',74,'2A'),
('10103',288,'3A'),
('10103',560,'SL'),
('10103',424,'2S');

insert into seating values
('12553',20,'1A'),
('12553',128,'2A'),
('12553',216,'3A'),
('12553',720,'SL');

insert into seating values
('12565',32,'1A'),
('12565',94,'2A'),
('12565',72,'3A'),
('12565',1040,'SL');