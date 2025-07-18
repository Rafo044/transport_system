/* SQL scripting 
* How many stations are there of each?.*/

select count(s.station_id),c.city_name
from stations as s 
join cities as c on s.city_id = c.city_id
group by c.city_name ;

/* How many times has each vehicle been on a trip? */

select count(t.tip_id) ,r.vehicle_type 
from trips as t
join routes as r on r.route_id = t.route_id 
group  by t.trip_id ;


