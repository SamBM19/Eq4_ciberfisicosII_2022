
    ###  Librerias  ###
import RPi.GPIO as GPIO
from mfrc522 import MFRC522
from time import sleep
import paho.mqtt.client as mqtt
import sys
import pygame
import Mov_Keyboard as Mk
import json
from datetime import datetime
from pygame.locals import *
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

###  Cfg GPIO  ###
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

###  Cfg Motor 1  ###
ENA1,IN1,IN2 = 13,3,5
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA1, GPIO.OUT)

PWMA = GPIO.PWM(ENA1, 100)
PWMA.start(0)

#GPIO.output(IN1, True)
#GPIO.output(IN2, False)

# # Cambiar Velocidad Motor 1
#PWMA.ChangeDutyCycle(100)
#     GPIO.output(ENA1, True)

###  Cfg Motor 2  ###
ENA2,IN3,IN4 = 35,33,37
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA2, GPIO.OUT)

PWMB = GPIO.PWM(ENA2, 100)
PWMB.start(0)

#GPIO.output(IN3, True)
#GPIO.output(IN4, False)

# # Cambiar Velocidad Motor 2
#PWMB.ChangeDutyCycle(100)
#GPIO.output(ENA2, True)

### Cfg Servo 1 ###
GPIO.setup(7, GPIO.OUT)
servo = GPIO.PWM(7,50)
servo.start(0)

### Cfg Servo 2 ###
GPIO.setup(11, GPIO.OUT)
servo2 = GPIO.PWM(11,50)
servo2.start(0)

###  Cfg RFID  ###
continue_reading = True
# This is the default key for authentication
key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
#Mifare Block number
block_num = 4
block_num2=8
block_num3=12
block_num4=16

###  Cfg Certificados  ###
Root_CA = "/home/pi/Documents/Certificates/root-ca.pem"
Private_Key = "/home/pi/Documents/Certificates/private.pem.key"
Certificate = "/home/pi/Documents/Certificates/certificate.pem.crt" 

###  Cfg MQTT  ###
#broker_address="10.48.248.229"
#topic = 'L_RFID1'

client = mqtt.Client()
#client.connect(broker_address)

Mk.init()

def main():

    if Mk.getKey('UP'):

        PWMA.ChangeDutyCycle(100)
        PWMB.ChangeDutyCycle(100)
        GPIO.output(IN1, True)
        GPIO.output(IN2, False)
        GPIO.output(IN3, True)
        GPIO.output(IN4, False)
    
        # sleep(TX) Usar para avanzar por X Tiempo
        print('Tecla ARRIBA presionada')

    elif Mk.getKey('DOWN'):

        PWMA.ChangeDutyCycle(100)
        PWMB.ChangeDutyCycle(100)
        GPIO.output(IN1, False)
        GPIO.output(IN2, True)
        GPIO.output(IN3, False)
        GPIO.output(IN4, True)
    
        # sleep(TX) Usar para avanzar por X Tiempo
        print('Tecla ABAJO presionada')

    elif Mk.getKey('LEFT'):

        PWMA.ChangeDutyCycle(10)
        PWMB.ChangeDutyCycle(100)
        GPIO.output(IN1, False)
        GPIO.output(IN2, False)
        GPIO.output(IN3, True)
        GPIO.output(IN4, False)
    
        # sleep(TX) Usar para avanzar por X Tiempo
        print('Tecla IZQUIERDA presionada')

    elif Mk.getKey('RIGHT'):

        PWMA.ChangeDutyCycle(100)
        PWMB.ChangeDutyCycle(10)
        GPIO.output(IN1, True)
        GPIO.output(IN2, False)
        GPIO.output(IN3, False)
        GPIO.output(IN4, False)
    
        # sleep(TX) Usar para avanzar por X Tiempo
        print('Tecla DERECHA presionada')

    elif Mk.getKey('x'):

        servo.ChangeDutyCycle(2)
        sleep(0.5)
        servo.ChangeDutyCycle(0)       

        print('Servo Derecha') 

    elif Mk.getKey('c'):

        duty = 1

        while duty <= 7:
            servo.ChangeDutyCycle(duty)
            duty = duty + 1
            #sleep(0.1)

        # sleep(TX) Usar para avanzar por X Tiempo
        print('Centro Servo')        

    elif Mk.getKey('v'):

        duty = 1

        while duty <= 12:
            servo.ChangeDutyCycle(duty)
            duty = duty + 1
            #sleep(0.1)

            print('Servo Izquierda') 

    elif Mk.getKey('b'):

        duty = 1

        while duty <= 3:
            servo2.ChangeDutyCycle(duty)
            duty = duty + 1
            #sleep(0.1)

        # sleep(TX) Usar para avanzar por X Tiempo
        print('Arriba Servo 2')  
    
    elif Mk.getKey('n'):

            duty = 1

            while duty <= 5:
                servo2.ChangeDutyCycle(duty)
                duty = duty + 1
                #sleep(0.1)

                print('Centro Servo 2') 

    elif Mk.getKey('m'):

        duty = 1

        while duty <= 7:
            servo2.ChangeDutyCycle(duty)
            duty = duty + 1
            #sleep(0.1)

            print('Abajo Servo 2') 

    else:

        servo.ChangeDutyCycle(0)
        servo2.ChangeDutyCycle(0)
        PWMA.ChangeDutyCycle(0)
        PWMB.ChangeDutyCycle(0)
        GPIO.output(IN1, False)
        GPIO.output(IN2, False)
        GPIO.output(IN3, False)
        GPIO.output(IN4, False)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # Create an object of the class MFRC522
        MIFAREReader = MFRC522()
        # This loop keeps checking for chips. If one is near it will get the UID and authenticate
        if continue_reading :
            if Mk.getKey('1'):
                print('Tarjeta 1 en proceso de lectura')
                Lect_RFID1 = True  
                Lect_RFID2 = 0
                Lect_RFID3 = 0
                Del_RFID1 = 0
                Del_RFID2 = 0  
                Del_RFID3 = 0
                Home_Carga = 0
                Home_Stop = 0
                Reset = 0
                print('Tecla 1 presionada')
                """
                client.publish(topic = 'L_RFID1', payload = Lect_RFID1, qos=0)
                client.publish(topic = 'L_RFID2', payload = Lect_RFID2, qos=0)       
                client.publish(topic = 'L_RFID3', payload = Lect_RFID3, qos=0)
                client.publish(topic = 'D_RFID1', payload = Del_RFID1, qos=0)
                client.publish(topic = 'D_RFID2', payload = Del_RFID2, qos=0)       
                client.publish(topic = 'D_RFID3', payload = Del_RFID3, qos=0)
                client.publish(topic = 'Home_Carga', payload = Home_Carga, qos=0)
                client.publish(topic = 'Home_Stop', payload = Home_Stop, qos=0)
                client.publish(topic = 'Reset', payload = Reset, qos=0)
                """
                # Scan for cards    
                (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                # If a card is found
                if status == MIFAREReader.MI_OK:
                    print("Tag detectado")
                    
                # Get the UID of the card
                (status,uid) = MIFAREReader.MFRC522_Anticoll()
                # If we have the UID, continue
                block_num= 4
                key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

                if status == MIFAREReader.MI_OK:
                        # Variable for the data to write        
                        # Print UID
                    #print("UID de tag: %s%s%s%s" % ('{0:x}'.format(uid[0]), '{0:x}'.format(uid[1]), '{0:x}'.format(uid[2]), '{0:x}'.format(uid[3])))
                        
                        # Select the scanned tag
                    MIFAREReader.MFRC522_SelectTag(uid)
                        # Authenticate
                    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_num, key, uid)
                        # Check if authenticated
                    

                    if status == MIFAREReader.MI_OK:
                        print("El sector 1 tenía esta información:")
                            # Read block 8
                        backdata_4 = MIFAREReader.MFRC522_Read(block_num)
                        backdata_5= MIFAREReader.MFRC522_Read(block_num+1)
                        backdata_6= MIFAREReader.MFRC522_Read(block_num+2)

                            #print(backdata)
                        read_value4=''.join([chr(number) for number in backdata_4])
                        read_value5=''.join([chr(number) for number in backdata_5])
                        read_value6=''.join([chr(number) for number in backdata_6])
                        print(block_num)
                        #print(backdata_4)
                        #print(backdata_5)
                        #print(backdata_6)
                        #print(read_value4)
                        #print(read_value5)
                        #print(read_value6)
                        
                                #print(read_value4)
                        #s1 = "" + read_value4 + "" + read_value5 + "" + read_value6
                                #print(read_value1)
                        GPIO.cleanup()
                        continue_reading==True
                        #print('s1', s1)
                        MIFAREReader = MFRC522()
                        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                        
                        # Scan for cards    
                        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                        # If a card is found
                        block_num2= 8
                        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                        if status == MIFAREReader.MI_OK:
                            print("Tag detectado")
                            
                        # Get the UID of the card
                        (status,uid) = MIFAREReader.MFRC522_Anticoll()
                        # If we have the UID, continue
                        if status == MIFAREReader.MI_OK:
                                # Variable for the data to write        
                                # Print UID
                            #print("UID de tag: %s%s%s%s" % ('{0:x}'.format(uid[0]), '{0:x}'.format(uid[1]), '{0:x}'.format(uid[2]), '{0:x}'.format(uid[3])))
                                
                                # Select the scanned tag
                            MIFAREReader.MFRC522_SelectTag(uid)
                                # Authenticate
                            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_num2, key, uid)
                                # Check if authenticated
                            
                            if status == MIFAREReader.MI_OK:
                                print("El sector 2 tenía esta información:")
                                    # Read block 8
                                backdata_8 = MIFAREReader.MFRC522_Read(block_num2)
                                
                                backdata_9= MIFAREReader.MFRC522_Read(block_num2+1)
                                backdata_10= MIFAREReader.MFRC522_Read(block_num2+2)

                                    #print(backdata)
                                read_value8=''.join([chr(number) for number in backdata_8])
                                read_value9=''.join([chr(number) for number in backdata_9])
                                read_value10=''.join([chr(number) for number in backdata_10])
                                print(block_num2)
                                
                                        #print(read_value4)
                                s2 = "" + read_value8+ "" + "" + read_value9 + "" + read_value10 + ""
                                        #print(read_value1)
                                GPIO.cleanup()
                                continue_reading==True
                                #print('s2',s2)

                                MIFAREReader = MFRC522()
                                key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                                
                                # Scan for cards    
                                (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                                # If a card is found
                                if status == MIFAREReader.MI_OK:
                                    print("Tag detectado")
                                    
                                # Get the UID of the card
                                (status,uid) = MIFAREReader.MFRC522_Anticoll()
                                # If we have the UID, continue
                                block_num3= 12
                                key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                                if status == MIFAREReader.MI_OK:
                                        # Variable for the data to write        
                                        # Print UID
                                    #print("UID de tag: %s%s%s%s" % ('{0:x}'.format(uid[0]), '{0:x}'.format(uid[1]), '{0:x}'.format(uid[2]), '{0:x}'.format(uid[3])))
                                        
                                        # Select the scanned tag
                                    MIFAREReader.MFRC522_SelectTag(uid)
                                        # Authenticate
                                    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_num3, key, uid)
                                        # Check if authenticated
                                    
                                    block_num3= block_num3

                                    if status == MIFAREReader.MI_OK:
                                        print("El sector 3 tenía esta información:")
                                            # Read block 8
                                        backdata_12 = MIFAREReader.MFRC522_Read(block_num3)
                                        backdata_13= MIFAREReader.MFRC522_Read(block_num3+1)
                                        backdata_14= MIFAREReader.MFRC522_Read(block_num3+2)

                                            #print(backdata)
                                        read_value12=''.join([chr(number) for number in backdata_12])
                                        read_value13=''.join([chr(number) for number in backdata_13])
                                        read_value14=''.join([chr(number) for number in backdata_14])
                                        print(block_num3)
                                        
                                                #print(read_value4)
                                        #s3 = "" + read_value12 + "" + read_value13 + "" + read_value14 + ""
                                                #print(read_value1)
                                        GPIO.cleanup()
                                        continue_reading==True
                                        #print("s3",s3)
                                        
                                        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                                        MIFAREReader = MFRC522()

                                        # Scan for cards    
                                        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                                        # If a card is found
                                        if status == MIFAREReader.MI_OK:
                                            print("Tag detectado")
                                            
                                        # Get the UID of the card
                                        (status,uid) = MIFAREReader.MFRC522_Anticoll()
                                        # If we have the UID, continue
                                        block_num4=16
                                        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                                        if status == MIFAREReader.MI_OK:
                                                # Variable for the data to write        
                                                # Print UID
                                            #print("UID de tag: %s%s%s%s" % ('{0:x}'.format(uid[0]), '{0:x}'.format(uid[1]), '{0:x}'.format(uid[2]), '{0:x}'.format(uid[3])))
                                                
                                                # Select the scanned tag
                                            MIFAREReader.MFRC522_SelectTag(uid)
                                                # Authenticate
                                            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_num4, key, uid)
                                                # Check if authenticated
                                            
                                            block_num4= block_num4

                                            if status == MIFAREReader.MI_OK:
                                                print("El sector 4 tenía esta información:")
                                                    # Read block 8
                                                backdata_16 = MIFAREReader.MFRC522_Read(block_num4)
                                                backdata_17= MIFAREReader.MFRC522_Read(block_num4+1)
                                                backdata_18= MIFAREReader.MFRC522_Read(block_num4+2)

                                                    #print(backdata)
                                                read_value16=''.join([chr(number) for number in backdata_16])
                                                read_value17=''.join([chr(number) for number in backdata_17])
                                                read_value18=''.join([chr(number) for number in backdata_18])
                                                print(block_num4)
                                                
                                                        #print(read_value4)
                                                #s4 ="" + read_value16 + "" + read_value17 + "" + read_value18 + ""
                                                        #print(read_value1)
                                                GPIO.cleanup()
                                                continue_reading==True
                                                #print("s4",s4)
                                                #s5="" + read_value5 + "" + read_value5 + "" + read_value6 + "" + read_value9 + "" + read_value9 + "" + read_value10 + "" + read_value13 + "" + read_value13 + "" + read_value14 + "" + read_value16 + "" + read_value17 + "" + read_value18 + ""
                                                s5="" + read_value4 + "" + read_value5 + "" + read_value6 + "" + read_value8+ ""+read_value9 + "" + read_value10 + "" + read_value12 + "" + read_value13 + "" + read_value14 + "" + read_value16 + "" + read_value17 + "" + read_value18
                                                s1="" + read_value4 + "" + read_value5 + "" + read_value6 + "" + read_value8
                                                s2="" + read_value9 + "" + read_value10 + "" + read_value12 + "" + read_value13
                                                s3="" + read_value14 + "" + read_value16 + "" + read_value17 + "" + read_value18
                                                #print("s4",s5)
                                                print('JSON leído en la tarjeta',s5)
                                                myMQTTClient=AWSIoTMQTTClient('Prueba')
                                                myMQTTClient.configureEndpoint("a2l5d164bdvycm-ats.iot.us-east-2.amazonaws.com", 8883)

                                                myMQTTClient.configureCredentials(Root_CA, Private_Key, Certificate)

                                                myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
                                                myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
                                                myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
                                                myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
                                                print ('Initiating Realtime Data Transfer From Raspberry Pi...')
                                                myMQTTClient.connect()
                                                now=datetime.now()

                                                timestamp = int(datetime.timestamp(now)*1000000)
                                                timestamp = timestamp *100 + 1
                                                
                                                s1=s1.replace("{","{\"Pan_1\":""{")
                                                s2=s2.replace("{",",\"Pan_2\":""{")
                                                s3=s3.replace("{",",\"Pan_3\":""{")
                                                s5=s1+s2+s3
                                                print(s5)
                                                #s5=s5.replace(" ","")
                                                s5=s5.replace(" ","")
                                                s5=s5.replace("\u0000","")

                                                s5=s5.replace(":{",":{\"timestamp\":"+str(timestamp)+",")
                                                s5=s5.replace("}{","},")
                                                s5=s5.replace(s5,s5+"}")                                              

                                                myMQTTClient.publish(
                                                topic="iot/Panaderia_reto",
                                                QoS=1,
                                                payload=json.dumps(s5),
                                                )                                                
                                                                                      
                                                
        # Create an object of the class MFRC522
            MIFAREReader = MFRC522()
            # This loop keeps checking for chips. If one is near it will get the UID and authenticate
            if continue_reading:
                if Mk.getKey('2'):
                    print('Tarjeta 2 en proceso de lectura')
                    Lect_RFID1 = 0 
                    Lect_RFID2 = True  
                    Lect_RFID3 = 0
                    Del_RFID1 = 0
                    Del_RFID2 = 0  
                    Del_RFID3 = 0
                    Home_Carga = 0
                    Home_Stop = 0
                    Reset = 0
                    print('Tecla 2 presionada') 
                    client.publish(topic = 'L_RFID1', payload = Lect_RFID1, qos=0)
                    client.publish(topic = 'L_RFID2', payload = Lect_RFID2, qos=0)       
                    client.publish(topic = 'L_RFID3', payload = Lect_RFID3, qos=0)
                    client.publish(topic = 'D_RFID1', payload = Del_RFID1, qos=0)
                    client.publish(topic = 'D_RFID2', payload = Del_RFID2, qos=0)       
                    client.publish(topic = 'D_RFID3', payload = Del_RFID3, qos=0)
                    client.publish(topic = 'Home_Carga', payload = Home_Carga, qos=0)
                    client.publish(topic = 'Home_Stop', payload = Home_Stop, qos=0)
                    client.publish(topic = 'Reset', payload = Reset, qos=0)
                    # Scan for cards    
                    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                    # If a card is found
                    block_num= 4
                    key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]


                    if status == MIFAREReader.MI_OK:
                        print("Tag detectado")
                        
                    # Get the UID of the card
                    (status,uid) = MIFAREReader.MFRC522_Anticoll()
                    # If we have the UID, continue
                    if status == MIFAREReader.MI_OK:
                            # Variable for the data to write        
                            # Print UID
                        #print("UID de tag: %s%s%s%s" % ('{0:x}'.format(uid[0]), '{0:x}'.format(uid[1]), '{0:x}'.format(uid[2]), '{0:x}'.format(uid[3])))
                            
                            # Select the scanned tag
                        MIFAREReader.MFRC522_SelectTag(uid)
                            # Authenticate
                        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_num, key, uid)
                            # Check if authenticated
                        

                        if status == MIFAREReader.MI_OK:
                            print("El sector 1 tenía esta información:")
                                # Read block 8
                            backdata_4 = MIFAREReader.MFRC522_Read(block_num)
                            backdata_5= MIFAREReader.MFRC522_Read(block_num+1)
                            backdata_6= MIFAREReader.MFRC522_Read(block_num+2)

                                #print(backdata)
                            read_value4=''.join([chr(number) for number in backdata_4])
                            read_value5=''.join([chr(number) for number in backdata_5])
                            read_value6=''.join([chr(number) for number in backdata_6])
                            print(block_num)
                            #print(backdata_4)
                            #print(backdata_5)
                            #print(backdata_6)
                            #print(read_value4)
                            #print(read_value5)
                            #print(read_value6)
                            
                                    #print(read_value4)
                            #s1 = "" + read_value4 + "" + read_value5 + "" + read_value6
                                    #print(read_value1)
                            GPIO.cleanup()
                            continue_reading==True
                            #print('s1', s1)
                            MIFAREReader = MFRC522()
                            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                            
                            # Scan for cards    
                            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                            # If a card is found
                            block_num2= 8
                            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]


                            if status == MIFAREReader.MI_OK:
                                print("Tag detectado")
                                
                            # Get the UID of the card
                            (status,uid) = MIFAREReader.MFRC522_Anticoll()
                            # If we have the UID, continue
                            if status == MIFAREReader.MI_OK:
                                    # Variable for the data to write        
                                    # Print UID
                                #print("UID de tag: %s%s%s%s" % ('{0:x}'.format(uid[0]), '{0:x}'.format(uid[1]), '{0:x}'.format(uid[2]), '{0:x}'.format(uid[3])))
                                    
                                    # Select the scanned tag
                                MIFAREReader.MFRC522_SelectTag(uid)
                                    # Authenticate
                                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_num2, key, uid)
                                    # Check if authenticated
                                
                                if status == MIFAREReader.MI_OK:
                                    print("El sector 2 tenía esta información:")
                                        # Read block 8
                                    backdata_8 = MIFAREReader.MFRC522_Read(block_num2)
                                    
                                    backdata_9= MIFAREReader.MFRC522_Read(block_num2+1)
                                    backdata_10= MIFAREReader.MFRC522_Read(block_num2+2)

                                        #print(backdata)
                                    read_value8=''.join([chr(number) for number in backdata_8])
                                    read_value9=''.join([chr(number) for number in backdata_9])
                                    read_value10=''.join([chr(number) for number in backdata_10])
                                    print(block_num2)
                                    
                                            #print(read_value4)
                                    s2 = "" + read_value8+ "" + "" + read_value9 + "" + read_value10 + ""
                                            #print(read_value1)
                                    GPIO.cleanup()
                                    continue_reading==True
                                    #print('s2',s2)

                                    MIFAREReader = MFRC522()
                                    
                                    # Scan for cards    
                                    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                                    # If a card is found
                                    if status == MIFAREReader.MI_OK:
                                        print("Tag detectado")
                                        
                                    # Get the UID of the card
                                    (status,uid) = MIFAREReader.MFRC522_Anticoll()
                                    # If we have the UID, continue
                                    block_num3= 12
                                    key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]


                                    if status == MIFAREReader.MI_OK:
                                            # Variable for the data to write        
                                            # Print UID
                                        #print("UID de tag: %s%s%s%s" % ('{0:x}'.format(uid[0]), '{0:x}'.format(uid[1]), '{0:x}'.format(uid[2]), '{0:x}'.format(uid[3])))
                                            
                                            # Select the scanned tag
                                        MIFAREReader.MFRC522_SelectTag(uid)
                                            # Authenticate
                                        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_num3, key, uid)
                                            # Check if authenticated
                                        
                                        if status == MIFAREReader.MI_OK:
                                            print("El sector 3 tenía esta información:")
                                                # Read block 8
                                            backdata_12 = MIFAREReader.MFRC522_Read(block_num3)
                                            backdata_13= MIFAREReader.MFRC522_Read(block_num3+1)
                                            backdata_14= MIFAREReader.MFRC522_Read(block_num3+2)

                                                #print(backdata)
                                            read_value12=''.join([chr(number) for number in backdata_12])
                                            read_value13=''.join([chr(number) for number in backdata_13])
                                            read_value14=''.join([chr(number) for number in backdata_14])
                                            print(block_num3)
                                            
                                                    #print(read_value4)
                                            #s3 = "" + read_value12 + "" + read_value13 + "" + read_value14 + ""
                                                    #print(read_value1)
                                            GPIO.cleanup()
                                            continue_reading==True
                                            #print("s3",s3)
                                            
                                            MIFAREReader = MFRC522()

                                            # Scan for cards    
                                            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                                            # If a card is found
                                            block_num4= 16
                                            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]


                                            if status == MIFAREReader.MI_OK:
                                                print("Tag detectado")
                                                
                                            # Get the UID of the card
                                            (status,uid) = MIFAREReader.MFRC522_Anticoll()
                                            # If we have the UID, continue
                                            if status == MIFAREReader.MI_OK:
                                                    # Variable for the data to write        
                                                    # Print UID
                                                #print("UID de tag: %s%s%s%s" % ('{0:x}'.format(uid[0]), '{0:x}'.format(uid[1]), '{0:x}'.format(uid[2]), '{0:x}'.format(uid[3])))
                                                    
                                                    # Select the scanned tag
                                                MIFAREReader.MFRC522_SelectTag(uid)
                                                    # Authenticate
                                                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_num4, key, uid)
                                                    # Check if authenticated
                                            
                                                if status == MIFAREReader.MI_OK:
                                                    print("El sector 4 tenía esta información:")
                                                        # Read block 8
                                                    backdata_16 = MIFAREReader.MFRC522_Read(block_num4)
                                                    backdata_17= MIFAREReader.MFRC522_Read(block_num4+1)
                                                    backdata_18= MIFAREReader.MFRC522_Read(block_num4+2)

                                                        #print(backdata)
                                                    read_value16=''.join([chr(number) for number in backdata_16])
                                                    read_value17=''.join([chr(number) for number in backdata_17])
                                                    read_value18=''.join([chr(number) for number in backdata_18])
                                                    print(block_num4)
                                                    
                                                            #print(read_value4)
                                                    #s4 ="" + read_value16 + "" + read_value17 + "" + read_value18 + ""
                                                            #print(read_value1)
                                                    GPIO.cleanup()
                                                    continue_reading==True
                                                    #print("s4",s4)
                                                    #s5="" + read_value5 + "" + read_value5 + "" + read_value6 + "" + read_value9 + "" + read_value9 + "" + read_value10 + "" + read_value13 + "" + read_value13 + "" + read_value14 + "" + read_value16 + "" + read_value17 + "" + read_value18 + ""
                                                    s5="" + read_value4 + "" + read_value5 + "" + read_value6 + "" + read_value8 + "" + read_value9 + "" + read_value10 + "" + read_value12 + "" + read_value13 + "" + read_value14 + "" + read_value16 + "" + read_value17 + "" + read_value18
                                                    s1="" + read_value4 + "" + read_value5 + "" + read_value6 + "" + read_value8
                                                    s2="" + read_value9 + "" + read_value10 + "" + read_value12 + "" + read_value13
                                                    s3="" + read_value14 + "" + read_value16 + "" + read_value17 + "" + read_value18
                                                    #print("s4",s5)
                                                    print('JSON leído en la tarjeta',s5)
                                                    myMQTTClient=AWSIoTMQTTClient('Prueba')
                                                    myMQTTClient.configureEndpoint("a2l5d164bdvycm-ats.iot.us-east-2.amazonaws.com", 8883)

                                                    myMQTTClient.configureCredentials(Root_CA, Private_Key, Certificate)

                                                    myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
                                                    myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
                                                    myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
                                                    myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
                                                    print ('Initiating Realtime Data Transfer From Raspberry Pi...')
                                                    myMQTTClient.connect()
                                                    
                                                
                                                    now=datetime.now()

                                                    timestamp = int(datetime.timestamp(now)*1000000)
                                                    timestamp = timestamp *100 + 2
                                                    s1=s1.replace("{","{\"Pan_1\":""{")
                                                    s2=s2.replace("{",",\"Pan_2\":""{")
                                                    s3=s3.replace("{",",\"Pan_3\":""{")
                                                    s5=s1+s2+s3
                                                    print(s5)
                                                    s5=s5.replace(" ","")
                                                    s5=s5.replace("\u0000","")

                                                    s5=s5.replace(":{",":{\"timestamp\":"+str(timestamp)+",")
                                                    s5=s5.replace("}{","},")
                                                    s5=s5.replace(s5,s5+"}")                                              

                                                    myMQTTClient.publish(
                                                    topic="iot/Panaderia_reto",
                                                    QoS=1,
                                                    payload=json.dumps(s5),
                                                    )  
                                                
            # Create an object of the class MFRC522
            MIFAREReader = MFRC522()
            # This loop keeps checking for chips. If one is near it will get the UID and authenticate
            if continue_reading:
                if Mk.getKey('3'):

                    print('Tarjeta 3 en proceso de lectura')
                    Lect_RFID1 = 0 
                    Lect_RFID2 = 0  
                    Lect_RFID3 = True
                    Del_RFID1 = 0
                    Del_RFID2 = 0  
                    Del_RFID3 = 0
                    Home_Carga = 0  
                    Home_Stop = 0
                    Reset = 0
                    print('Tecla 3 presionada') 
                    client.publish(topic = 'L_RFID1', payload = Lect_RFID1, qos=0)
                    client.publish(topic = 'L_RFID2', payload = Lect_RFID2, qos=0)       
                    client.publish(topic = 'L_RFID3', payload = Lect_RFID3, qos=0)
                    client.publish(topic = 'D_RFID1', payload = Del_RFID1, qos=0)
                    client.publish(topic = 'D_RFID2', payload = Del_RFID2, qos=0)       
                    client.publish(topic = 'D_RFID3', payload = Del_RFID3, qos=0)
                    client.publish(topic = 'Home_Carga', payload = Home_Carga, qos=0)
                    client.publish(topic = 'Home_Stop', payload = Home_Stop, qos=0)
                    client.publish(topic = 'Reset', payload = Reset, qos=0)
                    # Scan for cards    
                    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                    # If a card is found
                    if status == MIFAREReader.MI_OK:
                        print("Tag detectado")
                        
                    # Get the UID of the card
                    (status,uid) = MIFAREReader.MFRC522_Anticoll()
                    # If we have the UID, continue
                    block_num= 4
                    key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]


                    if status == MIFAREReader.MI_OK:
                            # Variable for the data to write        
                            # Print UID
                        #print("UID de tag: %s%s%s%s" % ('{0:x}'.format(uid[0]), '{0:x}'.format(uid[1]), '{0:x}'.format(uid[2]), '{0:x}'.format(uid[3])))
                            
                            # Select the scanned tag
                        MIFAREReader.MFRC522_SelectTag(uid)
                            # Authenticate
                        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_num, key, uid)
                            # Check if authenticated
                        
                        if status == MIFAREReader.MI_OK:
                            print("El sector 1 tenía esta información:")
                                # Read block 8
                            backdata_4 = MIFAREReader.MFRC522_Read(block_num)
                            backdata_5= MIFAREReader.MFRC522_Read(block_num+1)
                            backdata_6= MIFAREReader.MFRC522_Read(block_num+2)

                                #print(backdata)
                            read_value4=''.join([chr(number) for number in backdata_4])
                            read_value5=''.join([chr(number) for number in backdata_5])
                            read_value6=''.join([chr(number) for number in backdata_6])
                            print(block_num)
                            #print(backdata_4)
                            #print(backdata_5)
                            #print(backdata_6)
                            #print(read_value4)
                            #print(read_value5)
                            #print(read_value6)
                            
                                    #print(read_value4)
                            #s1 = "" + read_value4 + "" + read_value5 + "" + read_value6
                                    #print(read_value1)
                            GPIO.cleanup()
                            continue_reading==True
                            #print('s1', s1)
                            MIFAREReader = MFRC522()
                            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                            
                            # Scan for cards    
                            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                            # If a card is found
                            block_num2=8
                            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]


                            if status == MIFAREReader.MI_OK:
                                print("Tag detectado")
                                
                            # Get the UID of the card
                            (status,uid) = MIFAREReader.MFRC522_Anticoll()
                            # If we have the UID, continue
                            if status == MIFAREReader.MI_OK:
                                    # Variable for the data to write        
                                    # Print UID
                                #print("UID de tag: %s%s%s%s" % ('{0:x}'.format(uid[0]), '{0:x}'.format(uid[1]), '{0:x}'.format(uid[2]), '{0:x}'.format(uid[3])))
                                    
                                    # Select the scanned tag
                                MIFAREReader.MFRC522_SelectTag(uid)
                                    # Authenticate
                                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_num2, key, uid)
                                    # Check if authenticated
                                

                                if status == MIFAREReader.MI_OK:
                                    print("El sector 2 tenía esta información:")
                                        # Read block 8
                                    backdata_8 = MIFAREReader.MFRC522_Read(block_num2)
                                    
                                    backdata_9= MIFAREReader.MFRC522_Read(block_num2+1)
                                    backdata_10= MIFAREReader.MFRC522_Read(block_num2+2)

                                        #print(backdata)
                                    read_value8=''.join([chr(number) for number in backdata_8])
                                    read_value9=''.join([chr(number) for number in backdata_9])
                                    read_value10=''.join([chr(number) for number in backdata_10])
                                    print(block_num2)
                                    
                                            #print(read_value4)
                                    s2 = "" + read_value8+ "" + "" + read_value9 + "" + read_value10 + ""
                                            #print(read_value1)
                                    GPIO.cleanup()
                                    continue_reading==True
                                    #print('s2',s2)

                                    MIFAREReader = MFRC522()                                    
                                    # Scan for cards    
                                    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                                    # If a card is found
                                    if status == MIFAREReader.MI_OK:
                                        print("Tag detectado")
                                        
                                    # Get the UID of the card
                                    (status,uid) = MIFAREReader.MFRC522_Anticoll()
                                    # If we have the UID, continue
                                    block_num3= 12
                                    key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                                    if status == MIFAREReader.MI_OK:
                                            # Variable for the data to write        
                                            # Print UID
                                        #print("UID de tag: %s%s%s%s" % ('{0:x}'.format(uid[0]), '{0:x}'.format(uid[1]), '{0:x}'.format(uid[2]), '{0:x}'.format(uid[3])))
                                            
                                            # Select the scanned tag
                                        MIFAREReader.MFRC522_SelectTag(uid)
                                            # Authenticate
                                        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_num3, key, uid)
                                            # Check if authenticated
                                        if status == MIFAREReader.MI_OK:
                                            print("El sector 3 tenía esta información:")
                                                # Read block 8
                                            backdata_12 = MIFAREReader.MFRC522_Read(block_num3)
                                            backdata_13= MIFAREReader.MFRC522_Read(block_num3+1)
                                            backdata_14= MIFAREReader.MFRC522_Read(block_num3+2)

                                                #print(backdata)
                                            read_value12=''.join([chr(number) for number in backdata_12])
                                            read_value13=''.join([chr(number) for number in backdata_13])
                                            read_value14=''.join([chr(number) for number in backdata_14])
                                            print(block_num3)
                                            
                                                    #print(read_value4)
                                            #s3 = "" + read_value12 + "" + read_value13 + "" + read_value14 + ""
                                                    #print(read_value1)
                                            GPIO.cleanup()
                                            continue_reading==True
                                            #print("s3",s3)
                                            
                                            MIFAREReader = MFRC522()

                                            # Scan for cards    
                                            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                                            # If a card is found
                                            if status == MIFAREReader.MI_OK:
                                                print("Tag detectado")
                                                
                                            # Get the UID of the card
                                            (status,uid) = MIFAREReader.MFRC522_Anticoll()
                                            # If we have the UID, continue
                                            block_num4= 16
                                            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

                                            if status == MIFAREReader.MI_OK:
                                                    # Variable for the data to write        
                                                    # Print UID
                                                #print("UID de tag: %s%s%s%s" % ('{0:x}'.format(uid[0]), '{0:x}'.format(uid[1]), '{0:x}'.format(uid[2]), '{0:x}'.format(uid[3])))
                                                    
                                                    # Select the scanned tag
                                                MIFAREReader.MFRC522_SelectTag(uid)
                                                    # Authenticate
                                                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block_num4, key, uid)
                                                    # Check if authenticated
                                                

                                                if status == MIFAREReader.MI_OK:
                                                    print("El sector 4 tenía esta información:")
                                                        # Read block 8
                                                    backdata_16 = MIFAREReader.MFRC522_Read(block_num4)
                                                    backdata_17= MIFAREReader.MFRC522_Read(block_num4+1)
                                                    backdata_18= MIFAREReader.MFRC522_Read(block_num4+2)

                                                        #print(backdata)
                                                    read_value16=''.join([chr(number) for number in backdata_16])
                                                    read_value17=''.join([chr(number) for number in backdata_17])
                                                    read_value18=''.join([chr(number) for number in backdata_18])
                                                    print(block_num4)
                                                    
                                                            #print(read_value4)
                                                    #s4 ="" + read_value16 + "" + read_value17 + "" + read_value18 + ""
                                                            #print(read_value1)
                                                    GPIO.cleanup()
                                                    continue_reading==True
                                                    #print("s4",s4)
                                                    #s5="" + read_value5 + "" + read_value5 + "" + read_value6 + "" + read_value9 + "" + read_value9 + "" + read_value10 + "" + read_value13 + "" + read_value13 + "" + read_value14 + "" + read_value16 + "" + read_value17 + "" + read_value18 + ""
                                                    #s5="" + read_value4 + "" + read_value5 + "" + read_value6 + "" + read_value8 + "" + read_value9 + "" + read_value10 + "" + read_value12 + "" + read_value13 + "" + read_value14 + "" + read_value16 + "" + read_value17 + "" + read_value18
                                                    s1="" + read_value4 + "" + read_value5 + "" + read_value6 + "" + read_value8
                                                    s2="" + read_value9 + "" + read_value10 + "" + read_value12 + "" + read_value13
                                                    s3="" + read_value14 + "" + read_value16 + "" + read_value17 + "" + read_value18
                                                    s5=s1+s2+s3
                                                    #print("s4",s5)
                                                    print('JSON leído en la tarjeta 3',s5)
                                                    myMQTTClient=AWSIoTMQTTClient('Prueba')
                                                    myMQTTClient.configureEndpoint("a2l5d164bdvycm-ats.iot.us-east-2.amazonaws.com", 8883)

                                                    myMQTTClient.configureCredentials(Root_CA, Private_Key, Certificate)

                                                    myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
                                                    myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
                                                    myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
                                                    myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
                                                    print ('Initiating Realtime Data Transfer From Raspberry Pi...')
                                                    myMQTTClient.connect()
                                                                                                  
                                                    now=datetime.now()

                                                    timestamp = int(datetime.timestamp(now)*1000000)
                                                    timestamp = timestamp *100 + 3
                                                    s1=s1.replace("{","{\"Pan_1\":""{")
                                                    s2=s2.replace("{",",\"Pan_2\":""{")
                                                    s3=s3.replace("{",",\"Pan_3\":""{")
                                                    s5=s1+s2+s3
                                                    print(s5)
                                                    s5=s5.replace("\u0000","")

                                                    s5=s5.replace(" ","")
                                                    s5=s5.replace(":{",":{\"timestamp\":"+str(timestamp)+",")
                                                    s5=s5.replace("}{","},")
                                                    s5=s5.replace(s5,s5+"}")                                              

                                                    myMQTTClient.publish(
                                                    topic="iot/Panaderia_reto",
                                                    QoS=1,
                                                    payload=json.dumps(s5),
                                                    )

            if Mk.getKey('4'):

                Lect_RFID1 = 0 
                Lect_RFID2 = 0  
                Lect_RFID3 = 0
                Del_RFID1 = 0
                Del_RFID2 = 0  
                Del_RFID3 = 0
                Home_Carga = True 
                Home_Stop = 0
                Reset = 0 
                print('Tecla 4 presionada') 
                print('Cargando en Home') 
                client.publish(topic = 'L_RFID1', payload = Lect_RFID1, qos=0)
                client.publish(topic = 'L_RFID2', payload = Lect_RFID2, qos=0)       
                client.publish(topic = 'L_RFID3', payload = Lect_RFID3, qos=0)
                client.publish(topic = 'D_RFID1', payload = Del_RFID1, qos=0)
                client.publish(topic = 'D_RFID2', payload = Del_RFID2, qos=0)       
                client.publish(topic = 'D_RFID3', payload = Del_RFID3, qos=0)
                client.publish(topic = 'Home_Carga', payload = Home_Carga, qos=0)
                client.publish(topic = 'Home_Stop', payload = Home_Stop, qos=0)
                client.publish(topic = 'Reset', payload = Reset, qos=0)   

            elif Mk.getKey('5'):

                Del_RFID1 = True
                Del_RFID2 = 0  
                Del_RFID3 = 0
                Lect_RFID1 = 0 
                Lect_RFID2 = 0  
                Lect_RFID3 = 0
                Act_Robot_RFID1 = True
                Act_Robot_RFID2 = 0
                Act_Robot_RFID3 = 0
                Home_Carga = 0  
                Home_Stop = 0 
                Reset = 0
                print('Tecla 5 presionada') 
                print('Entregando a RFID 1') 
                client.publish(topic = 'L_RFID1', payload = Lect_RFID1, qos=0)
                client.publish(topic = 'L_RFID2', payload = Lect_RFID2, qos=0)       
                client.publish(topic = 'L_RFID3', payload = Lect_RFID3, qos=0)
                client.publish(topic = 'D_RFID1', payload = Del_RFID1, qos=0)
                client.publish(topic = 'D_RFID2', payload = Del_RFID2, qos=0)       
                client.publish(topic = 'D_RFID3', payload = Del_RFID3, qos=0)
                client.publish(topic = 'AR_RFID1', payload = Act_Robot_RFID1, qos=0)
                client.publish(topic = 'AR_RFID2', payload = Act_Robot_RFID2, qos=0)
                client.publish(topic = 'AR_RFID3', payload = Act_Robot_RFID3, qos=0)
                client.publish(topic = 'Home_Carga', payload = Home_Carga, qos=0)
                client.publish(topic = 'Home_Stop', payload = Home_Stop, qos=0)
                client.publish(topic = 'Reset', payload = Reset, qos=0)
                
            elif Mk.getKey('6'):

                Del_RFID1 = 0
                Del_RFID2 = True
                Del_RFID3 = 0
                Lect_RFID1 = 0 
                Lect_RFID2 = 0  
                Lect_RFID3 = 0
                Act_Robot_RFID1 = 0
                Act_Robot_RFID2 = True
                Act_Robot_RFID3 = 0
                Home_Carga = 0  
                Home_Stop = 0
                Reset = 0
                print('Tecla 6 presionada') 
                print('Entregando a RFID 2') 
                client.publish(topic = 'L_RFID1', payload = Lect_RFID1, qos=0)
                client.publish(topic = 'L_RFID2', payload = Lect_RFID2, qos=0)       
                client.publish(topic = 'L_RFID3', payload = Lect_RFID3, qos=0)
                client.publish(topic = 'D_RFID1', payload = Del_RFID1, qos=0)
                client.publish(topic = 'D_RFID2', payload = Del_RFID2, qos=0)       
                client.publish(topic = 'D_RFID3', payload = Del_RFID3, qos=0)
                client.publish(topic = 'AR_RFID1', payload = Act_Robot_RFID1, qos=0)
                client.publish(topic = 'AR_RFID2', payload = Act_Robot_RFID2, qos=0)
                client.publish(topic = 'AR_RFID3', payload = Act_Robot_RFID3, qos=0)
                client.publish(topic = 'Home_Carga', payload = Home_Carga, qos=0)
                client.publish(topic = 'Home_Stop', payload = Home_Stop, qos=0)
                client.publish(topic = 'Reset', payload = Reset, qos=0)
            
            elif Mk.getKey('7'):

                Del_RFID1 = 0
                Del_RFID2 = 0
                Del_RFID3 = True
                Lect_RFID1 = 0 
                Lect_RFID2 = 0  
                Lect_RFID3 = 0
                Act_Robot_RFID1 = 0
                Act_Robot_RFID2 = 0
                Act_Robot_RFID3 = True
                Home_Carga = 0  
                Home_Stop = 0
                Reset = 0
                print('Tecla 7 presionada') 
                print('Entregando a RFID 3') 
                client.publish(topic = 'L_RFID1', payload = Lect_RFID1, qos=0)
                client.publish(topic = 'L_RFID2', payload = Lect_RFID2, qos=0)       
                client.publish(topic = 'L_RFID3', payload = Lect_RFID3, qos=0)
                client.publish(topic = 'D_RFID1', payload = Del_RFID1, qos=0)
                client.publish(topic = 'D_RFID2', payload = Del_RFID2, qos=0)       
                client.publish(topic = 'D_RFID3', payload = Del_RFID3, qos=0)
                client.publish(topic = 'AR_RFID1', payload = Act_Robot_RFID1, qos=0)
                client.publish(topic = 'AR_RFID2', payload = Act_Robot_RFID2, qos=0)
                client.publish(topic = 'AR_RFID3', payload = Act_Robot_RFID3, qos=0)
                client.publish(topic = 'Home_Carga', payload = Home_Carga, qos=0)
                client.publish(topic = 'Home_Stop', payload = Home_Stop, qos=0)
                client.publish(topic = 'Reset', payload = Reset, qos=0)

            elif Mk.getKey('p'):

                Del_RFID1 = 0
                Del_RFID2 = 0
                Del_RFID3 = 0
                Lect_RFID1 = 0 
                Lect_RFID2 = 0  
                Lect_RFID3 = 0
                Act_Robot_RFID1 = 0
                Act_Robot_RFID2 = 0
                Act_Robot_RFID3 = 0
                Home_Carga = 0  
                Home_Stop = True
                Reset = 0
                print('Tecla 8 presionada') 
                print('Regresando a Home') 
                client.publish(topic = 'L_RFID1', payload = Lect_RFID1, qos=0)
                client.publish(topic = 'L_RFID2', payload = Lect_RFID2, qos=0)       
                client.publish(topic = 'L_RFID3', payload = Lect_RFID3, qos=0)
                client.publish(topic = 'D_RFID1', payload = Del_RFID1, qos=0)
                client.publish(topic = 'D_RFID2', payload = Del_RFID2, qos=0)       
                client.publish(topic = 'D_RFID3', payload = Del_RFID3, qos=0)
                client.publish(topic = 'AR_RFID1', payload = Act_Robot_RFID1, qos=0)
                client.publish(topic = 'AR_RFID2', payload = Act_Robot_RFID2, qos=0)
                client.publish(topic = 'AR_RFID3', payload = Act_Robot_RFID3, qos=0)
                client.publish(topic = 'Home_Carga', payload = Home_Carga, qos=0)
                client.publish(topic = 'Home_Stop', payload = Home_Stop, qos=0)
                client.publish(topic = 'Reset', payload = Reset, qos=0)

            elif Mk.getKey('r'):

                Lect_RFID1 = 0 
                Lect_RFID2 = 0  
                Lect_RFID3 = 0
                Del_RFID1 = 0
                Del_RFID2 = 0
                Del_RFID3 = 0
                Act_Robot_RFID1 = 0
                Act_Robot_RFID2 = 0
                Act_Robot_RFID3 = 0
                Home_Carga = 0  
                Home_Stop = 0
                Reset = 1
                print('Tecla Reset presionada') 
                client.publish(topic = 'L_RFID1', payload = Lect_RFID1, qos=0)
                client.publish(topic = 'L_RFID2', payload = Lect_RFID2, qos=0)       
                client.publish(topic = 'L_RFID3', payload = Lect_RFID3, qos=0)
                client.publish(topic = 'D_RFID1', payload = Del_RFID1, qos=0)
                client.publish(topic = 'D_RFID2', payload = Del_RFID2, qos=0)       
                client.publish(topic = 'D_RFID3', payload = Del_RFID3, qos=0)
                client.publish(topic = 'AR_RFID1', payload = Act_Robot_RFID1, qos=0)
                client.publish(topic = 'AR_RFID2', payload = Act_Robot_RFID2, qos=0)
                client.publish(topic = 'AR_RFID3', payload = Act_Robot_RFID3, qos=0)
                client.publish(topic = 'Home_Carga', payload = Home_Carga, qos=0)
                client.publish(topic = 'Home_Stop', payload = Home_Stop, qos=0)
                client.publish(topic = 'Reset', payload = Reset, qos=0)

if __name__ == '__main__':
    while True:
        main()

        ###  Cfg GPIO  ###
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        ###  Cfg Motor 1  ###
        ENA1,IN1,IN2 = 13,3,5
        GPIO.setup(IN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.setup(ENA1, GPIO.OUT)

        #GPIO.output(IN1, True)
        #GPIO.output(IN2, False)

        # # Cambiar Velocidad Motor 1
        #PWMA.ChangeDutyCycle(100)
        #     GPIO.output(ENA1, True)

        ###  Cfg Motor 2  ###
        ENA2,IN3,IN4 = 35,33,37
        GPIO.setup(IN3, GPIO.OUT)
        GPIO.setup(IN4, GPIO.OUT)
        GPIO.setup(ENA2, GPIO.OUT)

        

        if Mk.getKey('UP'):

            PWMA.ChangeDutyCycle(100)
            PWMB.ChangeDutyCycle(100)
            GPIO.output(IN1, True)
            GPIO.output(IN2, False)
            GPIO.output(IN3, True)
            GPIO.output(IN4, False)
        
            # sleep(TX) Usar para avanzar por X Tiempo
            print('Tecla ARRIBA presionada')

        elif Mk.getKey('DOWN'):

            PWMA.ChangeDutyCycle(100)
            PWMB.ChangeDutyCycle(100)
            GPIO.output(IN1, False)
            GPIO.output(IN2, True)
            GPIO.output(IN3, False)
            GPIO.output(IN4, True)
        
            # sleep(TX) Usar para avanzar por X Tiempo
            print('Tecla ABAJO presionada')

        elif Mk.getKey('LEFT'):

            PWMA.ChangeDutyCycle(10)
            PWMB.ChangeDutyCycle(100)
            GPIO.output(IN1, False)
            GPIO.output(IN2, False)
            GPIO.output(IN3, True)
            GPIO.output(IN4, False)
        
            # sleep(TX) Usar para avanzar por X Tiempo
            print('Tecla IZQUIERDA presionada')

        elif Mk.getKey('RIGHT'):

            PWMA.ChangeDutyCycle(100)
            PWMB.ChangeDutyCycle(10)
            GPIO.output(IN1, True)
            GPIO.output(IN2, False)
            GPIO.output(IN3, False)
            GPIO.output(IN4, False)
        
            # sleep(TX) Usar para avanzar por X Tiempo
            print('Tecla DERECHA presionada')

        elif Mk.getKey('x'):

            servo.ChangeDutyCycle(2)
            sleep(0.5)
            servo.ChangeDutyCycle(0)       

            print('Servo Derecha') 

        elif Mk.getKey('c'):

            duty = 1

            while duty <= 7:
                servo.ChangeDutyCycle(duty)
                duty = duty + 1
                #sleep(0.1)

            # sleep(TX) Usar para avanzar por X Tiempo
            print('Centro Servo')        

        elif Mk.getKey('v'):

            duty = 1

            while duty <= 12:
                servo.ChangeDutyCycle(duty)
                duty = duty + 1
                #sleep(0.1)

                print('Servo Izquierda') 

        elif Mk.getKey('b'):

            duty = 1

            while duty <= 3:
                servo2.ChangeDutyCycle(duty)
                duty = duty + 1
                #sleep(0.1)

            # sleep(TX) Usar para avanzar por X Tiempo
            print('Arriba Servo 2')    
        
        elif Mk.getKey('n'):

            duty = 1

            while duty <= 5:
                servo2.ChangeDutyCycle(duty)
                duty = duty + 1
                #sleep(0.1)

                print('Centro Servo 2') 

        elif Mk.getKey('m'):

            duty = 1

            while duty <= 7:
                servo2.ChangeDutyCycle(duty)
                duty = duty + 1
                #sleep(0.1)

                print('Abajo Servo 2') 

        else:

            servo.ChangeDutyCycle(0)
            servo2.ChangeDutyCycle(0)
            PWMA.ChangeDutyCycle(0)
            PWMB.ChangeDutyCycle(0)
            GPIO.output(IN1, False)
            GPIO.output(IN2, False)
            GPIO.output(IN3, False)
            GPIO.output(IN4, False)


client.loop_forever()              
                                                
