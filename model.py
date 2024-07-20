import torch
import torch.nn as nn

# Definicja klasy sieci neuronowej
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        # Pierwsza warstwa liniowa
        self.l1 = nn.Linear(input_size, hidden_size)
        # Druga warstwa liniowa
        self.l2 = nn.Linear(hidden_size, hidden_size)
        # Trzecia warstwa liniowa (wyjściowa)
        self.l3 = nn.Linear(hidden_size, num_classes)
        # Funkcja aktywacji ReLU
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.3)
        
    def forward(self, x):
        # Przejście przez pierwszą warstwę i aktywację
        out = self.l1(x)
        out = self.relu(out)
        out = self.dropout(out) 
        # Przejście przez drugą warstwę i aktywację
        out = self.l2(out)
        out = self.relu(out)
        out = self.dropout(out)
        # Przejście przez trzecią warstwę (bez aktywacji)
        out = self.l3(out)
        return out  # Zwraca surowe wartości logitów (bez softmax)
