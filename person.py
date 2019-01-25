from keras.models import load_model
from PIL import Image
from scipy.misc import imresize
import numpy as np
import tensorflow as tf
import cv2

# Load the pre-trained model
# provide main_model.hdf5 / main_model_2.hdf5 for the name of model
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
    image1 = imresize(image, (224, 224)) / 255.0

    prediction = predict(image1[:, :, 0:3])
    print('##################################################################')

    prediction = imresize(prediction[:, :, 1], (image.height, image.width))
    prediction[prediction>0.5*255] = 255
    prediction[prediction<0.5*255] = 0

    transparency = np.append(np.array(image)[:, :, 0:3], prediction[: , :, None], axis=-1)
    png = Image.fromarray(transparency)

    png.save('output.png')

    print()
    print("saved the output image in output.png")
    print()
    print('##################################################################')

if __name__ == '__main__':
    main()
