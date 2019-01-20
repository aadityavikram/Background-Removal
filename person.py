from keras.models import load_model
from PIL import Image
from scipy.misc import imresize
import numpy as np
import tensorflow as tf
import cv2

# Load the pre-trained model
model = load_model('main_model.hdf5', compile=False)

graph = tf.get_default_graph()

def predict(image):
    with graph.as_default():
        # Make prediction
        prediction = model.predict(image[None, :, :, :])
    prediction = prediction.reshape((224,224, -1))
    return prediction

def main():
    print()
    print('##################################################################')
    print()
    path = input('Enter path of file: ')
    print()
    print('##################################################################')
    print()
    print("Removing background...")
    print()
    image = Image.open(path)
    resized_image = imresize(image, (224, 224)) / 255.0

    # Model input shape = (224,224,3)
    # [0:3] - Take only the first 3 RGB channels and drop ALPHA 4th channel in case this is a PNG
    prediction = predict(resized_image[:, :, 0:3])
    print('##################################################################')

    # Resize back to original image size
    # [:, :, 1] = Take predicted class 1 - currently in our model = Person class. Class 0 = Background
    prediction = imresize(prediction[:, :, 1], (image.height, image.width))
    prediction[prediction>0.5*255] = 255
    prediction[prediction<0.5*255] = 0

    # Append transparency 4th channel to the 3 RGB image channels.
    transparent_image = np.append(np.array(image)[:, :, 0:3], prediction[: , :, None], axis=-1)
    transparent_image = Image.fromarray(transparent_image)

    new_image = transparent_image

    new_image.save('output.png')

    print()
    print("saved the output image in output.png")
    print()
    print('##################################################################')

if __name__ == '__main__':
    main()