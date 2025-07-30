experiment = {
    1:"""EXPERIMENT : 1                                                LINK:https://colab.research.google.com/drive/1JEKC_hQfkfJ7Jep1TdeMxvQlZeKkYEWD?usp=sharing
import kagglehub
import os
import tensorflow as tf
import matplotlib.pyplot as plt

dataset_path = kagglehub.dataset_download("muratkokludataset/rice-image-dataset")

data_dir = os.path.join(dataset_path, "Rice_Image_Dataset")

batch_size = 64
img_size = (150, 150)

raw_train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=img_size,
    batch_size=batch_size
)

raw_val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=img_size,
    batch_size=batch_size
)

class_names = raw_train_ds.class_names
num_classes = len(class_names)

normalization_layer = tf.keras.layers.Rescaling(1./255)
train_ds = raw_train_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds = raw_val_ds.map(lambda x, y: (normalization_layer(x), y))

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(train_ds, validation_data=val_ds, epochs=5)

plt.plot(history.history['accuracy'], label='Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()""",
2:"""EXPERIMENT : 2                                                LINK:https://drive.google.com/file/d/1Xy_2qF-6nM3epZ8jdEMgNzkiao2C-bNZ/view?usp=sharing
!pip install -qq opendatasets

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras.models import *
from keras.layers import *
import opendatasets as od
from tensorflow.keras import layers, models


od.download("https://www.kaggle.com/datasets/hemendrasr/pizza-vs-ice-cream")

train_dir = '/content/pizza-vs-ice-cream/dataset/train'
test_dir = '/content/pizza-vs-ice-cream/dataset/test'

from keras.utils import image_dataset_from_directory
train_dataset = image_dataset_from_directory(train_dir, image_size=(600, 600), batch_size=32)
test_dataset = image_dataset_from_directory(test_dir, image_size=(600, 600), batch_size=32)

plt.figure(figsize=(10, 10))
for images, labels in test_dataset:
    for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"))
        plt.title(int(labels[i]))
        plt.axis("off")

input_shape = (600, 600, 3)



base_model = tf.keras.applications.InceptionV3(
    input_shape=input_shape,
    include_top=False,
    weights='imagenet'
)

base_model = tf.keras.applications.ResNet50(
    input_shape=input_shape,
    include_top=False,
    weights='imagenet'
)


base_model.trainable = False

resnet = models.Sequential([
    base_model,
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

resnet.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = resnet.fit(
    train_dataset,
    validation_data=test_dataset,
    epochs=1
)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()

from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

resnet.evaluate(test_dataset)

y_pred = resnet.predict(test_dataset)
y_pred_classes = np.where(y_pred > 0.5, 1, 0)
# y_pred_classes = np.argmax(y_pred, axis=1)  # For multi-class classification
y_true = np.concatenate([y for x, y in test_dataset], axis=0)

cm = confusion_matrix(y_true, y_pred_classes)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

print('Classification Report')
print(classification_report(y_true, y_pred_classes))""",
3:"""EXPERIMENT : 3                                                LINK:https://drive.google.com/file/d/1SJzXD-1LUgbhidGZcXvlDdz3skD2g1cN/view?usp=sharing
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.layers import Conv2D,BatchNormalization,MaxPooling2D,GlobalAveragePooling2D,Dense,Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import VGG16
from tensorflow.keras import layers,models

(x_train, y_train), (x_test, y_test) = cifar10.load_data()

KFOLD_WEIGHT_PATH=r'../model/cnn_cifar10_weights_{epoch:02d}_{val_acc:.2f}.hdf5'

x_train=x_train/255
x_test=x_test/255
y_train=keras.utils.to_categorical(y_train,10)
y_test=keras.utils.to_categorical(y_test,10)

b_m = VGG16(include_top=False,weights='imagenet')
b_m.trainable=False

model = models.Sequential([
    b_m,
    GlobalAveragePooling2D(),
    BatchNormalization(),
    layers.Flatten(),
    Dense(32,activation='relu'),
    Dropout(0.3),
    Dense(10,activation='softmax')
])

model.compile(loss='categorical_crossentropy',optimizer='Adam',metrics=['accuracy'])
model.summary()

from keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(monitor='val_loss',patience=5,restore_best_weights=True)

his = model.fit(x_train,y_train,validation_split=0.1,batch_size=32,epochs=2,callbacks=[early_stopping])

res = model.evaluate(x_test,y_test)[1]*100
print("Score : ",res)""",

4:"""EXPERIMENT : 4                                                LINK:https://drive.google.com/file/d/18zKnPCJeX9rdiuHX5BODUN4202MMEZuk/view?usp=sharing
import keras
import numpy as np
from keras.models import Sequential
from keras import regularizers, optimizers
from keras.layers import Dense, Dropout, Flatten,GlobalAveragePooling2D
from tensorflow.keras.applications import ResNet50
from keras.layers import Conv2D, MaxPooling2D,BatchNormalization

!pip install opendatasets
import opendatasets as op

op.download('https://www.kaggle.com/datasets/jessicali9530/stanford-dogs-dataset/data')

import os
import shutil
import random

def split_dataset(source_dir, train_dir, test_dir, test_size=0.2):
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    for class_name in os.listdir(source_dir):
        class_dir = os.path.join(source_dir, class_name)
        if os.path.isdir(class_dir):
            os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
            os.makedirs(os.path.join(test_dir, class_name), exist_ok=True)

            images = os.listdir(class_dir)
            random.shuffle(images)

            split_index = int(len(images) * test_size)

            test_images = images[:split_index]
            train_images = images[split_index:]

            for img in test_images:
                shutil.move(os.path.join(class_dir, img), os.path.join(test_dir, class_name, img))

            for img in train_images:
                shutil.move(os.path.join(class_dir, img), os.path.join(train_dir, class_name, img))

    print(f'Dataset split into {train_dir} and {test_dir}')

source_directory = '/content/stanford-dogs-dataset/images/Images'
train_directory = '/content/data/train'
test_directory = '/content/data/test'
split_dataset(source_directory, train_directory, test_directory)


train_dir='/content/data/train'
test_dir='/content/data/test'

from keras.utils import image_dataset_from_directory
train = image_dataset_from_directory(train_dir, image_size=(224, 224), batch_size=32)
test = image_dataset_from_directory(test_dir, image_size=(224, 224), batch_size=32)

from tensorflow.keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(rescale=1.0/255)
test_datagen = ImageDataGenerator(rescale=1.0/255)
train= train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

test= test_datagen.flow_from_directory(
    test_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

from tensorflow.keras.applications import InceptionV3
base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(224,224, 3))

base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
x = Dropout(0.3)(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.3)(x)
predictions = Dense(train.num_classes, activation='softmax')(x)

model = keras.models.Model(inputs=base_model.input, outputs=predictions)

model = keras.models.Model(inputs=base_model.input, outputs=predictions)
model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.Adamax(),
              metrics=['accuracy'])

model.summary()

history1= model.fit(train,
                    validation_data=test,
                    epochs=5,
                    verbose=1)

import matplotlib.pyplot as plt
plt.title('Training Log')
plt.plot(history1.history['loss'], label='Training Loss')
plt.plot(history1.history['accuracy'], label='Training Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Score')
plt.legend()
plt.show()

score1 = model.evaluate(test, verbose=2)""",

5:"""EXPERIMENT : 5                                                LINK:https://colab.research.google.com/drive/1q7iwgCXu2OQVhs6ARkxwmL9ocFkM69Op?usp=sharing
!pip install transformers datasets torch scikit-learn

!pip install transformers
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset
import torch

dataset = load_dataset("imdb")
train_data = dataset["train"].shuffle(seed=42).select(range(5000))

tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

def tokenize(example):
    return tokenizer(example["text"], truncation=True, padding="max_length", max_length=256)

train_data = train_data.map(tokenize, batched=True)
test_data = test_data.map(tokenize, batched=True)

train_data.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])
test_data.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])

model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2,
    ignore_mismatched_sizes=True
)
train_dataset = dataset["train"]
test_dataset = dataset["test"]

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=2,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    eval_strategy="epoch",
    save_strategy="no",
    report_to="none"
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_data,
    eval_dataset=test_data,
    compute_metrics=compute_metrics
)


dataset["train"] = dataset["train"].select(range(1000))
dataset["test"] = dataset["test"].select(range(500))


trainer.train()

trainer.evaluate()

eval_results = trainer.evaluate()
print("Accuracy:", eval_results["eval_accuracy"])


from transformers import DistilBertTokenizerFast
import torch
import torch.nn.functional as F

tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")


def predict_sentiment(text, model, tokenizer):
    model.eval(); device = torch.device("cuda" if torch.cuda.is_available() else "cpu"); model.to(device)
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=256).to(device)
    with torch.no_grad(): probs = torch.nn.functional.softmax(model(**inputs).logits, dim=1)
    pred = probs.argmax().item()
    return ("POSITIVE" if pred else "NEGATIVE"), round(probs[0][pred].item(), 4)


text = "This movie was absolutely terrible. I hated it."
label, confidence = predict_sentiment(text, model, tokenizer)

print(f"Review   : {text}")
print(f"Sentiment: {label} (Confidence: {confidence})")

""",

6:"""EXPERIMENT : 6                                                LINK:https://colab.research.google.com/drive/1F9MhEvLZbcPKCgUDOH09mMxoXrBUYC75?usp=sharing
import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

num_words = 10000
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=num_words)

max_len = 200
x_train = pad_sequences(x_train, maxlen=max_len)
x_test = pad_sequences(x_test, maxlen=max_len)

embedding_index = {}
embedding_dim = 100

!wget http://nlp.stanford.edu/data/glove.6B.zip

!unzip glove.6B.zip

with open("glove.6B.100d.txt", encoding='utf8') as f:
    for line in f:
        values = line.split()
        word = values[0]
        coeffs = np.asarray(values[1:], dtype='float32')
        embedding_index[word] = coeffs

word_index = imdb.get_word_index()
embedding_matrix = np.zeros((num_words, embedding_dim))

for word, i in word_index.items():
    if i < num_words:
        embedding_vector = embedding_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dropout, Dense

model = Sequential([
    Embedding(input_dim=num_words,
              output_dim=embedding_dim,
              weights=[embedding_matrix],
              input_length=max_len,
              trainable=True),

    Bidirectional(LSTM(64, return_sequences=True)),
    Dropout(0.3),

    Bidirectional(LSTM(32)),
    Dropout(0.5),

    Dense(64, activation='relu'),
    Dropout(0.4),

    Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()
model.fit(x_train, y_train, epochs=5, batch_size=128, validation_split=0.2)""",

7:"""EXPERIMENT : 7                                                LINK:https://colab.research.google.com/drive/1J1-W3961E7EidLFkg3WuIelIcK3IrTj-?usp=sharing
!pip install transformers torch nltk scikit-learn

import nltk
import numpy as np
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

import nltk
nltk.download('punkt_tab')

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def split_into_sentences(text):
    return nltk.sent_tokenize(text)

def get_bert_embeddings(sentences):
    embeddings = []
    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors='pt', max_length=512, truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        sentence_embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
        embeddings.append(sentence_embedding)
    return np.array(embeddings)

def generate_summary(document, num_sentences=3):
    sentences = split_into_sentences(document)
    if len(sentences) < num_sentences:
        return " ".join(sentences)
    embeddings = get_bert_embeddings(sentences)
    similarity_matrix = cosine_similarity(embeddings)
    sentence_scores = similarity_matrix.sum(axis=1)
    ranked_sentence_indices = sentence_scores.argsort()[-num_sentences:][::-1]
    ranked_sentence_indices.sort()
    summary_sentences = [sentences[i] for i in ranked_sentence_indices]
    return " ".join(summary_sentences)

document = ""
The rapid advancement of artificial intelligence has transformed industries worldwide. Machine learning models, such as BERT, are now pivotal in natural language processing tasks. These models require significant computational resources, often leveraging GPUs for training. Transfer learning allows pre-trained models to be fine-tuned for specific tasks like summarization. However, challenges remain, including ethical concerns and the need for large datasets. Researchers are exploring ways to make AI more efficient and accessible. The future of AI promises further innovation but requires careful regulation.
""

summary = generate_summary(document, num_sentences=3)
print("Original Document:\n", document)
print("\nSummary:\n", summary)""",

8:"""EXPERIMENT : 8                                                LINK:https://colab.research.google.com/drive/1eSVHhWRorFh2ZGGvmEcy2yu7_bgr1Uts?usp=sharing
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()

x_train = x_train.reshape(-1, 28, 28, 1) / 255.0
x_test = x_test.reshape(-1, 28, 28, 1) / 255.0

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test))

test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'\nTest Accuracy: {test_acc:.2f}')

plt.plot(history.history['accuracy'], label='train acc')
plt.plot(history.history['val_accuracy'], label='val acc')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']


import numpy as np
index = 5
img = x_test[index]

img_batch = np.expand_dims(img, axis=0)


prediction = model.predict(img_batch)
predicted_class = np.argmax(prediction)

plt.imshow(img.squeeze(), cmap='gray')
plt.title(f'Predicted: {class_names[predicted_class]}')
plt.axis('off')
plt.show()""",

9:"""EXPERIMENT : 9                                                LINK:https://drive.google.com/file/d/1N3z9TJFhOuJcNKucam3yrePTTRCU4Hmm/view?usp=sharing
!pip install resampy


import kagglehub

# Download latest version
df_path = kagglehub.dataset_download("chrisfilo/urbansound8k")

print("Path to dataset files:", df_path)

import os, numpy as np, pandas as pd, librosa, matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization
import tensorflow as tf
import librosa.display  # Required for waveshow

# Set seed for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Path to dataset folder
dataset_path = "/kaggle/input/urbansound8k"

# Load metadata
df_path = os.path.join(dataset_path, "UrbanSound8K.csv")
df = pd.read_csv(df_path)

# Display waveform of the first file in fold1
sample_row = df[df['fold'] == 1].iloc[0]
sample_file = os.path.join(dataset_path, 'fold1', sample_row['slice_file_name'])
audio, sr = librosa.load(sample_file, sr=None)

plt.figure(figsize=(10, 4))
librosa.display.waveshow(audio, sr=sr)
plt.title(f"Waveform of {sample_row['slice_file_name']} ({sample_row['class']})")
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.show()

# Extract MFCC features
def extract_mfcc(path):
    audio, sr = librosa.load(path)
    return np.mean(librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40).T, axis=0)

X, Y = [], []
for _, row in tqdm(df[df['fold'] == 1].iterrows(), total=df[df['fold'] == 1].shape[0]):
    f = os.path.join(dataset_path, 'fold1', row['slice_file_name'])
    if os.path.exists(f):
        X.append(extract_mfcc(f))
        Y.append(row['class'])

# Preprocess data
X = StandardScaler().fit_transform(X)
Y = to_categorical(LabelEncoder().fit_transform(Y))
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Build and compile model
model = Sequential([
    Dense(128, activation='relu', input_shape=(40,)), BatchNormalization(),
    Dense(64, activation='relu'), BatchNormalization(),
    Dense(32, activation='relu'), BatchNormalization(),
    Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train and evaluate
history = model.fit(X_train, Y_train, epochs=10, validation_data=(X_test, Y_test), verbose=1)
print(f"Test Accuracy: {model.evaluate(X_test, Y_test, verbose=0)[1]*100:.2f}%")

# Plot results
plt.figure(figsize=(10,4))
plt.subplot(1,2,1); plt.plot(history.history['accuracy'], label='Train')
plt.plot(history.history['val_accuracy'], label='Test'); plt.title('Accuracy'); plt.legend()
plt.subplot(1,2,2); plt.plot(history.history['loss'], label='Train')
plt.plot(history.history['val_loss'], label='Test'); plt.title('Loss'); plt.legend()
plt.tight_layout(); plt.show()
""",

10:"""EXPERIMENT : 10                                                LINK:https://colab.research.google.com/drive/1zaQRGQMy7uRO4yT6cNIlES2AaaVlwoJH?usp=sharing
# 1. Import Libraries
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, UpSampling2D, InputLayer
from tensorflow.keras.optimizers import Adam

(x_train, _), (x_test, _) = cifar10.load_data()

x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.

def rgb2gray(images):
    return np.dot(images[...,:3], [0.299, 0.587, 0.114])[..., np.newaxis]

x_train_gray = rgb2gray(x_train)
x_test_gray = rgb2gray(x_test)

x_train_gray = np.repeat(x_train_gray, 3, axis=3)
x_test_gray = np.repeat(x_test_gray, 3, axis=3)

print("Grayscale input shape:", x_train_gray.shape)
print("Color output shape:", x_train.shape)

model = Sequential()
model.add(InputLayer(input_shape=(32, 32, 3)))
model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(3, (3, 3), activation='sigmoid', padding='same'))

model.compile(optimizer=Adam(), loss='mse')

model.fit(x_train_gray, x_train, validation_data=(x_test_gray, x_test), epochs=10, batch_size=128)

preds = model.predict(x_test_gray[:10])
plt.figure(figsize=(12, 4))
for i in range(10):
    plt.subplot(3, 10, i+1)
    plt.imshow(x_test_gray[i])
    plt.axis('off')

    plt.subplot(3, 10, i+11)
    plt.imshow(preds[i])
    plt.axis('off')

    plt.subplot(3, 10, i+21)
    plt.imshow(x_test[i])
    plt.axis('off')

plt.tight_layout()
plt.show()
"""
 }