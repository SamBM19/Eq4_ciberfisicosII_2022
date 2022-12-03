import cv2
from time import sleep
import boto3
import io
from PIL import Image

capture = cv2.VideoCapture(0)
#objeto salida, contiene los parámetros para crear el video


for i in range(5):
    salida = cv2.VideoWriter('/home/pi/ciber/PDIYepez/ImagenesPrueba/imagenProfes%s.jpg' % i, cv2.VideoWriter_fourcc(*'XVID'), 10, (640,480))
    sleep(5)
    ret, frame = capture.read()
    cv2.imshow('frame',frame)
    #Usar write para GUARDAR el video
    salida.write(frame)
    if (cv2.waitKey(1) == ord('s')):
        break

salida.release()
capture.release()
cv2.destroyAllWindows()



rekognition = boto3.client('rekognition', region_name='us-east-2')
dynamodb = boto3.client('dynamodb', region_name='us-east-2')

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

    if not found:
        print("Person cannot be recognized")
        
    
