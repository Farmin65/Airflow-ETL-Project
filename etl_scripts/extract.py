import pandas as pd
import logging
import os


def extract_data(file_path: str) -> pd.DataFrame:
    logging.info(f"Reading from {file_path}")

    if not os.path.exists(file_path):
        logging.warning("Source file missing, generating test dataset")
        test_data = {
            'order_id': [101, 102, 103, 104, 105],
            'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Laptop'],
            'price': ['1200.50', '25', '45.00', '300', '1250.00'],
            'quantity': [1, 5, 3, 2, 1],
            'order_date': ['2026-04-15', '2026-04-16', '2026-04-16', 'bad_date', '2026-04-17']
        }
        df = pd.DataFrame(test_data)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)

    df = pd.read_csv(file_path)
    logging.info(f"Extracted {len(df)} rows")
    return df