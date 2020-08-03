use swiftrail;

-- Queries
-- Get Train Schedule
	select * from train_details join train using(train_no) where train_no='10103';
	select station_name, arrival, departure, distance, day  
	from schedule join station on schedule.station_code = station.station_code
	where train_no = '10103';

-- Reservation 
	-- Train between stations
		select S.train_no from schedule as S, schedule as T
		where S.station_code = 'CSTM'  and T.station_code = 'MAO' and
		S.distance < T.distance;

	-- Get Seat Availability (given train no, class, journey date)
		select ((select S.max_seats
		from seating as S
		where S.train_no = '10103' and S.class = '1A') -
		ifnull((select sum(seats) from allotted_seats 
		where train_no = '10103' and journey_date = '2019-09-13'
		group by class
		having class = '1A'),0)) as 'Available Seats';

-- Ticket details
	select * from ticket where pnr = '';
-- Transaction details
	select * from transaction where transaction_id = '';

-- Sample ticket booking