def tlexp(exp_number):
    if exp_number == 1:
        return '''\
# EXPERIMENT NO - 1 and also 8 (CNN)

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical

(x_train, y_train), (x_test, y_test) = cifar10.load_data()
x_train = x_train / 255.0
x_test = x_test / 255.0
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=10, batch_size=64, validation_split=0.1)
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"\\nTest Accuracy: {test_acc:.4f}")
'''
    elif exp_number == 2:
        return '''\
# EXPERIMENT NO - 2 (TRANSFER LEARNING USING VGG16)

import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras import layers, models

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
x_train_resized = tf.image.resize(x_train, (224, 224)) / 255.0
x_test_resized = tf.image.resize(x_test, (224, 224)) / 255.0
y_train_cat = tf.keras.utils.to_categorical(y_train, 10)
y_test_cat = tf.keras.utils.to_categorical(y_test, 10)

base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train_resized, y_train_cat, epochs=5, validation_data=(x_test_resized, y_test_cat))
test_loss, test_acc = model.evaluate(x_test_resized, y_test_cat)
print(f"Test Accuracy: {test_acc:.4f}")
'''
    elif exp_number==4:
        return '''\
# EXPERIMENT NO - 4(VGG16 with custom dog dataset)

import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_dir = 'dog_dataset/train'
test_dir = 'dog_dataset/test'
IMG_SIZE = 224
BATCH_SIZE = 32

train_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=20,
                                   zoom_range=0.2,
                                   horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir, target_size=(IMG_SIZE, IMG_SIZE), batch_size=BATCH_SIZE, class_mode='categorical'
)
test_generator = test_datagen.flow_from_directory(
    test_dir, target_size=(IMG_SIZE, IMG_SIZE), batch_size=BATCH_SIZE, class_mode='categorical'
)

base_model = VGG16(weights='imagenet', include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(train_generator.num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(train_generator, epochs=5, validation_data=test_generator)
loss, acc = model.evaluate(test_generator)
print(f"Test Accuracy: {acc:.4f}")
'''
    elif exp_number == 5:
        return '''\
# EXPERIMENT NO - 5 (Text Classification with Universal Sentence Encoder)

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds

train_data, test_data = tfds.load('imdb_reviews', split=['train[:80%]', 'train[80%:]'], as_supervised=True)

hub_layer = hub.KerasLayer("https://tfhub.dev/google/universal-sentence-encoder/4",
                           input_shape=[], dtype=tf.string, trainable=False)

model = tf.keras.Sequential([
    hub_layer,
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(train_data.batch(32), epochs=5, validation_data=test_data.batch(32))
loss, acc = model.evaluate(test_data.batch(32))
print(f"\\nTest Accuracy: {acc:.4f}")
'''
    elif exp_number == 9:
        return '''\
# EXPERIMENT NO - 9 (Audio Classification using MFCC features)

import os
import numpy as np
import pandas as pd
import librosa
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization

audio_dataset_path = '/content/drive/MyDrive/archive-2/audio/audio'
metadata = pd.read_csv('/content/drive/MyDrive/archive-2/esc50.csv')

def mfcc_extract(file_path):
    waveform, sample_rate = librosa.load(file_path)
    mfccs = librosa.feature.mfcc(y=waveform, sr=sample_rate, n_mfcc=50)
    return np.mean(mfccs, axis=1)

features, labels = [], []
for _, row in metadata.iterrows():
    file_path = os.path.join(audio_dataset_path, row['filename'])
    mfcc_feat = mfcc_extract(file_path)
    features.append(mfcc_feat)
    labels.append(row['take'])

X = np.array(features)
label_encoder = LabelEncoder()
Y = to_categorical(label_encoder.fit_transform(np.array(labels)))

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
num_classes = Y.shape[1]

model = Sequential([
    Dense(1024, activation='relu', input_shape=(50,)),
    BatchNormalization(),
    Dense(512, activation='relu'),
    BatchNormalization(),
    Dense(256, activation='relu'),
    BatchNormalization(),
    Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, Y_train, epochs=10, validation_data=(X_test, Y_test))
loss, accuracy = model.evaluate(X_test, Y_test)
print(f"Test accuracy: {accuracy:.4f}")

'''
    elif exp_number==10:
        return '''\
        import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import cifar10
import numpy as np

# Load and preprocess CIFAR-10
(x_train, _), (x_test, _) = cifar10.load_data()
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# Convert RGB to grayscale (input)
x_train_gray = tf.image.rgb_to_grayscale(x_train)
x_test_gray = tf.image.rgb_to_grayscale(x_test)

# Model: Autoencoder-style
def build_colorization_model():
    input_img = layers.Input(shape=(32, 32, 1))  # Grayscale input

    # Encoder
    x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(input_img)
    x = layers.MaxPooling2D((2, 2), padding='same')(x)
    x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = layers.MaxPooling2D((2, 2), padding='same')(x)

    # Decoder
    x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = layers.UpSampling2D((2, 2))(x)
    x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = layers.UpSampling2D((2, 2))(x)
    
    # Output layer with 3 channels (RGB)
    output_img = layers.Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

    model = models.Model(input_img, output_img)
    return model

# Build and compile
model = build_colorization_model()
model.compile(optimizer='adam', loss='mse')

# Train the model
model.fit(x_train_gray, x_train, epochs=10, batch_size=128, validation_split=0.1)

# Evaluate
loss = model.evaluate(x_test_gray, x_test)
print(f"Test MSE: {loss:.4f}")
'''
    elif exp_number==7:
        return '''\
        import tensorflow_hub as hub
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

# Load pre-trained Universal Sentence Encoder
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

# Document to summarize
document = """
This movie was absolutely amazing. The storyline was compelling and the actors delivered phenomenal performances.
The cinematography was beautiful and the soundtrack perfectly matched the mood.
There were some slow moments in the middle, but overall the pacing was solid.
I highly recommend it to fans of drama and emotion-heavy plots.
"""

# Sentence tokenization
sentences = sent_tokenize(document)

# Generate sentence embeddings
sentence_embeddings = embed(sentences).numpy()

# Score sentences using cosine similarity to the full document
doc_embedding = embed([document])[0].numpy()
scores = np.inner(sentence_embeddings, doc_embedding)

# Get top 3 sentences
top_n = 3
top_indices = np.argsort(scores)[-top_n:][::-1]
summary = ' '.join([sentences[i] for i in top_indices])

print("Summary:\n", summary)
'''
    elif exp_number==6:
        return '''/
        import tensorflow as tf
import numpy as np

# Load the IMDB dataset
vocab_size = 10000
max_len = 200
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.imdb.load_data(num_words=vocab_size)

# Pad the sequences
x_train = tf.keras.preprocessing.sequence.pad_sequences(x_train, maxlen=max_len)
x_test = tf.keras.preprocessing.sequence.pad_sequences(x_test, maxlen=max_len)

# Load the word index
word_index = tf.keras.datasets.imdb.get_word_index()

# Load GloVe embeddings
embedding_index = {}
with open("glove.6B.100d.txt", encoding='utf8') as f:
    for line in f:
        values = line.split()
        word = values[0]
        vector = np.asarray(values[1:], dtype='float32')
        embedding_index[word] = vector

# Create embedding matrix
embedding_dim = 100
embedding_matrix = np.zeros((vocab_size, embedding_dim))
for word, i in word_index.items():
    if i < vocab_size:
        vec = embedding_index.get(word)
        if vec is not None:
            embedding_matrix[i] = vec

# Build the model
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim,
                              weights=[embedding_matrix],
                              input_length=max_len,
                              trainable=False),  # Freeze embeddings
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')  # For binary classification
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(x_train, y_train, epochs=5, batch_size=128, validation_split=0.2)

# Evaluate the model
loss, accuracy = model.evaluate(x_test, y_test)
print(f"Test Accuracy: {accuracy:.4f}")
'''
    else:
        return "Invalid experiment number. Please choose from 1, 2, 4, 5, 7, or 9."
