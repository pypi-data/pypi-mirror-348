def run():
    import numpy as np
    import matplotlib.pyplot as plt
    import tensorflow as tf
    from tensorflow import keras
    from keras.models import Sequential
    from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    import seaborn as sns
    import os
    import pandas as pd

    os.chdir('/content/drive/MyDrive/Cars Dataset')

    train_dir = '/content/drive/MyDrive/Cars Dataset/train'
    test_dir = '/content/drive/MyDrive/Cars Dataset/test'

    from keras.utils import image_dataset_from_directory

    train_dataset = image_dataset_from_directory(train_dir, image_size=(128, 128), batch_size=32, shuffle=True)
    test_dataset = image_dataset_from_directory(test_dir, image_size=(128, 128), batch_size=32, shuffle=False)

    class_names = train_dataset.class_names
    print("\nClass names:", class_names)

    train_count = sum([len(batch[0]) for batch in train_dataset])
    test_count = sum([len(batch[0]) for batch in test_dataset])
    print(f"\nTotal training images: {train_count}")
    print(f"Total testing images: {test_count}")

    class_counts = [0] * len(class_names)
    for _, labels in train_dataset.unbatch():
        class_counts[int(labels.numpy())] += 1

    df = pd.DataFrame({'Car Class': class_names, 'Count': class_counts})
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Car Class', y='Count', data=df, palette='pastel')
    plt.title("Training Images per Car Class")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 10))
    for images, labels in train_dataset.take(1):
        for i in range(9):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            plt.title(f"Label: {class_names[labels[i]]}")
            plt.axis("off")

    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(len(class_names), activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.summary()

    logs = model.fit(train_dataset, epochs=10, validation_data=test_dataset)

    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.plot(logs.history['accuracy'], label='Train Acc')
    plt.plot(logs.history['val_accuracy'], label='Val Acc')
    plt.title('Accuracy')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(logs.history['loss'], label='Train Loss')
    plt.plot(logs.history['val_loss'], label='Val Loss')
    plt.title('Loss')
    plt.legend()
    plt.tight_layout()
    plt.show()

    y_true = np.concatenate([labels.numpy() for _, labels in test_dataset])
    y_pred = []

    for images, _ in test_dataset:
        preds = model.predict(images)
        y_pred.extend(np.argmax(preds, axis=1))

    y_pred = np.array(y_pred)

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)

    plt.figure(figsize=(10, 8))
    disp.plot(cmap=plt.cm.Blues, xticks_rotation=45)
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.show()

    test_counts = [0] * len(class_names)
    for _, labels in test_dataset.unbatch():
        test_counts[int(labels.numpy())] += 1

    for class_name, count in zip(class_names, test_counts):
        print(f"{class_name}: {count} test images")

    train_y_true = []
    train_y_pred = []

    for images, labels in train_dataset:
        preds = model.predict(images)
        train_y_pred.extend(np.argmax(preds, axis=1))
        train_y_true.extend(labels.numpy())

    cm_train = confusion_matrix(train_y_true, train_y_pred)
    disp_train = ConfusionMatrixDisplay(confusion_matrix=cm_train, display_labels=class_names)

    plt.figure(figsize=(10, 8))
    disp_train.plot(cmap=plt.cm.Oranges, xticks_rotation=45)
    plt.title("Confusion Matrix - Training Data")
    plt.tight_layout()
    plt.show()
