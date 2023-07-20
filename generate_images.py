import cv2

# Load image using opencv
image_title = 'Muleta1Render2'
img = cv2.imread(f'{image_title}.png')

# # Display image
# cv2.imshow('image', img)
# cv2.waitKey(0)

extensions = ['_lg', '_md', '_placehold', '_sm', '_thumb', '_thumb@2x', '_xs', '']
resolutions = [(1999, 992), (991, 492), (230, 114), (767, 381), (535, 313), (909, 531), (575, 285), (1920, 953)]

# For each resolution, resize the image and save it
for resolution, extension in zip(resolutions, extensions):
    # Prevent the image from being distorted by cropping if necessary
    
    # Get the aspect ratio of the image
    aspect_ratio = resolution[1] / resolution[0]

    # Crop the image in order to have the required aspect ratio
    cropped = img
    if cropped.shape[0] / cropped.shape[1] > aspect_ratio:
        # The image is too tall, crop the top and bottom
        new_height = int(cropped.shape[1] * aspect_ratio)
        cropped = cropped[(cropped.shape[0] - new_height) // 2 : (cropped.shape[0] + new_height) // 2, :]
    else:
        # The image is too wide, crop the left and right
        new_width = int(cropped.shape[0] / aspect_ratio)
        cropped = cropped[:, (cropped.shape[1] - new_width) // 2 : (cropped.shape[1] + new_width) // 2]
    # Resize the image
    resized_img = cv2.resize(cropped, resolution) 
    cv2.imwrite(f'{image_title}{extension}.jpg', resized_img)