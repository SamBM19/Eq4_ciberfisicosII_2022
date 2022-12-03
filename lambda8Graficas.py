#EQUIPO4_CIBERFISICOS_II
#Lambda para las graficas de ventas de las 3 sucursales y en general
#Son un total de 8 graficas que se guardan en un bucket de s3

#Librerias
import json
import boto3
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO, BytesIO
import matplotlib.colors as mcolors
from boto3.dynamodb.conditions import Key

#Main del evento
#Este evento tiene un trigger con iot_core regla(mqtt_graficas) el mensaje que llegue por mqtt desencadena esta funcion
def lambda_handler(event, context):
    #Imprime el evento
    print(event)
    body = json.loads(event)
    
    #Informacion que se va a analizar segun la sucursal, ventas, fechas y los ingresos
    fecha = body['Pan_1']['Fecha']
    txt_sucursal = str(body['Pan_1']["timestamp"])[-2:]
    Info_PaAnalizar = [body['Pan_1'],body['Pan_2'],body['Pan_3']]
    x_panes, x_ingresos = Info_Sucursal(Info_PaAnalizar)
    y = np.array(['Dona', 'Oreja', 'Concha', 'Muffin', 'Bolillo'],dtype=('U9'))
    
    #Path pa guardar en s3 con distintas carpetas segun la fecha y sucursal
    Path_PaGuardar ='Ventas/Sucursal-'+txt_sucursal+'/'
    Path_PaGuardar_Fecha = Path_PaGuardar+fecha+'/'
    Venta_Sucursal ='Panes vendidos por la Sucursal'+txt_sucursal+' el dia '+fecha
    
    #Todo pa graficar los datos...
    Ingresos_Por_Sucursal(x_ingresos,y,'Ingreso por los'+Venta_Sucursal,Path_PaGuardar_Fecha+'panes')
    Ingresos_Por_Sucursal(x_panes,y,'Número de' +Venta_Sucursal,Path_PaGuardar_Fecha+'Ventas')
    ventas_hasta_ahora = GET_Completo()
    panes_ventas,ingresos_completos,dias=Orden_Por_Fecha(ventas_hasta_ahora)
    panes_organi = Info_Graficar(panes_ventas)
    panes_organi = np.array(panes_organi,dtype=np.int8)
    ingresos_ordenados = Info_Graficar(ingresos_completos)
    ingresos_ordenados = np.array(ingresos_ordenados,dtype=np.float32)
    plotear_histogramas(panes_organi,panes_ventas,dias,'Ventas/Ingresos-total','Número de panes vendidos')
    plotear_histogramas(ingresos_ordenados,ingresos_completos,dias,'Ventas/Ventas-total','Ingreso por los panes vendidos')
    #comprobar con un msj de ooook
    return {
        'statusCode': 200,
        'body': json.dumps('Todo marcha bien')
    }
        
#Funcion para organizar con fecha los panes que se vendieron. Todo se tiene que ir sumando segun las ventas...
def Orden_Por_Fecha(items):
    panes = ['Dona', 'Oreja', 'Concha', 'Muffin', 'Bolillo']
    costos= [12.5, 14.5, 9.5, 13.5, 3.5]
    dias = []
    panes_ventas = []
    ingresos = []

    for i in range(len(items)):
        if items[i]['Fecha'] not in dias:
            print('Se anade la informacion...')
            print(items[i]['Fecha'])
            print('Sucursal: ' +str(items[i]['ts'])[-2:])
            dias.append(items[i]['Fecha'])
            panes_ventas.append([0,0,0,0,0])
            ingresos.append([0,0,0,0,0])      
    dias.append('')
    for i in range(len(items)):
        panes_ventas[dias.index(items[i]['Fecha'])][panes.index(items[i]['Pan'])]+=int(items[i]['Can'])
        ingresos[dias.index(items[i]['Fecha'])][panes.index(items[i]['Pan'])]+=int(items[i]['Can'])*costos[panes.index(items[i]['Pan'])]
    panes_ventas=np.array(panes_ventas,dtype=np.int8)
    ingresos=np.array(ingresos,dtype=np.float32)
    return panes_ventas,ingresos,dias

#Info pa graficar
def Info_Graficar(panes):
    datos = []
    for j in range(len(panes)):
        Total_De_Panes=panes[j].sum()
        datos.append([])
        for i in range(5):
            datos[j].append(Total_De_Panes)
            Total_De_Panes-=panes[j][i]
    return datos

#Sacar los items completos de la tabla  
def GET_Completo():
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table("panaderia_reto1")
    response = table.scan()
    return response['Items']
    
#Informacion segun las ventas de cada sucursal 01,02,03...    
def Info_Sucursal(body):
    Sucursales=[0,0,0,0,0]
    Ventas_Totales=[0,0,0,0,0]
    for i in range(len(body)):
        info=(body[i])
        panes = ['Dona', 'Oreja', 'Concha', 'Muffin', 'Bolillo']
        costos= [12.5, 14.5, 9.5, 13.5, 3.5]
        Sucursales[panes.index(info["Pan"])]=int(info["Can"])
        Ventas_Totales[panes.index(info["Pan"])]=int(info["Can"])*costos[panes.index(info["Pan"])]
        Sucursales=np.array(Sucursales,dtype=np.int8)
        Ventas_Totales=np.array(Ventas_Totales,dtype=np.float32)
    return Sucursales,Ventas_Totales

#Plot de los ingresos por sucursal...        
def Ingresos_Por_Sucursal(x,y,name,out_key):
    colores= ['violet','gold','papayawhip','aqua','lime']#los cambiamos?
    fig, ax = plt.subplots()
    ax.bar(y,x, color = mcolors.CSS4_COLORS['hotpink'],edgecolor="black")
    if name[:7]=='Ingreso':
        print('1')
        y_label='Ingreso en pesos mx'
        before_text='Total: $'
        print(name[-2:])
    elif name[:6]=='Número':
        print('2')
        y_label='Número de panes'
        before_text='Cantidad: '
        print(name[39:41])
    for i in range(len(x)):
        ax.text(x=y[i] , y=x[i]+x[x.argmax(axis=0)]*.02, s=before_text+str(x[i]),ha="center")
    ax.set_title(name, fontdict = {'fontsize':10, 'fontweight':'bold', 'color':mcolors.CSS4_COLORS['black']})
    ax.set_ylim(0, x[x.argmax(axis=0)]*1.1)
    plt.xlabel('Pan', fontdict = {'fontsize':9, 'color':mcolors.CSS4_COLORS['grey']})
    plt.ylabel(y_label, fontdict = {'fontsize':9, 'color':mcolors.CSS4_COLORS['grey']})
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    Guardar_El_Plot(img_data,out_key)
    
#Graficar...
def plotear_histogramas(panes_organi,panes_ventas,dias,out_key,name):
    colores= ['violet','gold','papayawhip','aqua','lime']
    panes = ['Dona', 'Oreja', 'Concha', 'Muffin', 'Bolillo']

    find_max=np.where(panes_organi == np.amax(panes_organi))
    max_value=panes_organi[find_max[0],find_max[1]]
    fig, ax = plt.subplots()
    
    if name[:7]=='Ingreso':
        print('1')
        y_label='Ingreso en pesos mx'
        before_text='Total: $'
        #ruta='Ventas/Sucursal
        print(name[-2:])
    elif name[:6]=='Número':
        print('2')
        y_label='Número de panes'
        before_text='Can: '
    for j in range(5):
        a=[]
        for i in range(len(panes_organi)):
            a.append(panes_organi[i][j])
            if j==0:
                ax.text(x=dias[i] , y=panes_organi[i][j]+max_value*.02, s=before_text+str(panes_organi[i][j]),ha="center")
            print(panes_organi[i][j])
            if panes_ventas[i][j]!=0:
                ax.text(x=dias[i] , y=panes_organi[i][j]-max_value*.04, s=panes[j]+': '+str(panes_ventas[i][j]),ha="center")
        a.append(0)
        ax.bar(dias,a,color=colores[j],edgecolor="black")
        print(a)
    ax.set_ylim(0, max_value*1.1)
    plt.xlabel('Día de venta', fontdict = {'fontsize':9, 'color':mcolors.CSS4_COLORS['hotpink']})
    plt.ylabel(y_label, fontdict = {'fontsize':9, 'color':mcolors.CSS4_COLORS['hotpink']})
    ax.set_title('Número de panes por fecha de venta', fontdict = {'fontsize':10, 'fontweight':'bold', 'color':mcolors.CSS4_COLORS['black']})
    ax.legend(panes,bbox_to_anchor=(1, 1))
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    Guardar_El_Plot(img_data,out_key)

#Funcion para guardar el plot ya dentro de s3
def Guardar_El_Plot(img_data,out_key):
    s3 = boto3.client('s3')
    #Buckest en el que se va a guardar... no olvidar dar full access a esta lambda para editar s3
    out_bucket='graficarventas'
    bucket = boto3.resource('s3').Bucket(out_bucket)
    bucket.put_object(Body=img_data, ContentType='image/png', Key=(out_key+'.png'))