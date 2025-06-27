import pandas as pd
import csv

# Path to input file
input_csv = 'PhiUSIIL_Phishing_URL_Dataset.csv'

# Output file
output_csv = 'balanced_dataset_spaced.csv'

# Load original dataset
df = pd.read_csv(input_csv)
df['class'] = df['label'].map({0: -1, 1: 1})

# Sample 1000 phishing and 998 legit, add two long-legit manually
phish_df = df[df['class'] == -1].sample(n=1000, random_state=42)[['URL', 'class']]
legit_sample = df[df['class'] == 1].sample(n=998, random_state=42)[['URL', 'class']]
manual_legit = pd.DataFrame({
    'URL': [
        'https://booking.kayak.com/flights/BER-TAS/2025-08-06/ffab3f65966fe653f09e92b4fef7dd7d4?sort=bestflight_a&attempt=2&lastms=1750969639598',
        'https://www.kaggle.com/datasets/shashwatwork/web-page-phishing-detection-dataset'
    ],
    'class': [1, 1]
})
legit_df = pd.concat([legit_sample, manual_legit], ignore_index=True)
balanced = pd.concat([phish_df, legit_df], ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)

# Writes to CSV with a comma and space after each comma
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    writer.writerow(['URL', 'class'])
    for url, label in balanced.values:
        writer.writerow([url, f' {label}'])

print(f'✅ Saved to {output_csv}.')
