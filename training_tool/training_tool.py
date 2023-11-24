from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,classification_report
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
import tensorflow as tf
from tqdm import tqdm
import numpy as np
import itertools 
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import itertools



def load_data(data_path, label):

    x_train = [] # training images.
    y_train  = [] # training labels.
    x_test = [] # testing images.
    y_test = [] # testing labels.

    image_size = 200

    for label in label:
        trainPath = os.path.join(data_path, 'Training',label)
        for file in tqdm(os.listdir(trainPath)):
            image = cv2.imread(os.path.join(trainPath, file),0) # load images in gray.
            image = cv2.bilateralFilter(image, 2, 50, 50) # remove images noise.
            image = cv2.applyColorMap(image, cv2.COLORMAP_BONE) # produce a pseudocolored image.
            image = cv2.resize(image, (image_size, image_size)) # resize images into 150*150.
            x_train.append(image)
            y_train.append(label.index(label))
        
        testPath = os.path.join(data_path, 'Testing',label)
        for file in tqdm(os.listdir(testPath)):
            image = cv2.imread(os.path.join(testPath, file),0)
            image = cv2.bilateralFilter(image, 2, 50, 50)
            image = cv2.applyColorMap(image, cv2.COLORMAP_BONE)
            image = cv2.resize(image, (image_size, image_size))
            x_test.append(image)
            y_test.append(label.index(label))


    x_train = np.array(x_train) / 255.0 # normalize Images into range 0 to 1.
    x_test = np.array(x_test) / 255.0

    print(x_train.shape)
    print(x_test.shape)

    images = [x_train[i] for i in range(15)]
    fig, axes = plt.subplots(3, 5, figsize = (10, 10))
    axes = axes.flatten()
    for img, ax in zip(images, axes):
        ax.imshow(img)
    plt.tight_layout()
    plt.show()


    x_train, y_train = shuffle(x_train,y_train, random_state=42) 

    y_train = tf.keras.utils.to_categorical(y_train) #One Hot Encoding on the labels
    y_test = tf.keras.utils.to_categorical(y_test)

    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, random_state=42) #Dividing the dataset into Training and Validation sets.

    print(x_val.shape)

    return x_train, x_val, x_test, y_train, y_val, y_test


def plot_confusion_matrix(cm,
                          target_names,
                          title='Confusion matrix',
                          cmap=None,
                          normalize=True):
    
    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")


    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.show()



def draw_curve(history):

    plt.figure(figsize=[8,6])
    plt.plot(history.history['loss'],'r',linewidth=3.0)
    plt.plot(history.history['val_loss'],'b',linewidth=3.0)
    plt.legend(['Training loss', 'Validation Loss'],fontsize=18)
    plt.xlabel('Epochs ',fontsize=16)
    plt.ylabel('Loss',fontsize=16)
    plt.title('Loss Curves',fontsize=16)
    plt.show()

    #Plot the Accuracy Curves
    plt.figure(figsize=[8,6])
    plt.plot(history.history['accuracy'],'r',linewidth=3.0)
    plt.plot(history.history['val_accuracy'],'b',linewidth=3.0)
    plt.legend(['Training Accuracy', 'Validation Accuracy'],fontsize=18)
    plt.xlabel('Epochs ',fontsize=16)
    plt.ylabel('Accuracy',fontsize=16)
    plt.title('Accuracy Curves',fontsize=16)   
    plt.show()


def draw_matrix(label, y_test_new, pred, acc):
    
    print("Test Accuracy: ",np.round(acc*100,2))
    print(classification_report(y_test_new,pred,target_names = label,digits = 4))
    confusion_mtx = confusion_matrix(y_test_new,pred)
    cm = plot_confusion_matrix(confusion_mtx, target_names = label, normalize=False)