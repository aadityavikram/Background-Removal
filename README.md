# Background-Removal
Background removal of an image using OpenCV and Deep Learning.

<h2> Background of images containing a person can be removed by running person.py </h2>
<p> python person.py </p>
<p> specify path of file when it outputs "Enter path of file: " </p>
<p> runs on Keras 2.0.9 </p>
<p> uses 100 layer Tiramisu neural network which was based on the DensNet. </p>
<p> pre-trained model can be downloaded at -> https://drive.google.com/open?id=1zk4j3bT1F6TZQiDsMKmEi7xB2Q6fSuHA </p>

<h2> Background of images not containing a person can be removed by running non-person.py </h2>
<p> python non-person.py </p>
<p> specify path of file when it outputs "Enter path of file: " </p>
<p> uses OpenCV </p>

<h2> Process for person.py :- </h2>
<p> 1) Loaded the pre-trained model. </p>
<p> 2) Resized the image to 224x224 as the model was taking input in the same resolution as seen from model.json file. </p>
<p> 3) Removed the transparency channel before getting predictions and resize the prediction to its original height and width. </p>
<p> 4) Pixel values above the threshold factor were converted back to 255 and below threshold were converted back to 0 to exclude out of          range pixels. </p>
<p> 5) Added back the transparency channel and converted the array back to image. </p>
<p> 6) Saved the image in png format. </p>

<h2> Process for non-person.py :- </h2>
<p> 1) Grayed the image and applied canny edge detection, erosion and dilation. </p>
<p> 2) Found the contours and filled all the contours. </p>
<p> 3) Blurred the mask after smoothing it to make the contours smooth. </p>
<p> 4) Converted the mask into 3-channel and blended it with foreground. </p>
<p> 5) Added transparency channel to the image to make background transparent. </p>
<p> 6) Saved the image in png format. </p>

<h2> Links referenced :- </h2>
<p> https://towardsdatascience.com/background-removal-with-deep-learning-c4f2104b3157 </p>
<p> https://www.youtube.com/watch?v=8-3vl71TjDs </p>
<p> https://docs.opencv.org/3.4/db/d5c/tutorial_py_bg_subtraction.html </p>
<p> http://benjamintan.io/blog/2018/05/24/making-transparent-backgrounds-with-numpy-and-opencv-in-python/ </p>
