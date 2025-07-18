alter table cities 
add primary key (city_id);

alter table stations  
add primary key (station_id);

alter table stations
add constraint stat_city_id
foreign key (city_id)
references cities(city_id);

alter table vehicles 
add primary key (vehicle_id);

alter table drivers 
add primary key (driver_id);

alter table drivers 
add constraint driver_vehile
foreign  key (vehicle_id)
references vehicles(vehicle_id);






