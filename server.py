# NOTE: Throughout the file the places where you need to make changes are labeled with a TODO.

# Mandatory imports
from concurrent import futures
import grpc
import grpc_reflection.v1alpha.reflection as grpc_reflection
# TODO: change the files names (make sure to change these names in the entire file, not just in these two lines)
import component_pb2
import component_pb2_grpc
import sys 

#Component imports 
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
import numpy as np

# Optional but useful imports

def imgtobyte(im) : 

    im_resize = cv2.resize(im, (500, 500))
    is_success, im_buf_arr = cv2.imencode(".jpg", im)
    byte_im = im_buf_arr.tobytes()
    return byte_im

import logging  # For printing information about execution (warnings, errors, etc). See
                # https://docs.python.org/3/howto/logging.html for more info on this


  # TODO: Choose a name for your server class and replace "YourServerClassName". Also replace "YourServicer" with the correct class name
class Server(component_pb2_grpc.OpenPoseEstimatorServicer):

    """Provides methods that implement functionality of your server."""
    # TODO: Replace "YourMethodName" with the method name you defined in your proto
    
    #returns landmarks keypoints 


    
    def estimate(self, request, context):
        """
        Implement your component funcionality here.
        :param request: the input message that your server just received.
        :param context: you can ignore this TODO: check this
        """
        # You can perform some verifications:
        # logging.info("Executing YourMethodName...")
        # if not request or request.some_number == 0:
        #     logging.error("Received empty request.")
        #     return your_service_name_pb2.OutputMessage()  # Simply returns an empty message
        

        with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=10, 
            refine_landmarks=True,
            min_detection_confidence=0.2) as face_mesh:
            img_bytes = request.data 
            img_array = np.frombuffer(img_bytes, np.uint8)
            image = cv2.imdecode(img_array, -1)
            # Convert the BGR image to RGB before processing.
            results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            poses_list= []

            if not results.multi_face_landmarks : 
                list_keypoints = []
                for id in range(478) :
                    keypoint  = component_pb2.KeyPoint(x = 0, y =0, z = 0)
                    list_keypoints.append(keypoint)
                
                pose_message = component_pb2.Pose(key_points = list_keypoints)
                poses_list.append(pose_message)
                return component_pb2.Poses(poses = poses_list)
                


            for face_landmarks in results.multi_face_landmarks:
                list_keypoints = []
                for landmark in face_landmarks.landmark :
                    keypoint  = component_pb2.KeyPoint(x = landmark.x, y =landmark.y, z = landmark.z)
                    list_keypoints.append(keypoint)
                pose_message = component_pb2.Pose(key_points = list_keypoints)
                poses_list.append(pose_message)
            multipose_msg = component_pb2.Poses(poses = poses_list)
            return multipose_msg

    #returns image with the landmarks    

    def estimateImg(self, request, context):
        with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=10, 
            refine_landmarks=True,
            min_detection_confidence=0.2) as face_mesh:
            img_bytes = request.data 
            img_array = np.frombuffer(img_bytes, np.uint8)
            image = cv2.imdecode(img_array, -1)
            # Convert the BGR image to RGB before processing.
            results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            annotated_image = image.copy()

            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())
                mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style())

            
            return component_pb2.Image(data = imgtobyte(annotated_image))
# The following code is required. Most likely you'll only need to change the service name to match your service name
def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    # TODO: Change "YourServicer" in the method name to the correct name. Also change "YourServerClassName" to the class name you choose earlier
    component_pb2_grpc.add_OpenPoseEstimatorServicer_to_server(
        Server(), server)

    # Add reflection. Is required so that the pipeline orchestrator knows what method to invoke
    service_names = (
        component_pb2.DESCRIPTOR.services_by_name['OpenPoseEstimator'].full_name,  # TODO: change "YourServiceName"
        grpc_reflection.SERVICE_NAME
    )
    grpc_reflection.enable_server_reflection(service_names, server)

    server.add_insecure_port('[::]:8061')  # Port 8061 is used to match AI4Europe specs and ensure compatibility
    server.start()
    logging.info("Successfully started and waiting for connections..")
    server.wait_for_termination()

if __name__ == '__main__':
    # Configure the following line according to the level of messages you want displayed on the terminal
    # This displays all messages
    logging.basicConfig(format='Server %(levelname)s: %(message)s', level=logging.INFO)
    # This displays only warnings or higher
    logging.basicConfig(format='Server %(levelname)s: %(message)s', level=logging.WARNING)
    serve()