import json
import time
import psycopg2
import psycopg2.extras
import asyncio
import threading
from memphis import Memphis

# =====================
# Memphis (async) 
# =====================
class MemphisProducer:
    def __init__(self, host, port, username, password, station):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.station = station
        self.memphis = Memphis()
        self.producer = None

    async def connect(self):
        await self.memphis.connect(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password
        )
        self.producer = await self.memphis.producer(self.station, producer_name="wal2json")
        print("[Memphis] Connected and producer ready.")

    async def send(self, data: dict):
        msg_str = json.dumps(data)
        await self.producer.produce(msg_str.encode())

    async def close(self):
        await self.memphis.close()
        print("[Memphis] Connection closed.")

# =====================================================
# PostgreSQL Logical Replication (sync)
# =====================================================
class PostgresCDC:
    def __init__(self, dsn, slot_name, send_callback):
        self.dsn = dsn
        self.slot_name = slot_name
        self.send_callback = send_callback  # async callback

    def consume(self, msg, cursor):
        try:
            change = json.loads(msg.payload)
            print("Received CDC change:", json.dumps(change, indent=2))
            asyncio.run_coroutine_threadsafe(self.send_callback(change), asyncio.get_event_loop())
            cursor.send_feedback(flush_lsn=msg.data_start)
        except Exception as e:
            print("Error processing message:", e)

    def start(self):
        conn = psycopg2.connect(
            self.dsn,
            connection_factory=psycopg2.extras.LogicalReplicationConnection
        )
        cur = conn.cursor()
        print("[Postgres] Starting replication...")
        cur.start_replication(slot_name=self.slot_name, options={"pretty-print": 1}, decode=True)
        try:
            cur.consume_stream(self.consume)
        except KeyboardInterrupt:
            print("[Postgres] Replication stopped by user.")
        finally:
            cur.close()
            conn.close()

# =====================================================
# Main idarəedici funksiya
# =====================================================
async def main():
    memphis_client = MemphisProducer(
        host="localhost",
        port=6666,
        username="memphis",
        password="R03292001afael@",
        station="main"
    )
    await memphis_client.connect()

    dsn = "dbname=mydb user=postgres password=postgres_password host=127.0.0.1 port=5432"
    slot_name = "my_slot"

    postgres_cdc = PostgresCDC(
        dsn=dsn,
        slot_name=slot_name,
        send_callback=memphis_client.send
    )

    thread = threading.Thread(target=postgres_cdc.start, daemon=True)
    thread.start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Stopping system...")
    finally:
        await memphis_client.close()

if __name__ == "__main__":
    asyncio.run(main())
