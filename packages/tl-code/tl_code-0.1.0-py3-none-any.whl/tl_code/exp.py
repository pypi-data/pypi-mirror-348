experiment = {

    1:"""


    EXPERIMENT : 1                                                LINK:https://colab.research.google.com/drive/1yrARAgdLPlD7pVokK9NZMSwovNTvRrLC?usp=sharing
    ---------------------------------------------------------------------------------------------------------------------------------------------------------
    import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import matplotlib.pyplot as plt

data_dir = "/content/drive/MyDrive/CAT VS DOG"
dog_dir = os.path.join(data_dir, 'dog')
cat_dir = os.path.join(data_dir, 'cat')

data_gen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
train_gen = data_gen.flow_from_directory(
    data_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    subset='training')

val_gen = data_gen.flow_from_directory(
    data_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    subset='validation')

def build_simple_cnn():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

simple_cnn = build_simple_cnn()
history_simple = simple_cnn.fit(train_gen, epochs=4, validation_data=val_gen, verbose=1)

# After training, print the accuracy for each epoch
print("Training Accuracy:", history_simple.history['accuracy'])
print("Validation Accuracy:", history_simple.history['val_accuracy'])

def plot_history(history, title):
    plt.figure(figsize=(12, 4))

    # Accuracy plot
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title(f'{title} - Accuracy')
    plt.legend()

    # Loss plot
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title(f'{title} - Loss')
    plt.legend()

    plt.show()

plot_history(history_simple, "Simple CNN")
# Hyperparameter tuning
from sklearn.model_selection import ParameterGrid

def build_model(conv_layers, dense_units, dropout_rate, learning_rate):
    model = Sequential()

    for _ in range(conv_layers):
        model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)))
        model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())

    model.add(Dense(dense_units, activation='relu'))
    model.add(Dropout(dropout_rate))

    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

param_grid = {
    'conv_layers': [1, 2],
    'dense_units': [64, 128],
    'dropout_rate': [0.3, 0.5],
    'learning_rate': [0.001, 0.0001]
}

results = []
grid = ParameterGrid(param_grid)
for params in grid:
    print(f"Training with parameters: {params}")
    model = build_model(**params)
    history = model.fit(train_gen, epochs=4, validation_data=val_gen, verbose=1)

    val_loss, val_accuracy = model.evaluate(val_gen, verbose=0)
    results.append({
        'params': params,
        'val_loss': val_loss,
        'val_accuracy': val_accuracy
    })

    plot_history(history, f"Hyperparameter: {params}")
results = sorted(results, key=lambda x: x['val_accuracy'], reverse=True)

for result in results:
    print(f"Parameters: {result['params']}, Validation Accuracy: {result['val_accuracy']:.4f}, Validation Loss: {result['val_loss']:.4f}")



"""
,
2: """

    EXPERIMENT :2                                                LINK:https://colab.research.google.com/drive/1fQsdjcbeTczV3ArsImh13-EZB7jmFLj8?usp=sharing
    ---------------------------------------------------------------------------------------------------------------------------------------------------------
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


data='/content/drive/MyDrive/horse-or-human'
train_dir = '/content/drive/MyDrive/horse-or-human/train'
test_dir = '/content/drive/MyDrive/horse-or-human/validation'


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
y_true = np.concatenate([y for x, y in test_dataset], axis=0)

cm = confusion_matrix(y_true, y_pred_classes)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

print('Classification Report')
print(classification_report(y_true, y_pred_classes))


"""
,
3: """


    EXPERIMENT :3                                               LINK:https://colab.research.google.com/drive/1BgKFBZJHA01MuL5emcrqgaP1tnZLFOAk?usp=sharing
    ---------------------------------------------------------------------------------------------------------------------------------------------------------
    import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.layers import Conv2D,BatchNormalization,MaxPooling2D,GlobalMaxPooling2D,Dense,Dropout
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
    GlobalMaxPooling2D(),
    BatchNormalization(),
    layers.Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(256, activation='relu'),
    Dropout(0.4),
    Dense(10, activation='softmax')
])

model.compile(loss='categorical_crossentropy',optimizer='Adam',metrics=['accuracy'])
model.summary()
from keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(monitor='val_loss',patience=5,restore_best_weights=True)
his = model.fit(x_train,y_train,validation_split=0.3,batch_size=32,epochs=20,callbacks=[early_stopping])
res = model.evaluate(x_test,y_test)[1]*100
print("Score : ",res)


"""
,
4:"""
    EXPERIMENT :4                                             LINK:https://colab.research.google.com/drive/16dvf7CRPuQ7IkIdZ79y45ydJUapP-ixf?usp=sharing
    ---------------------------------------------------------------------------------------------------------------------------------------------------------
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
    # Create directories if they don't exist
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    # Iterate over each class directory
    for class_name in os.listdir(source_dir):
        class_dir = os.path.join(source_dir, class_name)
        if os.path.isdir(class_dir):
            # Create class directories in train and test directories
            os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
            os.makedirs(os.path.join(test_dir, class_name), exist_ok=True)

            # Get list of images
            images = os.listdir(class_dir)
            random.shuffle(images)

            # Calculate split index
            split_index = int(len(images) * test_size)

            # Split images into training and test sets
            test_images = images[:split_index]
            train_images = images[split_index:]

            # Move images to train and test directories
            for img in test_images:
                shutil.move(os.path.join(class_dir, img), os.path.join(test_dir, class_name, img))

            for img in train_images:
                shutil.move(os.path.join(class_dir, img), os.path.join(train_dir, class_name, img))

    print(f'Dataset split into {train_dir} and {test_dir}')

# Example usage
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
score1 = model.evaluate(test, verbose=2)

""",

5:"""
    EXPERIMENT :5                                             LINK:https://colab.research.google.com/drive/1hg1vMNZrk_PFVNDOSHxxSk0ZcRuPWdb0?usp=sharing
    ---------------------------------------------------------------------------------------------------------------------------------------------------------
    import pandas as pd
import re
import string
import collections
import matplotlib.pyplot as plt

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, SnowballStemmer

import tensorflow as tf
from tensorflow.keras.layers import Embedding, Dense, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd

df_train = pd.read_csv('/content/drive/MyDrive/TL Lab/Train.csv')
df_test = pd.read_csv('/content/drive/MyDrive/TL Lab/Test.csv')
df_train.head()

df_train.info()
print(df_train['label'].value_counts())
print(df_test['label'].value_counts())

import numpy as np
average_len = np.mean([len(item) for item in df_train['text']])
print("Average Length of Text in Training Dataset:", average_len)
max_len = int(average_len + 100)
from tensorflow.keras.preprocessing.text import Tokenizer

tokenizer = Tokenizer(num_words=10_000, oov_token='<OOV>')
tokenizer.fit_on_texts(df_train['text'])

train_seq = tokenizer.texts_to_sequences(df_train['text'])
test_seq = tokenizer.texts_to_sequences(df_test['text'])
train_pad = pad_sequences(train_seq , maxlen = max_len )
test_pad = pad_sequences(test_seq , maxlen = max_len )
from tensorflow.keras.utils import to_categorical

train_label = to_categorical(df_train['label'])
test_label = to_categorical(df_test['label'])
y_train = df_train['label'].values
y_train
import tensorflow as tf

model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(10_000, 16),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32, return_sequences=True)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(loss=tf.keras.losses.binary_crossentropy, optimizer=optimizer, metrics=['accuracy'])
import numpy as np

# Convert padded sequences to NumPy arrays
train_pad_np = np.array(train_pad)
test_pad_np = np.array(test_pad)
print(type(train_seq), type(y_train))
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

max_length = 100
train_seq_padded = pad_sequences(train_seq, maxlen=max_length, padding='post')

train_seq_np = np.array(train_seq_padded)

y_train_np = np.array(y_train)

print(train_seq_np.shape, y_train_np.shape)
from tensorflow.keras.callbacks import EarlyStopping

# Define EarlyStopping callback
early_stopping = EarlyStopping(monitor='val_accuracy', patience=3, restore_best_weights=True)

# Train the model with EarlyStopping
history = model.fit(train_seq_np, y_train_np, epochs=10, batch_size=64, validation_split=0.1, callbacks=[early_stopping])
plt.style.use('dark_background')
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])

plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Training', 'Validation'], loc='upper right')
plt.show()
plt.style.use('dark_background')
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])

plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Training', 'Validation'], loc='lower right')
plt.show()
import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

max_length = 100
test_seq_padded = pad_sequences(test_seq, maxlen=max_length, padding='post')

test_seq_np = np.array(test_seq_padded)

predictions = model.predict(test_seq_np)

predicted_labels = np.round(predictions)
true_labels = np.array(df_test['label'])

cm = confusion_matrix(true_labels, predicted_labels)

plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", annot_kws={"size": 16})
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tabulate import tabulate

max_length = 100
test_seq_padded = pad_sequences(test_seq, maxlen=max_length, padding='post')

test_seq_np = np.array(test_seq_padded)

predictions = model.predict(test_seq_np)

predicted_labels = np.round(predictions)
true_labels = np.array(df_test['label'])

accuracy = accuracy_score(true_labels, predicted_labels)
precision = precision_score(true_labels, predicted_labels)
recall = recall_score(true_labels, predicted_labels)
f1 = f1_score(true_labels, predicted_labels)

table = [
    ["Accuracy", accuracy],
    ["Precision", precision],
    ["Recall", recall],
    ["F1-score", f1]
]

print(tabulate(table, headers=["Metric", "Value"], tablefmt="fancy_grid"))
# Function to predict a single input string
def predict_sentiment(text, tokenizer, model, max_length=100):
    # Convert text to sequence
    seq = tokenizer.texts_to_sequences([text])
    # Pad the sequence
    padded_seq = pad_sequences(seq, maxlen=max_length, padding='post')
    # Predict
    pred = model.predict(padded_seq)
    # Round to get 0 or 1
    label = int(np.round(pred[0][0]))
    sentiment = "Positive" if label == 1 else "Negative"
    print(f"Input: {text}")
    print(f"Predicted Sentiment: {sentiment} ({label})")

# Example usage
sample_text = "I really enjoyed the experience!"
predict_sentiment(sample_text, tokenizer, model)


"""
,

6:
"""
EXPERIMENT :6  
LINK: https://colab.research.google.com/drive/1tkvsXHzxWXCqUKWjEyKat2U4UJRCB5sk?usp=sharing
----------------------------------------------------------------------------------------------------

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Input, Dense, Embedding, MultiHeadAttention, LayerNormalization, Dropout, GlobalAveragePooling1D, LSTM, Bidirectional, GlobalMaxPooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nltk
from nltk.tokenize import sent_tokenize
import re
from tensorflow.keras.initializers import Constant
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

nltk.download('punkt')

# Ensure latest numpy and gensim
!pip install --upgrade --force-reinstall numpy gensim

from gensim.models import FastText

TODO:eroor

# Load IMDB data
def load_imdb_data():
    imdb, info = tfds.load('imdb_reviews', with_info=True, as_supervised=True)

    train_data = imdb['train']
    train_sentences, train_labels = [], []
    for sentence, label in tfds.as_numpy(train_data):
        train_sentences.append(clean_text(sentence.decode('utf-8')))
        train_labels.append(int(label))

    test_data = imdb['test']
    test_sentences, test_labels = [], []
    for sentence, label in tfds.as_numpy(test_data):
        test_sentences.append(clean_text(sentence.decode('utf-8')))
        test_labels.append(int(label))

    return train_sentences, train_labels, test_sentences, test_labels

# Fetch and preprocess IMDB data
train_sentences, train_labels, test_sentences, test_labels = load_imdb_data()

# Parameters
max_len = 100
embedding_dim = 128
max_words = 10000

# Tokenizer
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(train_sentences)

# Tokenize for FastText
tokenized_sentences = [sentence.split() for sentence in train_sentences]

# Train FastText model using CBOW
fasttext_model = FastText(sentences=tokenized_sentences, vector_size=embedding_dim, window=5, min_count=1, sg=0)

# Create embedding matrix
word_index = tokenizer.word_index
embedding_matrix = np.zeros((max_words, embedding_dim))

for word, i in word_index.items():
    if i < max_words:
        if word in fasttext_model.wv:
            embedding_matrix[i] = fasttext_model.wv[word]

# Prepare padded sequences
train_sequences = tokenizer.texts_to_sequences(train_sentences)
train_padded = pad_sequences(train_sequences, maxlen=max_len, padding='post')
train_labels = np.array(train_labels)

# Build the model
model = Sequential()
model.add(Embedding(max_words, embedding_dim, embeddings_initializer=Constant(embedding_matrix), input_length=max_len, trainable=False))
model.add(Bidirectional(LSTM(64, return_sequences=True)))
model.add(GlobalMaxPooling1D())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train-validation split
X_train, X_val, y_train, y_val = train_test_split(train_padded, train_labels, test_size=0.2, random_state=42)

# Train the model
history = model.fit(X_train, y_train, epochs=10, batch_size=128, validation_data=(X_val, y_val), verbose=1)

# Plot training metrics
def plot_metrics(history):
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='train accuracy')
    plt.plot(history.history['val_accuracy'], label='val accuracy')
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='train loss')
    plt.plot(history.history['val_loss'], label='val loss')
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend()

    plt.tight_layout()
    plt.show()

plot_metrics(history)

# Prepare test data
test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = pad_sequences(test_sequences, maxlen=max_len, padding='post', truncating='post')

# Predict and evaluate
y_pred = (model.predict(test_padded) > 0.5).astype("int32")
print(classification_report(test_labels, y_pred))
"""

,

7:
"""
EXPERIMENT :7
LINK: https://colab.research.google.com/drive/1AwgVwCYSkzdwYV7bsXBGm065zoMt_C3c?usp=sharing
----------------------------------------------------------------------------------------------------

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Input, Dense, Embedding, Bidirectional, LSTM, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nltk
from nltk.tokenize import sent_tokenize
import re

nltk.download('punkt')

TODO:eroor

def load_imdb_data():
    imdb, info = tfds.load('imdb_reviews', with_info=True, as_supervised=True)
    train_data = imdb['train']
    train_sentences, train_labels = [], []

    for sentence, label in tfds.as_numpy(train_data):
        train_sentences.append(clean_text(sentence.decode('utf-8')))
        train_labels.append(int(label))

    return train_sentences, train_labels

def summarize_document(document, model, tokenizer, max_len, top_n=3):
    sentences = sent_tokenize(document)
    sequence_data = tokenizer.texts_to_sequences(sentences)
    padded_sequences = pad_sequences(sequence_data, maxlen=max_len, padding='post')

    predictions = model.predict(padded_sequences)
    sentence_scores = [(index, score) for index, score in enumerate(predictions)]
    top_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:top_n]

    summary = [sentences[i] for i, _ in top_sentences]
    return ' '.join(summary)

# Load IMDB data
train_sentences, train_labels = load_imdb_data()

# Define parameters
max_len = 100
embedding_dim = 128
max_words = 10000

# Tokenizer for Keras
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(train_sentences)

# Prepare training data
train_sequences = tokenizer.texts_to_sequences(train_sentences)
train_padded = pad_sequences(train_sequences, maxlen=max_len, padding='post')

# Build and train the model
model = Sequential([
    Embedding(max_words, embedding_dim, input_length=max_len),
    Bidirectional(LSTM(64, return_sequences=True)),
    GlobalAveragePooling1D(),
    Dense(24, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
num_epochs = 5
model.fit(train_padded, np.array(train_labels), epochs=num_epochs, validation_split=0.2)

# Save and reload the model
model.save("/content/drive/MyDrive/Temp/imdb_model.h5")
imdb_model = tf.keras.models.load_model('/content/drive/MyDrive/Temp/imdb_model.h5')

for layer in imdb_model.layers:
    layer.trainable = False

# Build the summarization model
inputs = Input(shape=(max_len,))
x = imdb_model(inputs)
x = Dense(64, activation='relu')(x)
x = Dense(32, activation='relu')(x)
x = Dense(1, activation='sigmoid')(x)

summarization_model = Model(inputs=inputs, outputs=x)
summarization_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
summarization_model.summary()

# Fallback sentence tokenizer (without NLTK)
def simple_sent_tokenize(text):
    return text.split('. ')

# Sample document
example_document = (
    "This movie was fantastic! I loved the plot and the acting was superb. "
    "However, I felt that the ending was a bit rushed. The cinematography was stunning, "
    "and the music added a wonderful depth to the scenes. The character development was rich, "
    "and I appreciated how the film tackled complex themes. I found myself emotionally invested "
    "in the characters and their journeys. There were moments of humor that broke the tension, "
    "which I enjoyed. Overall, it was an enjoyable experience, but it could have been more impactful "
    "if the pacing had been better. I would recommend this film to anyone who loves a good story. "
    "It provided a perfect mix of humor and drama, and I think it will resonate well with many audiences. "
    "The performances were not only entertaining but also very moving, capturing the essence of the story."
)

# Summarizer using simple tokenizer
def summarize_document(text):
    sentences = simple_sent_tokenize(text)
    summary = '. '.join(sentences[:3]) + '.'
    return summary

summary = summarize_document(example_document)
print("Summary:")
print(summary)
"""
,

8:"""
    EXPERIMENT :8                                             LINK:https://colab.research.google.com/drive/1mayYAKyZZ5YohvcBdYxVnAxhIfGo6zjb?usp=sharing
    ---------------------------------------------------------------------------------------------------------------------------------------------------------
pip install tensorflow numpy matplotlib scikit-learn
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16, ResNet50, InceptionV3
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    '/content/drive/MyDrive/archive (1)/Planets_Moons_Data/Planets and Moons',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    '/content/drive/MyDrive/archive (1)/Planets_Moons_Data/Planets and Moons',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))


for layer in base_model.layers:
    layer.trainable = False

x = Flatten()(base_model.output)
x = Dense(512, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(11, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=x)

model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

history = model.fit(
    train_generator,
    epochs=50,
    validation_data=validation_generator,
    callbacks=[early_stopping]
)

# Plot training & validation accuracy values
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()
""",

9:"""

    EXPERIMENT :9                                             LINK:https://colab.research.google.com/drive/1sGHQ5k0mDvW0Bt-pNILapv06fCWl2_I_?usp=sharing
    ---------------------------------------------------------------------------------------------------------------------------------------------------------

import pandas as pd
metadata= pd.read_csv('/content/drive/MyDrive/archive-2/esc50.csv')
metadata.head(15)
#checking dataset
metadata['take'].value_counts()
from google.colab import drive
drive.mount('/content/drive')
#read a sample audio using librosa
import librosa
audio_file_path='/content/drive/MyDrive/archive-2/audio/audio/1-100032-A-0.wav'
librosa_audio_data,librosa_sample_rate=librosa.load(audio_file_path)
print(librosa_audio_data)
#plotting the librosa audio data
import matplotlib.pyplot as plt
plt.figure(figsize=(15, 5))   # Original audio with 1 channel
plt.plot(librosa_audio_data)
from scipy.io import wavfile as wav  #Performing the same process wid scipy
wave_sample_rate, wave_audio = wav.read(audio_file_path)
wave_audio
import matplotlib.pyplot as plt


plt.figure(figsize=(15, 5)) # Original audio with 2 channels
plt.plot(wave_audio)
# Importing necessary libraries againd

# Data preprocessing
import pandas as pd
import numpy as np
import os, librosa
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Visualization
import IPython.display as ipd
import matplotlib.pyplot as plt
import seaborn as sns

# Model
from tensorflow import keras
from keras.utils import to_categorical
from keras import layers, Sequential
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.layers import Conv2D, MaxPooling2D,BatchNormalization

# Metrics
from sklearn.metrics import confusion_matrix

# Suppressing warnings
from warnings import filterwarnings
filterwarnings('ignore')
mfccs = librosa.feature.mfcc(y=librosa_audio_data, sr=librosa_sample_rate, n_mfcc=40)
print(mfccs.shape)
mfccs
#for all the files we will be performing it in following manner
import pandas as pd
import os
import librosa

audio_dataset_path = '/content/drive/MyDrive/archive-2/audio/audio'
metadata =  pd.read_csv('/content/drive/MyDrive/archive-2/esc50.csv')
metadata.head()
# Computing Mel-frequency cepstral coefficients
def mfccExtract(file):
    # Loading audio file
    waveform, sampleRate = librosa.load(file_name)

    features = librosa.feature.mfcc(y = waveform, sr = sampleRate, n_mfcc = 50)
    return np.mean(features, axis = 1)

extractAll = []

import numpy as np
from tqdm import tqdm
# Iterating through each row
for index_num, row in tqdm(metadata.iterrows()):

    file_name = os.path.join(audio_dataset_path,  row['filename'])

    features = mfccExtract(file_name)
    extractAll.append([features, row['take']])
featuresDf = pd.DataFrame(extractAll, columns = ['Features', 'take'])
featuresDf.head()
### Split the dataset into independent and dependent dataset
X=np.array(featuresDf['Features'].tolist())
Y=np.array(featuresDf['take'].tolist())
X.shape
Y
### Label Encoding
###y=np.array(pd.get_dummies(y))
### Label Encoder
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
labelencoder=LabelEncoder()
Y=to_categorical(labelencoder.fit_transform(Y))
Y
### Train Test Split
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=0)
X_train
X_train.shape
X_test.shape
Y_train.shape
### No of classes
num_labels=Y.shape[1]
### No of classes
num_labels=Y.shape[1]
# %%
model = Sequential([
    layers.Dense(1024, activation = 'relu', input_shape = (50,)), #above we have kept the value of features as 50
    layers.BatchNormalization(), #first layer

    layers.Dense(512, activation = 'relu'),
    layers.BatchNormalization(),

    layers.Dense(256, activation = 'relu'),
    layers.BatchNormalization(),

    layers.Dense(128, activation = 'relu'),
    layers.BatchNormalization(),

    layers.Dense(64, activation = 'relu'),
    layers.BatchNormalization(),

    layers.Dense(32, activation = 'relu'),
    layers.BatchNormalization(),

    layers.Dense(num_labels, activation = 'softmax') # Change to num_labels instead of 10
])
model.compile(loss='categorical_crossentropy',metrics=['accuracy'],optimizer='adam')
model.summary()
history = model.fit(X_train, Y_train, validation_data = (X_test, Y_test), epochs = 10)
test_accuracy=model.evaluate(X_test,Y_test,verbose=0)
print(test_accuracy[1])
historyDf = pd.DataFrame(history.history)
# Plotting training and validation loss
historyDf.loc[:, ['loss', 'val_loss']].plot()
# Plotting training and validation accuracy
historyDf.loc[:, ['accuracy', 'val_accuracy']].plot()
# Evaluating model
score = model.evaluate(X_test, Y_test)[1] * 100
print(f'Validation accuracy of model : {score:.2f}%')


""",

10:"""
    EXPERIMENT :10                                             LINK:https://colab.research.google.com/drive/1HlyXyCN7Asv5Q3dXpEw7urCk9EOZv_qp?usp=sharing
    ---------------------------------------------------------------------------------------------------------------------------------------------------------
    from google.colab import files
files.upload()
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!pip install -q kaggle

!kaggle datasets download -d aayush9753/image-colorization-dataset

!unzip image-colorization-dataset.zip

!pip install opencv-python

pip install tensorflow
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, UpSampling2D, concatenate, Lambda
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input

train_gray_dir = '/content/data/train_black'
train_color_dir = '/content/data/train_color'
test_gray_dir = '/content/data/test_black'
test_color_dir = '/content/data/test_color'
def load_images(gray_path, color_path, img_size=224, max_images=None):
    "
    Loads and preprocesses grayscale and corresponding color images.

    Parameters:
        gray_path (str): Directory path for grayscale images.
        color_path (str): Directory path for color images.
        img_size (int): Target image size (img_size x img_size).
        max_images (int, optional): Max number of images to load. If None, loads all.

    Returns:
        Tuple (gray_images, color_images): NumPy arrays of grayscale and color images.
    "
    gray_images = []
    color_images = []

    files = sorted(os.listdir(gray_path))  # ensure consistent ordering
    if max_images is not None:
        files = files[:max_images]

    for file in tqdm(files, desc=f"Loading from {os.path.basename(gray_path)}"):
        try:
            # Load and process grayscale image
            gray = cv2.imread(os.path.join(gray_path, file), cv2.IMREAD_GRAYSCALE)
            gray = cv2.resize(gray, (img_size, img_size))
            gray = gray.astype('float32') / 255.0
            gray = np.expand_dims(gray, axis=-1)

            # Load and process color image
            color = cv2.imread(os.path.join(color_path, file))
            color = cv2.resize(color, (img_size, img_size))
            color = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            color = color.astype('float32') / 255.0

            gray_images.append(gray)
            color_images.append(color)
        except Exception as e:
            print(f"Skipped {file} due to error: {e}")

    return np.array(gray_images), np.array(color_images)

IMAGE_SIZE = 224 # Assuming 224x224 image size, change if needed
gray_train, color_train = load_images(train_gray_dir, train_color_dir)
gray_test, color_test = load_images(test_gray_dir, test_color_dir)

X_train, X_val, y_train, y_val = train_test_split(gray_train, color_train, test_size=0.1)

def repeat_gray_to_rgb(x):
    return tf.image.grayscale_to_rgb(x)

# Build the model using VGG16 as feature extractor
def build_model(input_shape=(224, 224, 1)):
    # Grayscale input
    gray_input = Input(shape=input_shape)

    # Convert grayscale to RGB (VGG expects 3 channels)
    rgb_input = Lambda(repeat_gray_to_rgb)(gray_input)

    # Load pretrained VGG16 model (no top)
    vgg = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    vgg.trainable = False  # freeze VGG weights

    # Extract features using VGG16
    features = vgg(rgb_input)

    # Decoder: Upsample back to 224×224×3
    x = UpSampling2D((2, 2))(features)    # 7 → 14
    x = Conv2D(256, (3, 3), activation='relu', padding='same')(x)

    x = UpSampling2D((2, 2))(x)           # 14 → 28
    x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)

    x = UpSampling2D((2, 2))(x)           # 28 → 56
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)

    x = UpSampling2D((2, 2))(x)           # 56 → 112
    x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)

    x = UpSampling2D((2, 2))(x)           # 112 → 224
    output = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

    model = Model(inputs=gray_input, outputs=output)
    model.compile(optimizer='adam', loss='mse')

    return model

model = build_model()
model.summary()

# Train model
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=1,
    batch_size=16
)

# Evaluate
loss = model.evaluate(gray_test, color_test)
print("Test Loss:", loss)

# Show predictions
def show_predictions(model, gray_images, color_images, num=5):
    preds = model.predict(gray_images[:num])

    for i in range(num):
        fig, axs = plt.subplots(1, 3, figsize=(12, 4))
        axs[0].imshow(gray_images[i].squeeze(), cmap='gray')
        axs[0].set_title("Grayscale Input")
        axs[1].imshow(color_images[i])
        axs[1].set_title("Ground Truth")
        axs[2].imshow(preds[i])
        axs[2].set_title("Predicted Colorization")
        for ax in axs:
            ax.axis('off')
        plt.tight_layout()
        plt.show()

show_predictions(model, gray_test, color_test)
!pip install oPENcv2

"""
}

