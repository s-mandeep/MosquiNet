from detecto.core import Model
import cv2
import urllib.request
from azure.storage.blob import BlobClient
from datetime import datetime
import logging
import os
from detecto.core import Model
from detecto.utils import read_image

def detect_image(model, input_file, output_file, score_filter=0.6):

    image = read_image(input_file)
    predictions = model.predict(image)
    for label, box, score in zip(*predictions):
            if score < score_filter:
                continue
            image = cv2.rectangle(image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255, 0, 0), 3)
            image = cv2.putText(image, '{}: {}'.format(label, round(score.item(), 2)), (int(box[0]), int(box[1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    cv2.imwrite(output_file,image)

def tag(url):
   
    file_name = '/tmp/input_'+str(datetime.now()).replace(':','').replace('.','').replace(' ','').replace('-','')+".jpg" 
    logging.info("Downloading image...")
    urllib.request.urlretrieve(url, file_name)     
    logging.info("Downloaded the image.")
    dirname = os.path.dirname(__file__)
    model = Model.load(os.path.join(dirname, 'model.pth'),["tire", "pool", "bottle", "bucket", "watertank", "puddle"])
    logging.info("Model loaded.")
    output_name="/tmp/output_"+str(datetime.now()).replace(':','').replace('.','').replace(' ','').replace('-','')+".jpg"
    detect_image(model,file_name,output_name)
    logging.info("Finished tagging the image.")
    blob = BlobClient.from_connection_string(
        conn_str="DefaultEndpointsProtocol=https;AccountName=imaginecupmosquinet;AccountKey=6IB70jkGdlM9YJrs6vCuoJw64uE9hTZHH5n1I0JdhoDVFXGQKJW6D7MOYZQE5PciRkPlu2k/ZNO55jJ9tuR9Mg==;EndpointSuffix=core.windows.net", container_name="dropzone", blob_name=output_name)
    with open(output_name, "rb") as data:
        blob.upload_blob(data)
    logging.info("Video uploaded")
    remote_image_url = "https://imaginecupmosquinet.blob.core.windows.net/dropzone/" + output_name
    return remote_image_url


