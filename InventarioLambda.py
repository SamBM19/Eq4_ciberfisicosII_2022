#EQUIPO4_CIBERFISICOS_II
#Lambda para actualizar la tabla de inventario, con la lectura de los TAGS.
import json
import boto3
from decimal import Decimal

#Tablas de dynamoDB que estamos utilizando
tabla_ventas = "panaderia_reto1"
tabla_inventario = "inventario_equipo4"

#Main del evento
#Este evento tiene un trigger con iot_core (MQTT_to_lambda) el mensaje que llegue por mqtt desencadena esta funcion
def lambda_handler(event, context):
    #Info del evento
    print(event)
    body=json.loads(event)
    print(body["Pan_1"])
    print(len(body))
    
    for i in range(len(body)):
        info=body["Pan_"+str(i+1)]
        #Para cada mensaje vemos la informacion del tag, o sea el json que llega via mqtt
        print("Informacion que llega: "+ str(info))
        print("Panes vendidos: " +str(info["Can"]))
        #La info se guarda en la tabla de ventas
        PUT_Item_DeVenta(info)
        #Obtenemos la informacion del tipo de pan 
        existencia=GET_Item(info['Pan'])
        #Obtenemos la informacion del inventario
        print("Existencia en el inventario: "+ str(existencia["Can"]))
        print(int(existencia['Can'])-int(info['Can']))
        UPDATE_Item_DeInventario(info,existencia)
    #comprobar con un msj de ooook
    return {
        'statusCode': 200,
        'body': json.dumps('Todo marcha bien')
    }

#Funcion para obtener un dato de la tabla de inventario, en este caso el key.
def GET_Item(pan):
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(tabla_inventario)
    response = table.get_item(
        Key={
            "Pan":pan,
        }
    )
    return response["Item"]

#Funcion para poner los items en la tabla de ventas
def PUT_Item_DeVenta(event_body):
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(tabla_ventas)
    response = table.put_item(
        #atributos de la tabla 
        Item={
            "ts": int(event_body['timestamp']),
            "Pan": event_body['Pan'],
            "Precio": Decimal(event_body['Precio']),
            "Fecha": event_body['Fecha'],
            "Can": event_body['Can']
        }
    )

#Funcion para restar la venta realizada en la tabla del inventario de panes   
def UPDATE_Item_DeInventario(ventas,inventario):
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(tabla_inventario)
    print(inventario['Pan']) 
    response = table.put_item(
        Item={
            "Pan": inventario['Pan'],
            "Precio": inventario['Precio'],
            "Can": int(inventario['Can'])-int(ventas['Can'])
        }
    )


