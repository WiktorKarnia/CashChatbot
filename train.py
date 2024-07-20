import json
from nltk_utils import tokenize, stem, bag_of_words, detect_language
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet

# Załadowanie danych intencji z pliku JSON
with open('exchange-intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []

# Ignorowane znaki
ignore_words = ['?', '!', '<', '>', ',', '.', '/']

# Przetwarzanie danych intencji
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        language = detect_language(pattern)
        if language == 'unknown':
            continue
        w = tokenize(pattern, language=language)
        all_words.extend([stem(word, language) for word in w if word not in ignore_words and word is not None])
        xy.append((w, tag, language))

# Filtruj None z all_words
all_words = [word for word in all_words if word is not None]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

# Przygotowanie danych treningowych
x_train = []
y_train = []
for (pattern_sentence, tag, language) in xy:
    bag = bag_of_words(pattern_sentence, all_words, language=language)
    x_train.append(bag)
    label = tags.index(tag)
    y_train.append(label)

x_train = np.array(x_train)
y_train = np.array(y_train)

# Definicja datasetu
class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples

# Hiperparametry
batch_size = 32
hidden_size = 32
output_size = len(tags)
input_size = len(x_train[0])
learning_rate = 0.001
num_epochs = 2000

# Główna funkcja treningowa
if __name__ == '__main__':
    dataset = ChatDataset()
    train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=2, persistent_workers=True)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = NeuralNet(input_size, hidden_size, output_size).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        for (words, labels) in train_loader:
            words = words.to(device)
            labels = labels.to(device, dtype=torch.int64)

            # Przepuszczenie danych przez model (forward pass)
            outputs = model(words)
            loss = criterion(outputs, labels)

            # Obliczenie gradientów i optymalizacja
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if (epoch+1) % 100 == 0:
            print(f'epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}')

    print(f'final loss, loss={loss.item():.4f}')

    # Zapisanie wytrenowanego modelu
    data = {
        "model_state": model.state_dict(),
        "input_size": input_size,
        "output_size": output_size,
        "hidden_size": hidden_size,
        "all_words": all_words,
        "tags": tags
    }

    FILE = "data.pth"
    torch.save(data, FILE)

    print(f'Trainining complete. File saved to {FILE}')
