import RPi.GPIO as GPIO   
GPIO.setmode(GPIO.BCM)  # choose BCM numbering scheme.  

ENA1,IN1,IN2 = 12,3,5
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA1, GPIO.OUT)

PWMA = GPIO.PWM(ENA1, 100)
PWMA.start(0)
   
GPIO.setup(12, GPIO.OUT)# set GPIO 17 as output for white led  

   
hz = input('Please define the frequency in Herz(recommended:75): ')
reddc = input('Please define the red LED Duty Cycle: ')

 
red = GPIO.PWM(12, 75)    # create object red for PWM on port 17  


try:   
    while True:
            red.start((95/2.55))   #start red led
       
  
except KeyboardInterrupt:
        red.stop()   #stop red led
      
        GPIO.cleanup() 