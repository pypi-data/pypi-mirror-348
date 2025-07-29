import sensor_msgs.msg 
import cv2
from cv_bridge import CvBridge
import base64
import numpy as np
import json
from rosidl_runtime_py.convert import message_to_ordereddict

def compress_and_encode_image(msg, quality=100, max_width=800):
    """
    Compress an image message, encode as base64, and optionally chunk into JSON-compatible parts
    
    Args:
        msg: ROS image message
        quality: JPEG quality (0-100)
        max_width: Maximum width to resize to (maintains aspect ratio)
        chunk_size: Max size of base64 string per chunk (default 100KB)
    
    Returns:
        dict: Contains either full image or list of base64 chunks with metadata
    """
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

    height, width = cv_image.shape[:2]
    if width > max_width:
        scale_factor = max_width / width
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        cv_image = cv2.resize(cv_image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    encode_params = [cv2.IMWRITE_JPEG_PROGRESSIVE, 1, cv2.IMWRITE_JPEG_QUALITY, quality]
    success, encoded_image = cv2.imencode('.jpg', cv_image, encode_params)
    
    return encoded_image.tobytes()
    
    # # Load the image
    # encoded_image = cv2.imread('drone.jpg')

    # # Check if the image was loaded successfully
    # if encoded_image is None:
    #     print("Error: Could not load image.")
    # else:
    #     # Display the image in a window
    #     # cv2.imshow('Loaded Image', encoded_image)
    #     print("Loaded image.")

    # if not success:
    #     raise ValueError("Image encoding failed")

    # base64_encoded = base64.b64encode(encoded_image).decode('utf-8')
    # encoded_size = len(base64_encoded.encode('utf-8'))

    # result = {
    #     "format": "jpeg",
    #     "image_base64": base64_encoded,
    # }
    # result2 =None

    # if encoded_size > chunk_size:
    #     result2 ={
    #         "format": "jpeg",
    #     }
    #     chunks = [base64_encoded[i:i + chunk_size] for i in range(0, len(base64_encoded), chunk_size)]
    #     result2["image_base64"] = chunks[0]
    #     result2["chunked"] = True
    #     result2["num_chunks"] = len(chunks)
    
    # result["image_base64"] = base64_encoded
    # result["chunked"] = False
    # result["num_chunks"] = 0

    # json_string = json.dumps(result)
    
    # print(f"Compressed image size: {len(encoded_image)} bytes")
    # print(f"Base64 string size: {len(base64_encoded)} characters")
    # print(f"Json_string: {json_string}")
    # return encoded_image

def convert(msg_type, format, msg):
    if msg_type == "sensor_msgs.msg.Image":
        return compress_and_encode_image(msg)
    else:
        return message_to_ordereddict(msg)