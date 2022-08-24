import concurrent.futures as futures
import io
import logging
import time

import grpc
import grpc_reflection.v1alpha.reflection as grpc_reflect
import PIL.Image

import visualization_proto_pb2 as vis
import visualization_proto_pb2_grpc as vis_grpc

_MAX_WORKERS = 10
_SERVICE_NAME = 'ImageVisualizationService'
_PORT = 8061
_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class ImageVisualizationService(vis_grpc.ImageVisualizationServiceServicer):
    """
    gRPC service to receive and process the received image
    It resizes the images and adds the categories and attributes
    so that they can be displayed
    """

    def __init__(self, current_image):
        self.__current_img = current_image

    def Visualize(self, request: vis.Image, context):
        image_bytes = request.data
        img = PIL.Image.open(io.BytesIO(image_bytes))
        #img = img.resize((300, 300))

        # Save image to bytes
        image_bytes = io.BytesIO()
        img.save(image_bytes, format='jpeg')
        image_bytes = image_bytes.getvalue()
        self.__current_img.bytes = image_bytes
        return vis.Empty()


def run_server(shared_img):
    """
    Runs the gRPC server that receives the requests
    and updates the shared image with the most recent request
    Args:
        shared_img: shared image that should be updated by
                    the server with the most recent request
    """
    logging.basicConfig(level=logging.DEBUG)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=_MAX_WORKERS))
    vis_grpc.add_ImageVisualizationServiceServicer_to_server(
        ImageVisualizationService(shared_img), server)
    service_names = (
        vis.DESCRIPTOR.services_by_name[_SERVICE_NAME].full_name,
        grpc_reflect.SERVICE_NAME
    )
    grpc_reflect.enable_server_reflection(service_names, server)
    server.add_insecure_port(f'[::]:{_PORT}')
    server.start()
    logging.info('Server started at [::]:%s', _PORT)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)