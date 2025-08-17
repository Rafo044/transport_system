# create.py
from faker import Faker
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any

fake = Faker()

class TransitDataGenerator:
    def __init__(self):
        # in-memory tables
        self.cities: List[Dict[str, Any]] = []
        self.stations: List[Dict[str, Any]] = []
        self.routes: List[Dict[str, Any]] = []
        self.vehicles: List[Dict[str, Any]] = []
        self.drivers: List[Dict[str, Any]] = []
        self.tickets: List[Dict[str, Any]] = []
        self.schedules: List[Dict[str, Any]] = []
        self.gps_logs: List[Dict[str, Any]] = []
        self.passenger_counts: List[Dict[str, Any]] = []
        self.fare_cards: List[Dict[str, Any]] = []
        self.payments: List[Dict[str, Any]] = []
        self.incidents: List[Dict[str, Any]] = []
        self.users: List[Dict[str, Any]] = []


    # ---------- 1. City ----------
    def generate_city(self) -> Dict[str, Any]:
        city = {
            "city_id": str(uuid.uuid4()),
            "city_name": fake.city()
        }
        self.cities.append(city)
        return city

    # ---------- 2. Stations ----------
    def generate_station(self) -> Dict[str, Any]:
        if not self.cities:
            self.generate_city()
        station = {
            "station_id": str(uuid.uuid4()),
            "station_name": fake.street_name(),
            "city_id": self.cities[-1]["city_id"],
            "district": fake.state(),
            "is_active": random.choice([True, False])
        }
        self.stations.append(station)
        return station

    # ---------- 3. Routes ----------
    def generate_route(self) -> Dict[str, Any]:
        if not self.cities:
            self.generate_city()
        route = {
            "route_id": str(uuid.uuid4()),
            "route_number": str(random.randint(1, 999)),
            "vehicle_type": random.choice(["bus", "tram", "minibus"]),
            "city_id": self.cities[-1]["city_id"]
        }
        self.routes.append(route)
        return route

    # ---------- 4. Vehicles ----------
    def generate_vehicle(self) -> Dict[str, Any]:
        if not self.routes:
            self.generate_route()
        vehicle = {
            "vehicle_id": str(uuid.uuid4()),
            "vehicle_number": f"{random.randint(1000,9999)}-{random.choice(['A','B','C'])}",
            "capacity": random.randint(20, 80),
            "route_id": self.routes[-1]["route_id"]
        }
        self.vehicles.append(vehicle)
        return vehicle

    # ---------- 5. Drivers ----------
    def generate_driver(self) -> Dict[str, Any]:
        if not self.vehicles:
            self.generate_vehicle()
        driver = {
            "driver_id": str(uuid.uuid4()),
            "full_name": fake.name(),
            "licance_number": fake.bothify(text="??-#####"),
            "vehicle_id": self.vehicles[-1]["vehicle_id"]
        }
        self.drivers.append(driver)
        return driver

    # ---------- 6. Schedules ----------
    def generate_schedule(self) -> Dict[str, Any]:
        if not (self.routes and self.vehicles and self.drivers):
            # ensure minimal dependencies exist
            self.generate_route(); self.generate_vehicle(); self.generate_driver()
        departure = fake.date_time_between(start_date='-7d', end_date='+7d')
        arrival = departure + timedelta(minutes=random.randint(15, 180))
        schedule = {
            "schedule_id": str(uuid.uuid4()),
            "route_id": self.routes[-1]["route_id"],
            "vehicle_id": self.vehicles[-1]["vehicle_id"],
            "driver_id": self.drivers[-1]["driver_id"],
            "departure_time": departure.isoformat(),
            "arrival_time": arrival.isoformat()
        }
        self.schedules.append(schedule)
        return schedule

    # ---------- 7. Tickets ----------
    def generate_ticket(self) -> Dict[str, Any]:
        if not self.schedules:
            self.generate_schedule()
        ticket = {
            "ticket_id": str(uuid.uuid4()),
            "trip_id": self.schedules[-1]["schedule_id"],
            "passengers_name": fake.name(),
            "seat_number": random.randint(1, 50),
            "price": round(random.uniform(0.5, 10.0), 2),
            "purchase_time": fake.date_time_between(start_date='-30d', end_date='now').isoformat()
        }
        self.tickets.append(ticket)
        return ticket

    # ---------- 8. GPS Logs ----------
    def generate_gps_log(self) -> Dict[str, Any]:
        if not self.vehicles:
            self.generate_vehicle()
        log = {
            "log_id": str(uuid.uuid4()),
            "vehicle_id": self.vehicles[-1]["vehicle_id"],
            "timestamp": datetime.utcnow().isoformat(),
            "latitude": round(float(fake.latitude()), 6),
            "longitude": round(float(fake.longitude()), 6)
        }
        self.gps_logs.append(log)
        return log

    # ---------- 9. Passenger Counts ----------
    def generate_passenger_count(self) -> Dict[str, Any]:
        if not (self.stations and self.schedules):
            self.generate_station(); self.generate_schedule()
        count = {
            "count_id": str(uuid.uuid4()),
            "station_id": self.stations[-1]["station_id"],
            "trip_id": self.schedules[-1]["schedule_id"],
            "timestamp": datetime.utcnow().isoformat(),
            "passenger_count": random.randint(0, 60)
        }
        self.passenger_counts.append(count)
        return count

    # ---------- 10. Fare Cards ----------
    def generate_fare_card(self) -> Dict[str, Any]:
        if not self.users:
            self.generate_user()
        card = {
            "card_id": str(uuid.uuid4()),
            "user_id": self.users[-1]["user_id"],
            "issue_date": fake.date_this_year().isoformat(),
            "balance": round(random.uniform(0, 100), 2)
        }
        self.fare_cards.append(card)
        return card

    # ---------- 11. Payments ----------
    def generate_payment(self) -> Dict[str, Any]:
        if not self.fare_cards:
            self.generate_fare_card()
        payment = {
            "payment_id": str(uuid.uuid4()),
            "card_id": self.fare_cards[-1]["card_id"],
            "amount": round(random.uniform(0.2, 50.0), 2),
            "payment_time": datetime.utcnow().isoformat()
        }
        self.payments.append(payment)
        return payment

    # ---------- 12. Incidents ----------
    def generate_incident(self) -> Dict[str, Any]:
        if not self.schedules:
            self.generate_schedule()
        incident = {
            "incident_id": str(uuid.uuid4()),
            "trip_id": self.schedules[-1]["schedule_id"],
            "incident_time": datetime.utcnow().isoformat(),
            "description": fake.sentence(nb_words=8)
        }
        self.incidents.append(incident)
        return incident

    # ---------- 13. Users ----------
    def generate_user(self) -> Dict[str, Any]:
        user = {
            "user_id": str(uuid.uuid4()),
            "full_name": fake.name(),
            "email": fake.email(),
            "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat()
        }
        self.users.append(user)
        return user

    # ---------- Batch helper: generate many ----------------
    def generate_batch(self, n: int = 10) -> None:
        """Generate a batch of interrelated records. n controls how many 'units' to create.
        The method will create multiple related objects.
        """
        for _ in range(n):
            # create a city per iteration to get variety
            self.generate_city()
            # create a few stations per city
            for _ in range(random.randint(1, 3)):
                self.generate_station()
            # create routes & vehicles & drivers
            for _ in range(random.randint(1, 3)):
                self.generate_route()
                self.generate_vehicle()
                self.generate_driver()
            # schedules and tickets
            for _ in range(random.randint(1, 4)):
                self.generate_schedule()
                # some tickets
                for _ in range(random.randint(0, 3)):
                    self.generate_ticket()
            # random telemetry & counts
            for _ in range(random.randint(1, 5)):
                self.generate_gps_log()
                self.generate_passenger_count()
            # users, cards, payments, incidents
            for _ in range(random.randint(0, 2)):
                self.generate_user()
                self.generate_fare_card()
                self.generate_payment()
            if random.random() < 0.2:
                self.generate_incident()

    # ---------- Utility: collect tables ----------
    def tables(self) -> Dict[str, List[Dict[str, Any]]]:
        return {
            "cities": self.cities,
            "stations": self.stations,
            "routes": self.routes,
            "vehicles": self.vehicles,
            "drivers": self.drivers,
            "schedules": self.schedules,
            "tickets": self.tickets,
            "gps_logs": self.gps_logs,
            "passenger_counts": self.passenger_counts,
            "users": self.users,
            "fare_cards": self.fare_cards,
            "payments": self.payments,
            "incidents": self.incidents,
        }
    

    