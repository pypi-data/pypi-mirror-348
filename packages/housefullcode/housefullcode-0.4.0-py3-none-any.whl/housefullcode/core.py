# my_package/core.py

def exp1():
    return """
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

 
# Load and preprocess the dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

 
# Normalize the data
x_train = x_train.reshape((x_train.shape[0], 28, 28, 1)).astype('float32') / 255
x_test = x_test.reshape((x_test.shape[0], 28, 28, 1)).astype('float32') / 255

 
# One-hot encode the labels
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

 
# Build the CNN model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),

 
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

 
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),

 
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')  # 10 classes for MNIST
])

 
# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

 
# Train the model
history = model.fit(x_train, y_train, epochs=5, batch_size=64,
                    validation_split=0.1)

 
# Evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'Test Accuracy: {test_acc:.4f}')
model.summary()
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Training vs Validation Accuracy')
plt.show()"""

def exp2():
    return """ 
    import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical
 
# Load CIFAR-10 dataset
(x_train, y_train), (x_test, y_test) = cifar10.load_data()
 
# Resize images from 32x32 to 96x96 and normalize
x_train = tf.image.resize(x_train, (96, 96)) / 255.0
x_test = tf.image.resize(x_test, (96, 96)) / 255.0
 
# One-hot encode labels
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)
 
# Load pre-trained MobileNetV2 model without top layers
base_model = MobileNetV2(input_shape=(96, 96, 3),
                         include_top=False,
                         weights='imagenet')
base_model.trainable = False  # Freeze base model layers
 
# Add custom classification head
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
outputs = Dense(10, activation='softmax')(x)  # CIFAR-10 has 10 classes
 
# Create model
model = Model(inputs=base_model.input, outputs=outputs)
 
# Compile model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
 
# Train model
model.fit(x_train, y_train, epochs=5, batch_size=64, validation_split=0.1)
 
# Evaluate model
loss, acc = model.evaluate(x_test, y_test)
print(f"Test Accuracy: {acc:.4f}")
    """

def exp3():
    return """
    import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical
 
# Load CIFAR-10 dataset
(x_train, y_train), (x_test, y_test) = cifar10.load_data()
 
# Resize images from 32x32 to 96x96 and normalize
x_train = tf.image.resize(x_train, (96, 96)) / 255.0
x_test = tf.image.resize(x_test, (96, 96)) / 255.0
 
# One-hot encode labels
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)
 
# Load pre-trained MobileNetV2 model without top layers
base_model = MobileNetV2(input_shape=(96, 96, 3),
                         include_top=False,
                         weights='imagenet')
base_model.trainable = False  # Freeze base model layers
 
# Add custom classification head
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
outputs = Dense(10, activation='softmax')(x)  # CIFAR-10 has 10 classes
 
# Create model
model = Model(inputs=base_model.input, outputs=outputs)
 
# Compile model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
 
# Train model
model.fit(x_train, y_train, epochs=5, batch_size=64, validation_split=0.1)
 
# Evaluate model
loss, acc = model.evaluate(x_test, y_test)
print(f"Test Accuracy: {acc:.4f}")
    """

def exp4():
    return """
    import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt

# Load dataset
(ds_train, ds_val, ds_test), ds_info = tfds.load(
    'stanford_dogs',
    split=['train[:80%]', 'train[80%:90%]', 'train[90%:]'],
    with_info=True,
    as_supervised=True,
)

IMG_SIZE = 160
BATCH_SIZE = 32
NUM_CLASSES = ds_info.features['label'].num_classes

# Preprocessing function
def preprocess(image, label):
    image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE)) / 255.0
    return image, tf.one_hot(label, NUM_CLASSES)

# Apply preprocessing and batching
ds_train = ds_train.map(preprocess).shuffle(1000).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
ds_val = ds_val.map(preprocess).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
ds_test = ds_test.map(preprocess).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

# Load MobileNetV2 base
base_model = MobileNetV2(input_shape=(IMG_SIZE, IMG_SIZE, 3),
                         include_top=False,
                         weights='imagenet')
base_model.trainable = False  # Freeze base model

# Add classification head
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
outputs = Dense(NUM_CLASSES, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=outputs)

# Compile
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train
history = model.fit(ds_train, validation_data=ds_val, epochs=3)

# Evaluate
loss, acc = model.evaluate(ds_test)
print(f"Test Accuracy: {acc:.4f}")
plt.plot(history.history['accuracy'], label='Train')
plt.plot(history.history['val_accuracy'], label='Val')
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.title("Accuracy over Epochs")
plt.show()
    """

def exp5():
    return """
    import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import string
 
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, SnowballStemmer
 
import tensorflow as tf
from tensorflow.keras.layers import Embedding, Dense, LSTM, Dropout, Bidirectional, BatchNormalization
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from tabulate import tabulate
 
 
from tensorflow.keras.datasets import imdb
 
# Only keep top 10,000 most frequent words
num_words = 10_000
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=num_words)
 
word_index = imdb.get_word_index()
reverse_word_index = {value: key for key, value in word_index.items()}
 
def decode_review(encoded_review):
    return ' '.join([reverse_word_index.get(i - 3, '?') for i in encoded_review])
 
print("🔹 Sample Decoded Review:\n", decode_review(x_train[0]))
print("🔹 Label:", y_train[0])
 
#
average_len = np.mean([len(x) for x in x_train])
max_len = int(average_len + 100)
print("Average Length:", average_len, "→ Using Max Length:", max_len)
 
 
train_pad = pad_sequences(x_train, maxlen=max_len, padding='post')
test_pad = pad_sequences(x_test, maxlen=max_len, padding='post')
 
 
model = tf.keras.models.Sequential([
    Embedding(input_dim=num_words, output_dim=16),
    Bidirectional(LSTM(32, return_sequences=True)),
    BatchNormalization(),
    Bidirectional(LSTM(64)),
    Dropout(0.3),
    Dense(512, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])
 
model.compile(
    loss='binary_crossentropy',
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    metrics=['accuracy']
)
 
model.summary()
 
early_stopping = EarlyStopping(monitor='val_accuracy', patience=3, restore_best_weights=True)
 
history = model.fit(
    train_pad, y_train,
    epochs=4,
    batch_size=64,
    validation_split=0.1,
    callbacks=[early_stopping]
)
 
 
plt.style.use('dark_background')
 
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()
 
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Val Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
 
 
predictions = model.predict(test_pad)
predicted_labels = np.round(predictions)
 
cm = confusion_matrix(y_test, predicted_labels)
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', annot_kws={"size": 16})
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()
 
 
accuracy = accuracy_score(y_test, predicted_labels)
precision = precision_score(y_test, predicted_labels)
recall = recall_score(y_test, predicted_labels)
f1 = f1_score(y_test, predicted_labels)
 
table = [
    ["Accuracy", accuracy],
    ["Precision", precision],
    ["Recall", recall],
    ["F1 Score", f1]
]
 
print(tabulate(table, headers=["Metric", "Value"], tablefmt="fancy_grid"))
 
# ====
def predict_sentiment(text, model, tokenizer=word_index, max_length=max_len):
    words = text.lower().split()
    encoded = []
    for word in words:
        idx = tokenizer.get(word, 2)  # 2 = unknown token
        encoded.append(idx)
    padded = pad_sequences([encoded], maxlen=max_length, padding='post')
    pred = model.predict(padded)
    label = int(np.round(pred[0][0]))
    sentiment = "Positive" if label == 1 else "Negative"
    print(f"Input: {text}")
    print(f"Predicted Sentiment: {sentiment} ({label})")
 
# Example Prediction
predict_sentiment("This movie was amazing and full of surprises!", model)
    """

def exp6():
    return """
    import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import string
 
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, SnowballStemmer
 
import tensorflow as tf
from tensorflow.keras.layers import Embedding, Dense, LSTM, Dropout, Bidirectional, BatchNormalization
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from tabulate import tabulate
 
 
from tensorflow.keras.datasets import imdb
 
# Only keep top 10,000 most frequent words
num_words = 10_000
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=num_words)
 
word_index = imdb.get_word_index()
reverse_word_index = {value: key for key, value in word_index.items()}
 
def decode_review(encoded_review):
    return ' '.join([reverse_word_index.get(i - 3, '?') for i in encoded_review])
 
print("🔹 Sample Decoded Review:\n", decode_review(x_train[0]))
print("🔹 Label:", y_train[0])
 
#
average_len = np.mean([len(x) for x in x_train])
max_len = int(average_len + 100)
print("Average Length:", average_len, "→ Using Max Length:", max_len)
 
 
train_pad = pad_sequences(x_train, maxlen=max_len, padding='post')
test_pad = pad_sequences(x_test, maxlen=max_len, padding='post')
 
 
model = tf.keras.models.Sequential([
    Embedding(input_dim=num_words, output_dim=16),
    Bidirectional(LSTM(32, return_sequences=True)),
    BatchNormalization(),
    Bidirectional(LSTM(64)),
    Dropout(0.3),
    Dense(512, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])
 
model.compile(
    loss='binary_crossentropy',
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    metrics=['accuracy']
)
 
model.summary()
 
early_stopping = EarlyStopping(monitor='val_accuracy', patience=3, restore_best_weights=True)
 
history = model.fit(
    train_pad, y_train,
    epochs=4,
    batch_size=64,
    validation_split=0.1,
    callbacks=[early_stopping]
)
 
 
plt.style.use('dark_background')
 
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()
 
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Val Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
 
 
predictions = model.predict(test_pad)
predicted_labels = np.round(predictions)
 
cm = confusion_matrix(y_test, predicted_labels)
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', annot_kws={"size": 16})
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()
 
 
accuracy = accuracy_score(y_test, predicted_labels)
precision = precision_score(y_test, predicted_labels)
recall = recall_score(y_test, predicted_labels)
f1 = f1_score(y_test, predicted_labels)
 
table = [
    ["Accuracy", accuracy],
    ["Precision", precision],
    ["Recall", recall],
    ["F1 Score", f1]
]
 
print(tabulate(table, headers=["Metric", "Value"], tablefmt="fancy_grid"))
 
# ====
def predict_sentiment(text, model, tokenizer=word_index, max_length=max_len):
    words = text.lower().split()
    encoded = []
    for word in words:
        idx = tokenizer.get(word, 2)  # 2 = unknown token
        encoded.append(idx)
    padded = pad_sequences([encoded], maxlen=max_length, padding='post')
    pred = model.predict(padded)
    label = int(np.round(pred[0][0]))
    sentiment = "Positive" if label == 1 else "Negative"
    print(f"Input: {text}")
    print(f"Predicted Sentiment: {sentiment} ({label})")
 
# Example Prediction
predict_sentiment("This movie was amazing and full of surprises!", model)
    """

def exp7():
    return """
    import numpy as np
import re
import nltk
import tensorflow as tf
import tensorflow_datasets as tfds

from nltk.tokenize import sent_tokenize
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Download necessary NLTK data
nltk.download('punkt')
# Add download for the punkt_tab resource specifically required by sent_tokenize
nltk.download('punkt_tab')
def clean_text(text):
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    return text
def load_imdb_data():
    data = tfds.load('imdb_reviews', split='train', as_supervised=True)
    texts, labels = [], []
    for text, label in tfds.as_numpy(data.take(5000)):  # Using a small subset
        texts.append(clean_text(text.decode('utf-8')))
        labels.append(int(label))
    return texts, labels

 
def summarize(document, model, tokenizer, max_len, top_n=3):
    sentences = sent_tokenize(document)
    sequences = tokenizer.texts_to_sequences(sentences)
    padded = pad_sequences(sequences, maxlen=max_len, padding='post')
    scores = model.predict(padded).flatten()
    top_idx = np.argsort(scores)[-top_n:]
    summary = [sentences[i] for i in sorted(top_idx)]
    return ' '.join(summary)
texts, labels = load_imdb_data()

tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts(texts)

sequences = tokenizer.texts_to_sequences(texts)
padded = pad_sequences(sequences, maxlen=100, padding='post')
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(10000, 64, input_length=100),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(padded, np.array(labels), epochs=3, batch_size=64, validation_split=0.2)
doc = (
    "This movie was fantastic! I loved the plot and the acting was superb. "
    "However, I felt that the ending was a bit rushed. The cinematography was stunning. "
    "The music added wonderful depth. I found myself emotionally invested. "
    "Overall, a great watch with minor flaws."
)

summary = summarize(doc, model, tokenizer, max_len=100, top_n=3)
print("Summary:\n", summary)
    """

def exp8():
    return """
    import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

 
# Load and preprocess the dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

 
# Normalize the data
x_train = x_train.reshape((x_train.shape[0], 28, 28, 1)).astype('float32') / 255
x_test = x_test.reshape((x_test.shape[0], 28, 28, 1)).astype('float32') / 255

 
# One-hot encode the labels
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

 
# Build the CNN model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),

 
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

 
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),

 
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')  # 10 classes for MNIST
])

 
# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

 
# Train the model
history = model.fit(x_train, y_train, epochs=5, batch_size=64,
                    validation_split=0.1)

 
# Evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'Test Accuracy: {test_acc:.4f}')
model.summary()
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Training vs Validation Accuracy')
plt.show()
    """

def exp9():
    return """

import kagglehub
from kagglehub import KaggleDatasetAdapter

file_path = "UrbanSound8K.csv"

df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "chrisfilo/urbansound8k",
  file_path,
)

print(df.head())
# 1. Import Libraries
import os
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import librosa
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical

# 2. Load and Preprocess Audio Data
def load_audio_files(data_path, max_files=100):
    X, y = [], []
    classes = os.listdir(data_path)
    for label in classes:
        class_dir = os.path.join(data_path, label)
        if not os.path.isdir(class_dir):
            continue
        for i, file in enumerate(os.listdir(class_dir)):
            if i >= max_files:
                break
            if file.endswith('.wav'):
                file_path = os.path.join(class_dir, file)
                try:
                    audio, sr = librosa.load(file_path, sr=16000)
                    X.append(audio)
                    y.append(label)
                except Exception as e:
                    print(f"Failed to load {file_path}: {e}")
    return X, y

# Replace with your dataset path (e.g., "UrbanSound8K/audio" with folders by class name)
dataset_path = "/kaggle/input/urbansound8k"
X_audio, y_labels = load_audio_files(dataset_path, max_files=50)

# 3. Extract Embeddings Using YAMNet
yamnet_model_handle = 'https://tfhub.dev/google/yamnet/1'
yamnet_model = hub.load(yamnet_model_handle)

def extract_embedding(audio):
    waveform = tf.convert_to_tensor(audio, dtype=tf.float32)
    waveform = tf.reshape(waveform, [-1])
    scores, embeddings, spectrogram = yamnet_model(waveform)
    return tf.reduce_mean(embeddings, axis=0).numpy()

print("Extracting embeddings...")
X_embeddings = [extract_embedding(audio) for audio in X_audio]

# 4. Encode Labels
le = LabelEncoder()
y_encoded = le.fit_transform(y_labels)
y_categorical = to_categorical(y_encoded)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_embeddings, y_categorical, test_size=0.2, random_state=42
)

# 5. Create and Train Custom Classifier
model = Sequential([
    Dense(512, activation='relu', input_shape=(1024,)),
    Dropout(0.3),
    Dense(256, activation='relu'),
    Dropout(0.3),
    Dense(len(le.classes_), activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

model.fit(
    np.array(X_train), np.array(y_train),
    epochs=20, batch_size=16, validation_split=0.2
)

# 6. Evaluate Model
loss, acc = model.evaluate(np.array(X_test), np.array(y_test))
print(f"Test Accuracy: {acc * 100:.2f}%")
    """

def exp10():
    return """

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, UpSampling2D, Input, BatchNormalization, ReLU
from tensorflow.keras.models import Model

# Build the deep neural network for image colorization
def build_colorization_network(input_shape=(256, 256, 1)):
    inputs = Input(shape=input_shape)

    # Encoder
    x1 = Conv2D(64, 3, padding='same', strides=2)(inputs)
    x1 = BatchNormalization()(x1)
    x1 = ReLU()(x1)

    x2 = Conv2D(128, 3, padding='same', strides=2)(x1)
    x2 = BatchNormalization()(x2)
    x2 = ReLU()(x2)

    x3 = Conv2D(256, 3, padding='same', strides=2)(x2)
    x3 = BatchNormalization()(x3)
    x3 = ReLU()(x3)

    # Bottleneck
    x = Conv2D(512, 3, padding='same')(x3)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    # Decoder
    x = UpSampling2D(size=(2, 2))(x)
    x = Conv2D(256, 3, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    x = UpSampling2D(size=(2, 2))(x)
    x = Conv2D(128, 3, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    x = UpSampling2D(size=(2, 2))(x)
    x = Conv2D(64, 3, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    # Output Layer (RGB prediction)
    outputs = Conv2D(3, 1, activation='sigmoid', padding='same')(x)

    return Model(inputs=inputs, outputs=outputs)

# Create and compile the model
model = build_colorization_network()
model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
model.summary()

# Dummy training data (replace with actual grayscale/color image pairs)
X_gray = np.random.rand(10, 256, 256, 1)   # 10 grayscale images
Y_color = np.random.rand(10, 256, 256, 3)  # 10 corresponding RGB images

# Train the model
model.fit(X_gray, Y_color, epochs=5, batch_size=2)

# Prediction and visualization
gray_input = X_gray[0:1]
predicted_color = model.predict(gray_input)[0]

plt.figure(figsize=(10, 4))
plt.subplot(1, 3, 1)
plt.imshow(gray_input[0, :, :, 0], cmap='gray')
plt.title('Grayscale Input')

plt.subplot(1, 3, 2)
plt.imshow(Y_color[0])
plt.title('Ground Truth Color')

plt.subplot(1, 3, 3)
plt.imshow(predicted_color)
plt.title('Predicted Color')
plt.show()
    """


def exp11():
    return """
    Muttapunda mam sonnathu 10 exp thana nee ena 11 ena klika pora 
    """

def help():
    return """
1. Build CNN model for sample dataset
2. Implement transfer learning with pre-trained CNN model
3. Implement transfer learning for image classification with CIFAR-10 dataset
4. Apply transfer learning for dog breed identification dataset
5. Build review sentiment classifier using transfer learning
6. Apply transfer learning for IMDB dataset with word embeddings
7. Create document summaries using transfer learning
8. Build multiclass classification with CNN model
9. Perform audio event classification with transfer learning
10. Build a coloring deep neural network


Any doubt in calling function use helpf() function 
    """

def helpf():
    return """
    use print(housefullcode.exp1())  to get code replace 1 with your exp no
    """

def ex1():
    return "You spelled it wrong  correct is exp1"

def ex2():
    return "You spelled it wrong  correct is exp2"

def ex3():
    return "You spelled it wrong  correct is exp3"

def ex4():
    return "You spelled it wrong  correct is exp4"
def ex5():
    return "You spelled it wrong  correct is exp5"

def ex6():
    return "You spelled it wrong  correct is exp6"
def ex7():
    return "You spelled it wrong  correct is exp7"

def ex8():
    return "You spelled it wrong  correct is exp8"
def ex9():
    return "You spelled it wrong  correct is exp9"
def ex10():
    return "You spelled it wrong  correct is exp10"