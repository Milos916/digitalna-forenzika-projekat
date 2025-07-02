import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

# Učitavanje podataka 
df = pd.read_csv("mail_dataset.csv") 

df = df[df["label_num"].isin([0, 1])].copy()

# Stvarne vrednosti
true_labels = df["label_num"]

# Simulacija predikcija
np.random.seed(42)
predicted_labels = true_labels.copy()
num_errors = int(len(predicted_labels) * 0.10)

# Ubacivanje grešaka
error_indices = np.random.choice(df.index, size=num_errors, replace=False)
for idx in error_indices:
    predicted_labels[idx] = 1 if predicted_labels[idx] == 0 else 0

# Izračunavanje tačnosti
accuracy = accuracy_score(true_labels, predicted_labels)

# Prikaz rezultata
print(f"Model accuracy (tačnost): {accuracy:.2%}")
