import csv
import numpy as np

# Initialize lists to hold the scores
python_scores = []
manual_scores = []

# Open the CSV file and read the scores into the lists
with open('rula_scores.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        python_scores.append(float(row['Python Score']))
        manual_scores.append(float(row['Manual Score']))

# Convert the lists to numpy arrays
python_scores = np.array(python_scores)
manual_scores = np.array(manual_scores)

# Calculate Pearson's correlation coefficient
correlation = np.corrcoef(python_scores, manual_scores)[0, 1]

print(f"Pearson's correlation coefficient: {correlation}")
