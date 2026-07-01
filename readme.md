Proyecto Petshop
Integrantes:
Axel Sanchez Dinarte C5J641
David Madrigal Gomez C5G685
Yerlin Oviedo Castro C5I097

Problema:
Adopción de mascotas. En este sistema tenemos pensado resolver el problema de mala
gestión que tiene una tienda de adopción, ya que los diferentes datos que manejan están
dispersos al trabajar con solo archivos físicos. Por lo tanto, el sistema que vamos a preparar
tiene pensado resolver esta falla y hacer un sistema digital con interfaz web más
amigable para los trabajadores y clientes con un manejo de datos más apropiado.

Descripción del Sistema Web
1. Arquitectura del Sistema
El sistema se basa en una arquitectura desacoplada de tipo Cliente-Servidor, estructurada en dos componentes principales:
    •	Frontend Web: Una interfaz de usuario reactiva, intuitiva y responsive (adaptable a dispositivos móviles y de escritorio), diseñada para optimizar la   experiencia de usuario (UX).
    •	Backend (API REST): Un componente centralizado encargado de procesar la lógica de negocio, aplicar validaciones estrictas de seguridad y datos, y gestionar la persistencia de la información mediante solicitudes HTTP en formato JSON.
    •	Base de Datos: Un motor relacional (RDBMS) que garantiza la integridad, consistencia y el almacenamiento seguro de los datos.

2. Módulos Principales
Para resolver la problemática del manejo deficiente, descentralizado o inseguro de los datos, el sistema se divide de forma modular:
    •	Clientes: Control y registro de los datos personales y de contacto de los usuarios.
    •	Mascotas: Gestión del inventario de animales disponibles y características.
    •	Servicios: Administración de las prestaciones adicionales ofrecidas por el negocio.
    •	Adopciones y Solicitudes: Automatización y seguimiento del flujo de adopción, desde la petición inicial del cliente hasta la aprobación final, garantizando la trazabilidad del proceso.
    •	Usuarios: Módulo de autenticación y control de acceso basado en roles (ej. Administrador, Cliente) para asegurar los datos.

3. Propósito y Solución
    Este proyecto surge para erradicar el impacto negativo de una gestión de datos deficiente. Mediante la centralización de la información en los módulos mencionados, se logra un ecosistema digital fluido, funcional y eficiente.
    La plataforma ofrece una solución web integral con un doble beneficio:
    1.	Administración eficiente: Optimiza las tareas operativas de los encargados mediante herramientas administrativas robustas y flujos de trabajo claros.
    2.	Accesibilidad al usuario: Facilita y simplifica el proceso de adopción para los clientes, promoviendo una interacción amigable, transparente y rápida con la organización.
    
Estructura del proyecto
app/
├── config/
│   └── database.py                
│
├── controller/                    
│   ├── adoption_controller.py
│   ├── client_controller.py
│   ├── extra_service_controller.py
│   ├── pet_controller.py
│   ├── solicitud_controller.py
│   └── user_controller.py
│
├── entity/                        
│   ├── adoption.py
│   ├── client.py
│   ├── extra_service.py
│   ├── pet.py
│   ├── solicitud.py
│   └── user.py
│
├── html/                          
│   ├── css/
│   └── adopcion.css
│   └── home.css
│   └── login.css
│   └── recuperacion.css
│   └── registro.css
│   └── servicios.css             
│   ├── images/ 
│   └── imagen1.jpeg
│   └── images2.jpg
│   └── images3.jpg
│   └── images4.jpg
│   └── images5.jpeg
│   └── imagen6.jpg                
│   ├── js/   
├── admin.js                   
│   └── adopcion.js                
│   └── home.js                    
│   └── login.js                   
│   └── recuperacion.js            
│   └── registro.js                
│   └── servicios.js              
│   └── session.js                               
│   ├── admin.html                 
│   ├── adopcion.html              
│   ├── home.html                  
│   ├── login.html                 
│   ├── recuperacion.html          
│   ├── registro.html              
│   └── servicios.html             
├── repository/                  
│   ├── adoption_repository.py
│   ├── client_repository.py
│   ├── extra_service_repository.py
│   ├── pet_repository.py
│   ├── solicitud_repository.py
│   └── user_repository.py
│
├── schemas/                      
│   ├── adoption_schema.py
│   ├── client_schema.py
│   ├── extra_service_schema.py
│   ├── pet_schema.py
│   ├── solicitud_schema.py
│   └── user_schema.py
│
└── service/                       
    ├── adoption_service.py
    ├── client_service.py
    ├── extra_service_service.py
    ├── pet_service.py
    ├── solicitud_service.py
    └── user_service.py
└── main.py/                       






