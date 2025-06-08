# ai_module/neural_net.py
import torch
import torch.nn as nn
import torch.optim as optim
import time
import numpy as np
from django.conf import settings

###############################################################################
#                     МОДЕЛЬ WORD-LEVEL (LSTM)                                #
###############################################################################
class WordHeadlineGeneratorModel(nn.Module):
    """LSTM-модель для работы со словами (word-level)."""

    def __init__(self, vocab_size, embed_size=128, hidden_size=256):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, hidden=None):
        # x shape: (batch, seq_len) — индексы слов
        embed = self.embedding(x)       # (batch, seq_len, embed_size)
        output, hidden = self.lstm(embed, hidden)  # (batch, seq_len, hidden_size)
        logits = self.fc(output)        # (batch, seq_len, vocab_size)
        return logits, hidden


###############################################################################
#                     ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ДЛЯ WORD-УРОВНЯ                   #
###############################################################################
word_model = None           # сама PyTorch-модель
word_to_idx = {}            # { "привет": 0, "мир": 1, ... }
idx_to_word = {}            # { 0: "привет", 1: "мир", ... }


###############################################################################
#         ПОДГОТОВКА ДАТАСЕТА (WORD-BASED) И ОПРЕДЕЛЕНИЕ СЛОВАРЯ              #
###############################################################################
def prepare_word_dataset(headlines, seq_length=5):
    """
    1) Токенизирует каждую строку (заголовок) -> список слов.
    2) Создаёт словарь word_to_idx, idx_to_word.
    3) Формирует обучающие пары (X, y): 
       X — seq_length слов,     y — следующее слово.
    4) Возвращает тензоры X, y.
    """
    global word_to_idx, idx_to_word

    # 1. Собираем все слова
    all_tokens = []
    tokenized_lines = []
    for line in headlines:
        # простая токенизация (разбиваем по пробелам)
        # Можно улучшить: убрать пунктуацию, приводить к нижнему регистру и т.д.
        tokens = line.strip().split()
        if len(tokens) > 0:
            tokenized_lines.append(tokens)
            all_tokens.extend(tokens)

    # Удаляем дубликаты, формируем словарь
    vocab = sorted(list(set(all_tokens)))
    word_to_idx = {w: i for i, w in enumerate(vocab)}
    idx_to_word = {i: w for w, i in word_to_idx.items()}

    # 2. Готовим обучающие сэмплы
    X_data = []
    y_data = []

    for tokens in tokenized_lines:
        if len(tokens) < seq_length+1:
            continue  # слишком короткая строка, пропустим
        for i in range(len(tokens) - seq_length):
            seq_x = tokens[i : i + seq_length]         # seq_length слов
            next_word = tokens[i + seq_length]         # цель (следующее слово)
            # Преобразуем слова -> индексы
            X_idx = [word_to_idx[w] for w in seq_x]
            y_idx = word_to_idx[next_word]
            X_data.append(X_idx)
            y_data.append(y_idx)

    if not X_data:
        return None, None

    # Превращаем в тензоры
    X_tensor = torch.tensor(X_data, dtype=torch.long)
    y_tensor = torch.tensor(y_data, dtype=torch.long)
    return X_tensor, y_tensor


###############################################################################
#                ФУНКЦИЯ ОБУЧЕНИЯ WORD-LEVEL МОДЕЛИ                           #
###############################################################################
def train_model(headlines, epochs=5):
    """
    Переобучаем (или обучаем) глобальную модель word_model на наборе заголовков.
    Использует LSTM на уровне слов.
    """
    global word_model, word_to_idx, idx_to_word

    if not headlines:
        return None

    # Подготовка датасета
    X, y = prepare_word_dataset(headlines, seq_length=5)
    if X is None or y is None:
        # Нет достаточных данных для обучения
        return None

    vocab_size = len(word_to_idx)
    # Инициализируем новую модель
    word_model = WordHeadlineGeneratorModel(vocab_size)

    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.Adam(word_model.parameters(), lr=0.01)

    start_time = time.time()

    for epoch in range(epochs):
        optimizer.zero_grad()

        # Прямой проход
        logits, _ = word_model(X)  # logits: (batch_size, seq_len=5, vocab_size)

        # Берём выход по последнему слову в последовательности
        # logits[:, -1, :] -> (batch_size, vocab_size)
        final_logits = logits[:, -1, :]

        loss = loss_fn(final_logits, y)  # y shape: (batch_size, )

        # Обратный проход
        loss.backward()
        optimizer.step()

    elapsed = time.time() - start_time
    return elapsed


###############################################################################
#        ГЕНЕРАЦИЯ ЗАГОЛОВКА (WORD-LEVEL)                                     #
###############################################################################
def generate_headline(
    mode="random",
    max_length=12,
    start_text=""
):
    """
    Генерация заголовка словесной LSTM-моделью:
     - mode="random" или "greedy".
     - max_length - макс. кол-во слов.
     - start_text - начальные слова (не обязательно).
    """
    global word_model, word_to_idx, idx_to_word

    if word_model is None or not word_to_idx:
        return "Модель не обучена"

    # Разбиваем start_text на список слов (токенизируем)
    current_tokens = start_text.strip().split()
    if not current_tokens:
        # Если пусто, начнём с рандомного слова (или можно <START>)
        # Но пусть будет простое решение:
        current_tokens = [np.random.choice(list(word_to_idx.keys()))]

    hidden = None

    for _ in range(max_length):
        # Берём seq_length последних слов (у нас seq=5 в обучении)
        seq_length = 5
        if len(current_tokens) < seq_length:
            pad_size = seq_length - len(current_tokens)
            # Простой вариант: заполним "дырки" каким-то словом из словаря
            # Можно <PAD> токен завести, но упростим
            padded = [current_tokens[0]] * pad_size + current_tokens
            input_tokens = padded[-seq_length:]
        else:
            input_tokens = current_tokens[-seq_length:]

        # Превращаем слова -> индексы
        input_idx = [word_to_idx.get(w, 0) for w in input_tokens]
        x_tensor = torch.tensor([input_idx], dtype=torch.long)  # shape (1, seq_len)

        # Прогоняем через модель
        with torch.no_grad():
            logits, hidden = word_model(x_tensor, hidden)
            # logits: (batch=1, seq_len=5, vocab_size)
            final_logits = logits[:, -1, :]   # (1, vocab_size)
            probs = torch.softmax(final_logits, dim=1).squeeze(0)  # (vocab_size,)

        if mode == "random":
            # Сэмплируем следующее слово из вероятностей
            probs_np = probs.detach().numpy()
            next_idx = np.random.choice(len(probs_np), p=probs_np)
        else:
            # greedy
            next_idx = torch.argmax(probs).item()

        next_word = idx_to_word.get(next_idx, "<UNK>")

        # Если модель сгенерировала что-то типа <END>, можно остановиться
        # (Предположим, что <END> =  "##end##" если захотим)
        # if next_word == "##end##":
        #    break

        current_tokens.append(next_word)

    # Соединяем в строку
    generated_line = " ".join(current_tokens)
    return generated_line

