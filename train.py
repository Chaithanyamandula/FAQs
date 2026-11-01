import random
import numpy as np, pandas as pd, torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "distilbert-base-uncased" # use "bert-base-uncased" for full BERT
EPOCHS, BATCH, LR, MAX_LEN, SEED = 8, 8, 5e-5, 48, 42
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)

# 1. Load data and split 80% train / 20% test
df = pd.read_csv("data/faq_data.csv").dropna()
labels = sorted(df["category"].unique())
label2id = {l: i for i, l in enumerate(labels)}
id2label = {i: l for l, i in label2id.items()}
df["label"] = df["category"].map(label2id)
train_df, test_df = train_test_split(df, test_size=0.2, stratify=df["label"], random_state=SEED)

# 2. Tokenizer: turns text into token IDs (padding makes a batch the same length)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def collate(batch):
    texts, ys = zip(*batch)
    enc = tokenizer(list(texts), padding=True, truncation=True, max_length=MAX_LEN, return_tensors="pt")
    enc["labels"] = torch.tensor(ys)
    return enc

def make_loader(frame, shuffle):
    data = list(zip(frame["question"].tolist(), frame["label"].tolist()))
    return DataLoader(data, batch_size=BATCH, shuffle=shuffle, collate_fn=collate)

train_loader, test_loader = make_loader(train_df, True), make_loader(test_df, False)

# 3. Model: pre-trained DistilBERT + a fresh classification layer with 6 outputs
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME, num_labels=len(labels), id2label=id2label, label2id=label2id)
optimizer = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=0.01)

# 4. Training loop: forward pass, loss, backward pass, update weights
for epoch in range(1, EPOCHS + 1):
    model.train()
    total = 0.0
    for batch in train_loader:
        loss = model(**batch).loss # labels are inside the batch
        loss.backward()
        optimizer.step(); optimizer.zero_grad()
        total += loss.item()
    print(f"Epoch {epoch}/{EPOCHS} loss = {total / len(train_loader):.4f}")

# 5. Evaluate on the unseen test questions
model.eval()
truth, preds = [], []
with torch.no_grad():
    for batch in test_loader:
        y = batch.pop("labels")
        preds += model(**batch).logits.argmax(dim=-1).tolist()
        truth += y.tolist()

print("\nTest accuracy:", round(accuracy_score(truth, preds), 4))
print(classification_report(truth, preds, labels=list(range(len(labels))), target_names=labels,
                            zero_division=0))

# 6. Save the model and tokenizer for the web app
model.save_pretrained("model"); tokenizer.save_pretrained("model")
print("Saved to model/")
