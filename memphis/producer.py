from memphis import Memphis, Headers

# Asinxron funksiyadan istifadə olunur
import asyncio

async def main():
    memphis = Memphis()

    # 1. Bağlantı yarat
    await memphis.connect(
        host="localhost",
        port=6666,
        username="memphis",
        password="R03292001afael@",
    )

    producer = await memphis.producer(station_name="main", producer_name="my-producer")

    for i in range(10):  # real-time 10 mesaj göndərmək nümunəsi
        msg = f"Real-time message {i}"
        await producer.produce(msg)  # mesaj byte kimi göndərilir
        print(f"Sent: {msg}")
        await asyncio.sleep(1)  # 1 saniyə fasilə — real-time fasiləsiz də ola bilər

    await memphis.close()
# Run the async main
asyncio.run(main())
