import boto3
import io
from PIL import Image
#from picamera import PiCamera
from time import sleep
import cv2
import board
import neopixel
import time


pixels = neopixel.NeoPixel(board.D18, 4)
rekognition = boto3.client('rekognition', region_name='us-east-2')
dynamodb = boto3.client('dynamodb', region_name='us-east-2')

#camera = cv2.VideoCapture(cv2.CAP_V4L2)
camera = cv2.VideoCapture(0)
#frame = cv2.detect_from_video(frame)

# camera=PiCamera()
#camera.start_preview()



for i in range(5):
    sleep(2)
    leido, frame = camera.read()
    
    if leido == True:
        cv2.imwrite('/home/pi/ciber/PDIYepez/ImagenesPrueba/imagenProfes%s.jpg' % i,frame)
        print("Foto tomada correctamente")
    else:
        print("Error al acceder a la cámara")
        
    
    #camera('/home/pi/ciber/PDIYepez/ImagenesPrueba/imagenProfes%s.jpg' % i)
#camera.stop_preview(       
camera.release()
cv2.destroyAllWindows()


for i in range(5):
    
        
        
    image_path = ('/home/pi/ciber/PDIYepez/ImagenesPrueba/imagenProfes%s.jpg' % i)

    image = Image.open(image_path)
    stream = io.BytesIO()
    image.save(stream,format="JPEG")
    image_binary = stream.getvalue()


    response = rekognition.search_faces_by_image(
            CollectionId='recoprofes',
            Image={'Bytes':image_binary}                                       
            )

    found = False
    for match in response['FaceMatches']:
        print (match['Face']['FaceId'],match['Face']['Confidence'])
            
        face = dynamodb.get_item(
            TableName='recon-profes-tabla',  
            Key={'RekognitionId': {'S': match['Face']['FaceId']}}
            )
        
        if 'Item' in face:
            print ("Found Person: ",face['Item']['FullName']['S'])
            found = True
            
        #print(face['Item'])
        profe = str(face['Item']['FullName']['S'])
        #profe = str(match)
        
        if profe == "David Navarro":
            pixels.fill((255,0,0))
        elif profe == "Lizeth Machado":
            pixels.fill((0,0,255))
        elif profe == "Luis Yepez":
            pixels.fill((0,255,0))#verde Yepez
        elif profe == "Adriana Anselmo":
            pixels.fill((255,255,0))#naranja o morado Adriana
   
    
        

    
        
        

    if not found:
        print("Person cannot be recognized")
        
    
