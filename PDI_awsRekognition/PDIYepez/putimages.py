import boto3

s3 = boto3.resource('s3')

# Get list of objects for indexing
images=[('navarro1.jpg','David Navarro'),
      ('navarro2.jpg','David Navarro'),
      ('yepez1.jpg','Luis Yepez'),
      ('yepez2.jpg','Luis Yepez'),
      ('adriana1.jpg','Adriana Anselmo'),
      ('adriana2.jpg','Adriana Anselmo'),
      ('liz1.jpg','Lizeth Machado'),
      ('liz2.jpg','Lizeth Machado')
      ]

# Iterate through list to upload objects to S3   
for image in images:
    file = open(image[0],'rb')
    object = s3.Object('recon-profes-bucket','index/'+ image[0])
    ret = object.put(Body=file,
                    Metadata={'FullName':image[1]})