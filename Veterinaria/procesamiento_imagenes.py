import cv2


def detectar_imagen(img_path , tipo_animal):
    # el problema de esta dnn es que tiene pocos animales y detecta otras cosas
    net = cv2.dnn.readNet("dnn_model\yolov4-tiny.weights","dnn_model\yolov4-tiny.cfg")
    model = cv2.dnn.DetectionModel(net)
    model.setInputParams(size=(320,320), scale=1/255)

    
    clases = []
    with open ('dnn_model\classes.txt') as objeto_archivo:
        for nombre_clase in objeto_archivo.readlines():
            nombre_clase = nombre_clase.strip()
            clases.append(nombre_clase)
    

    clases_esp = {"perro":"dog", "pajaro":"bird", "gato":"cat", "caballo":"horse", "oveja":"sheep", "vaca":"cow"}
    tipo_animal = tipo_animal.lower()

    img = cv2.imread(img_path)
    (id_clase,puntaje,caja) = model.detect(img)

    flag_detectar = False
    flag_coincidencia = False
    
    if len(id_clase) == 0:
        flag_detectar = False
    else:
        flag_detectar = True
        if clases[id_clase[0]] == clases_esp[tipo_animal]:
            flag_coincidencia = True
        else:
            flag_coincidencia = False
    
    return flag_detectar, flag_coincidencia


#print(detectar_imagen('Media\perro_gato.jpg', "perro"))
#detectar_imagen('Media\perro_gato.jpg', "perro")
