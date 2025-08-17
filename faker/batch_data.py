# main.py
from create import TransitDataGenerator

if __name__ == "__main__":
    generator = TransitDataGenerator()
    batch_data = generator.generate_batch(n=5)  # 5 records batch for each table
