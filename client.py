"""
You'll only need this client to test your server. Other than that it won't be necessary since in practice your server
will be deployed in a pipeline.
"""


"""CMD Command : python client.py 1 directorypath filename"""

#instance.attribut

# Required imports
from urllib import request
import grpc
import component_pb2
import component_pb2_grpc
import cv2
import scipy.io
import numpy as np 
import tqdm 
import sys
import os 
# Optional but useful imports


dic = {}
i = 0
videotoimage = []
matrix = []
keypoints =[]
poses = []
video = 'C:\\Users\\Mathieu\\Desktop\\Stage_Lisbonne\\Videos\\videotest.mp4'

# Function to convert the video into a list of images
# Returns the number of frames of the video 
# fills frames_list with the path of all frames
def vidtoimg(videopath) : 
    vidcap = cv2.VideoCapture(videopath)
    success,image = vidcap.read()
    count = 1
    while success:
        videotoimage.append(image)
        success,image = vidcap.read()
        count += 1    
    return count


# Function to convert each image into bytes
def imgtobyte(im) : 
    img = cv2.imread(im)
    im_resize = cv2.resize(img, (500, 500))
    is_success, im_buf_arr = cv2.imencode(".jpg", im_resize)
    byte_im = im_buf_arr.tobytes()
    return byte_im

def dictoarray(dictionary) : 
    return np.array(list(dictionary.items()))


# You'll need the following code, just change the service name
if __name__ == '__main__':
    with grpc.insecure_channel('localhost:8061') as channel:
        estimator_stub = component_pb2_grpc.OpenPoseEstimatorStub(channel)
        try:
            #  python client.py 1 --> returns image with the landmarks
            if sys.argv[1] == '1' :
                response = estimator_stub.estimateImg(component_pb2.Image(data = imgtobyte(sys.argv[3]))) 
                img_bytes = response.data 
                img_array = np.frombuffer(img_bytes, np.uint8)
                image = cv2.imdecode(img_array, -1)
                os.chdir(sys.argv[2])
                cv2.imwrite(sys.argv[3], image)
                cv2.imshow('image',image)
                cv2.waitKey(0) 

            #  python client.py 0 --> returns the landmarks in a dictionnary

            if sys.argv[1] == '0' : 
                nb = vidtoimg(video) 
                for frame in tqdm.tqdm(videotoimage)  :
                    # Send a request to your server and receive the response
                    response = estimator_stub.estimate(component_pb2.Image(data = imgtobyte(frame)))
                    i += 1
                    nb -= 1 
                    
                    if response != {} : 
                        for index, key_points in enumerate(response.poses[0].key_points) : 
                            keypoints.append(response.poses[0].key_points[index].x)
                            keypoints.append(response.poses[0].key_points[index].y)
                            keypoints.append(response.poses[0].key_points[index].z)
                            matrix.append(keypoints)
                            keypoints = []
                        #print(matrix)
                        name = 'frame' + str(i)
                        dic[name] = matrix 
                        matrix = []
                scipy.io.savemat('matlab_data.mat',dic) 
                #print(dictoarray(dic))
                # Check if the response is what you expected
                    #print(response)
        except grpc.RpcError as rpc_error:  # Print the errors if they occur
            print('An error has occurred:')
            print(f'  Error Code: {rpc_error.code()}')