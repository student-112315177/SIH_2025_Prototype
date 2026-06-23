import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import pickle, os
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, "..")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
def get_kmer_features(sequences, k=6):
    all_kmer_counts = []
    for seq in sequences:
        kmer_counts = defaultdict(int)
        for i in range(len(seq) - k + 1):
            kmer = seq[i:i+k]
            if "N" not in kmer: kmer_counts[kmer] += 1
        all_kmer_counts.append(kmer_counts)
    return pd.DataFrame(all_kmer_counts).fillna(0)
print("Loading and preprocessing data for Random Forest...")
labeled_df = pd.read_csv(os.path.join(DATA_DIR, "labels", "deep_sea_labeled_clean.csv"))
encoder = LabelEncoder()
y = encoder.fit_transform(labeled_df['taxonomy'])
if not os.path.exists(MODELS_DIR): os.makedirs(MODELS_DIR)
with open(os.path.join(MODELS_DIR, 'label_encoder.pkl'), 'wb') as file: pickle.dump(encoder, file)
print(f"Label encoder saved to {os.path.join(MODELS_DIR, 'label_encoder.pkl')}")
X_kmer = get_kmer_features(labeled_df['sequence'])
X_train, X_test, y_train, y_test = train_test_split(X_kmer, y, test_size=0.3, random_state=42, stratify=y)
train_cols = X_train.columns
X_test = X_test.reindex(columns=train_cols, fill_value=0)
print("Training the Random Forest model...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
rf_model.fit(X_train, y_train)
print("\nEvaluating model performance...")
y_pred = rf_model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=encoder.classes_, zero_division=0))
with open(os.path.join(MODELS_DIR, 'random_forest_baseline.pkl'), 'wb') as file: pickle.dump(rf_model, file)
print(f"Random Forest model saved successfully to {os.path.join(MODELS_DIR, 'random_forest_baseline.pkl')}")