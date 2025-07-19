/* SQL scripting 
* How many stations are there of each?.*/

select count(s.station_id),c.city_name
from stations as s 
join cities as c on s.city_id = c.city_id
group by c.city_name ;

/* How many times has each vehicle been on a trip? */

select count(t.vehicle_id ) ,r.vehicle_type 
from trips as t
join routes as r on r.route_id = t.route_id 
group  by t.vehicle_type ;


select c.city_name,c.city_id,s.station_name
from cities c
left join stations s on c.city_id =s.city_id ;


select c.city_name,c.city_id,s.station_name
from cities c
full join stations s on c.city_id =s.city_id ;



select c.city_name, count(s.station_id) as station_count
from cities c
join stations s on c.city_id = s.city_id 
group by c.city_name
having  count(s.station_id) > 1;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'tickets' AND column_name = 'purchase_time';

select purchase_time
from tickets;

SELECT TO_TIMESTAMP(purchase_time, 'YYYY-MM-DD HH24:MI:SS') FROM tickets;

ALTER TABLE tickets 
ALTER COLUMN purchase_time TYPE timestamp
USING purchase_time::timestamp;


SELECT EXTRACT(month FROM purchase_time)
FROM tickets;


