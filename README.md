# todo-list-aws

Este proyecto contiene un ejemplo de solución **SAM + Jenkins**. Contiene una aplicación API RESTful de libreta de tareas pendientes (ToDo) y los pipelines que permiten definir el CI/CD para productivizarla.

## Estructura

A continuación se describe la estructura del proyecto:
- **pipelines** - pipelines de Jenkins que permiten construir el CI/CD
- **src** - en este directorio se almacena el código fuente de las funciones lambda con las que se va a trabajar
- **test** - Tests unitarios y de integración. 
- **samconfig.toml** - Configuración de los stacks de Staging y Producción
- **template.yaml** - Template que define los recursos AWS de la aplicación
- **localEnvironment.json** - Permite el despliegue en local de la aplicación sobreescribiendo el endpoint de dynamodb para que apunte contra el docker de dynamo

## Despliegue manual de la aplicación SAM en AWS

Para utilizar SAM CLI se necesitan las siguientes herramientas:

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/) - Se ha testeado con Python 3.7
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

Para una ejecución en local una vez se tenga instaladas las herramientas anteriores realizar las siguientes acciones:

### Comprobar redes en docker:
```bash
docker network ls
```
Ejemplo de ejecución:
:~/todo-list-aws (feature) $ docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
ae8ab5a5d353   bridge    bridge    local
0573a8e94ae8   host      host      local
bf277213565e   none      null      local

### Create red docker:
```bash
docker network create sam
```

### Ver detalle de la red docker:
```bash
docker network inspect sam
```

### Bajada de la imagen docker de dynamodb:
```bash
docker pull amazon/dynamodb-local
```

### Comprobar imagen docker dynamodb una vez bajada:
```bash
docker images
```

Ejemplo de ejecución:
:~ $ docker images
REPOSITORY              TAG       IMAGE ID       CREATED        SIZE
amazon/dynamodb-local   latest    904626f640dc   47 hours ago   499MB
:~ $

### Ejecutar docker imagen dynamodb:
```bash
docker run -p 8000:8000 --name dynamodb --network sam -d amazon/dynamodb-local
```

### Comprobar contenedor dynamodb corriendo:
```bash
docker ps
```

Ejemplo de ejecución:
:~/todo-list-aws (feature) $ docker ps
CONTAINER ID   IMAGE                   COMMAND                  CREATED         STATUS         PORTS                                       NAMES
936b326e0988   amazon/dynamodb-local   "java -jar DynamoDBL…"   2 minutes ago   Up 2 minutes   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   dynamodb
:~/todo-list-aws (feature) $

Una vez que el contenedor de la persistencia de la API Dynamodb está ejecutándose se debe de crear las tablas de la API con:

### Crear la tabla en Dynamodb en local, para poder trabajar localmemte
```bash
aws dynamodb create-table --table-name local-TodosDynamoDbTable --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --endpoint-url http://localhost:8000 --region us-east-1
```

### Construir la aplicación con el siguiente comando:
```bash
sam build
```
Este comando construye la aplicación serverless y la prepara para los siguientes pasos hasta completar el flujo de despliegue. El comando genera en el raíz de la aplicación una subcarpeta .aws-sam con todo lo relativo al proyecto serverless teniendo en cuenta el contenido de ficheros de configuración como requirements.txt en csao de proyecto python.

### Levantar la api en local, en el puerto 8080, dentro de la red de docker sam
```bash
sam local start-api --port 8081 --env-vars localEnvironment.json --docker-network sam
sam local start-api --port 8081 --env-vars localEnvironment.json --docker-network sam --debug --invoke-image amazon/aws-sam-cli-emulation-image-python3.7

```

Esto levanta un servicio demonio http por el puerto 8081, que se cierra con Ctrl+C


Otros comandos que pueden ser de ayuda:
### Detener contenedor:
```bash
docker stop dynamodb
```

Recomendable realizarlo antes de detener la instancia S3.

### Arrancar contenedor (detenido con anterioridad):
```bash
docker start dynamodb
```

Nota: si el contendor se elimina se debe de volver a ejecutar la creación de las tablas de la API

### Ver todos los contenedores (corriendo y detenidos):
```bash
docker ps -a
```

### Eliminar contenedor (no imagen):
```bash
docker rm dynamodb
```

### Para comprobar la configuración de AWS CLI, por ejemplo para ver si está configurado con credenciales:
```bash
aws configure list
```

### Para especificar las credenciales:
```bash
aws configure
```

Este menú solicita el AWS Acces Key ID, AWS Secret Access Key, Default region name y Default output format de un usuario creado en AWS.

Ejemplo de ejecución:
:~/todo-list-aws (feature) $ aws configure
AWS Access Key ID [None]: AKIAUNBGN4AV3FGB6WGZ
AWS Secret Access Key [None]: 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
Default region name [None]: us-east-1
Default output format [None]:
:~/todo-list-aws (feature) $



### Para **validar** el AWS SAM template file ejecutar:
```bash
sam validate
```

### Desplegar la aplicación por primera vez:
sam deploy

Sin utilizar la configuración del archivo samconfig.toml. Se generará un archivo de configuración reemplazando al actual si ya existe.
Ejecutar el siguiente comando:
```bash
sam deploy --guided
```

El despliegue de la aplicación empaqueta, publicará en un bucket s3 el artefacto y desplegará la aplicación en AWS. Solicitará la siguiente información

* **Stack Name**: El nombre del stack que desplegará en CloudFormation. Debe ser único
* **AWS Region**: La región en la que se desea publicar la Aplicación.
* **Confirm changes before deploy**: Si se indica "yes" se solicitará confirmación antes del despliegue si se encuentran cambios 
* **Allow SAM CLI IAM role creation**: Permite la creación de roles IAM
* **Save arguments to samconfig.toml**: Si se selecciona "yes" las respuestas se almacenarán en el fichero de configuración samconfig.toml, de esta forma el el futuro se podrá ejecutar con `sam deploy` y se leerá la configuración del fichero.

En el output del despliegue se devolverá el API Gateway Endpoint URL

### Desplegar la aplicación con la configuración de **samconfig.toml**:
Revisar el fichero samconfig.toml
```bash
vim samconfig.toml
```
Ejecutar el siguiente comando para el entorno de **default**. Nota: usar este para pruebas manuales y dejar el resto para los despliegues con Jenkins.
```bash
sam deploy template.yaml --config-env default
```
Ejecutar el siguiente comando para el entorno de **staging**
```bash
sam deploy template.yaml --config-env staging
```
Ejecutar el siguiente comando para el entorno de **producción**
```bash
sam deploy template.yaml --config-env prod
```

## Despliegue manual de la aplicación SAM en local











## comprobación de puerto 8000 (dynamodb) y 8081 (server local lambda) están en el servidor atendiendo:

netstat -tulpn

Ejemplo de salida esperada:

:~/todo-list-aws (feature) $ netstat -tulpn
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.1:8081          0.0.0.0:*               LISTEN      10997/sam
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:6010          0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:6011          0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:8000            0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -
tcp6       0      0 :::8080                 :::*                    LISTEN      -
tcp6       0      0 :::80                   :::*                    LISTEN      -
tcp6       0      0 :::22                   :::*                    LISTEN      -
tcp6       0      0 ::1:6010                :::*                    LISTEN      -
tcp6       0      0 ::1:6011                :::*                    LISTEN      -
tcp6       0      0 :::8000                 :::*                    LISTEN      -
udp        0      0 127.0.0.53:53           0.0.0.0:*                           -
udp        0      0 172.31.8.234:68         0.0.0.0:*                           -
:~/todo-list-aws (feature) $

## Instalación de jq para formatear la salida json en las peticiones curl:
sudo apt install jq


## Ejecución en local de todas las llamadas a la API:

Create:
curl -s -X POST http://127.0.0.1:8081/todos --data '{ "text": "Learn Serverless" }' | jq .

List:
curl -s http://127.0.0.1:8081/todos | jq .

Get:
curl -s http://127.0.0.1:8081/todos/<id> | jq .

Update:
curl -s -X PUT http://127.0.0.1:8081/todos/<id> --data '{ "text": "Learn Serverless", "checked": true }' | jq .

Delete:
curl -s -X DELETE http://127.0.0.1:8081/todos/<id>  

## Ejecución a servicio provisto en AWS de todas las llamadas a la API:

Create:
curl -X POST https://fwodikget1.execute-api.us-east-1.amazonaws.com/Prod/todos --data '{ "text": "Learn Serverless" }' | jq .

List:
curl https://fwodikget1.execute-api.us-east-1.amazonaws.com/Prod/todos | jq .

Get:
curl https://fwodikget1.execute-api.us-east-1.amazonaws.com/Prod/todos/<id> | jq .

Update:
curl -X PUT https://fwodikget1.execute-api.us-east-1.amazonaws.com/Prod/todos/<id> --data '{ "text": "Learn Serverless", "checked": true }' | jq .

Delete:
curl -X DELETE https://fwodikget1.execute-api.us-east-1.amazonaws.com/Prod/todos/<id>  



## Consultar logs de las funciones lambda

Se pueden consultar en CloudWath o ejecutando un comando similar al siguiente:
```bash
sam logs -n GetTodoFunction --stack-name todo-list-aws-staging
sam logs -n GetTodoFunction --stack-name todo-list-aws
```





## Tests

Se encuentran en la carpeta `test` que tiene la siguiente estructura:
```
- test
|--- integration (tests de integración)
|       -- todoApiTest.py
|--- unit (tests unitarios)
|       -- TestToDo.py
```
Para ejecutar los tests **unitarios** y de **integración** es necesario ejecutar los siguientes comandos:
```bash
# Ejecución Pruebas #

## Especificar el BASE_URL
export BASE_URL=https://<<id-api-rest>>.execute-api.us-east-1.amazonaws.com/Prod
export BASE_URL="https://e3h5d34ul6.execute-api.us-east-1.amazonaws.com/Prod"

aws sts get-session-token \
    --duration-seconds 900 \
    --serial-number "YourMFADeviceSerialNumber" \
    --token-code 123456
    
export AWS_ACCESS_KEY_ID=AKIAUNBGN4AVQJGMVFOO
export AWS_SECRET_ACCESS_KEY=1imBCmRfR3PItwx/PoGpzuVWfZPunnxlnJlfKULF
export AWS_SESSION_TOKEN=

aws sts assume-role --role-arn arn:aws:iam::123456789012:role/role-name --role-session-name "RoleSession1" --profile IAM-user-name > assume-role-output.txt
aws sts assume-role --role-arn arn:aws:iam::302875795499:role/LabRole --role-session-name "LabRole" --profile DevelopersGroupLabDevopsCloud > assume-role-output.txt

arn:aws:iam::302875795499:user/developer


## Configuración del entorno virtual ##
pipelines/PIPELINE-FULL-STAGING/setup.sh

## Pruebas unitarias ##
pipelines/PIPELINE-FULL-STAGING/unit_test.sh

## pruebas estáticas (seguridad, calidad, complejidad ) ##
pipelines/PIPELINE-FULL-STAGING/static_test.sh

## Pruebas de integración ##
# Si las pruebas de integración son contra sam local será necesario exportar la siguiente URL:
export BASE_URL="http://localhost:8081"
# Si las pruebas de integración son contra el api rest desplegado en AWS, será necesario exportar la url del API:
export BASE_URL="https://<<id-api-rest>>.execute-api.us-east-1.amazonaws.com/Prod
pipelines/common-steps/integration.sh $BASE_URL
```

## Pipelines

Para la implementación del CI/CD de la aplicación se utilizan los siguientes Pipelines:
*	**PIPELINE-FULL-STAGING**: (PIPELINE-FULL-STAGING/Jenkinsfile) Este pipeline es el encargado de configurar el entorno de staging y ejecutar las pruebas
*	**PIPELINE-FULL-PRODUCTION**: (PIPELINE-FULL-PRODUCTION/Jenkinsfile) Este pipeline es el encargado de configurar el entorno de production y ejecutar las pruebas
*	**PIPELINE-FULL-CD**: este pipeline es el encargado de enganchar los pipelines de staging y production,  con el objetivo de completar un ciclo de despliegue continuo desde un commit al repositorio de manera automática.


## Limpieza

Para borrar la apliación y eliminar los stacks creados ejecutar los siguientes comandos:

```bash
aws cloudformation delete-stack --stack-name todo-list-aws-staging
aws cloudformation delete-stack --stack-name todo-list-aws-production
```

