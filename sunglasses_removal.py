import os
import glob
import cv2
import numpy as np
from PIL import Image, ImageChops

print('#### The dataset folder should be in the same directory as this python file ####')
print()
s=input('Enter name of dataset directory -> ')

train_path = s
train_labels = os.listdir(train_path)

output_path = "trained"
if os.path.exists(output_path)==False:
	os.system("mkdir " + output_path)

idx1=idx2=0

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

# loop over all the labels in the folder
count = 1
for i, label in enumerate(train_labels):
	cur_path = train_path + "\\" + label
	for e in [cur_path + "\\*.jpg",cur_path + "\\*.png"]:
		for image_path in glob.glob(e):
			name=""
			
			# print(image_path)
			for i in range(len(image_path)-1,0,-1):
				if image_path[i]=='.':
					idx2=i+1
				if image_path[i]=='\\':
					idx1=i+1
					break

			for i in range(idx1,idx2-1):
				name=name+image_path[i]
			
			img = cv2.imread(image_path)

			# changing the contrast of image
			new_image = np.zeros(img.shape, img.dtype)
			alpha = 1.1  # contrast control
			beta = 10    # brightness control
			for y in range(img.shape[0]):
				for x in range(img.shape[1]):
					for c in range(img.shape[2]):
						new_image[y,x,c] = np.clip(alpha*img[y,x,c] + beta, 0, 255)

			img=new_image


			gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			blurred = cv2.GaussianBlur(img, (9, 9), 0)

			# Edge detection 
			edges = cv2.Canny(gray, 100, 200)
			edges = cv2.dilate(edges, None)
			edges = cv2.erode(edges, None)

			# Find contours in edges, sort by area 
			contour_info = []
			contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
			for c in contours:
				contour_info.append((
					c,
					cv2.isContourConvex(c),
					cv2.contourArea(c),
				))
			contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
			max_contour = contour_info[0]

			# Create empty mask and flood fill
			mask = np.zeros(edges.shape)
			for c in contour_info:
				cv2.fillConvexPoly(mask, c[0], (255))

			# Smooth mask and blur it
			mask = cv2.dilate(mask, None, iterations=10)
			mask = cv2.erode(mask, None, iterations=10)
			mask = cv2.GaussianBlur(mask, (21, 21), 0)

			# Create 3-channel alpha mask
			mask_stack = np.dstack([mask]*3)

			# Blend mask and foreground image
			mask_stack  = mask_stack.astype('float32') / 255.0  
			img         = img.astype('float32') / 255.0    
			masked = (mask_stack * img) + ((1-mask_stack) * (1.0,1.0,1.0))
			masked = (masked * 255).astype('uint8')                    

			# Make the background transparent by adding 4th alpha channel
			tmp = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
			_,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
			b, g, r = cv2.split(masked)
			rgba = [b,g,r, alpha]
			dst = cv2.merge(rgba,4)

			final_output_path = output_path + "\\" + label

			if os.path.exists(final_output_path)==False:
				os.system("mkdir " + final_output_path)

			cv2.imwrite(final_output_path + "\\" + name + ".png",dst)
			im = Image.open(final_output_path + "\\" + name + ".png")
			im = trim(im)
			im.save(final_output_path + "\\" + name + ".png")
			#print(im.width,im.height)
			print("Saved Image %s.png"%count)
			count += 1