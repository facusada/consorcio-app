# User Personas

Definicion de roles y usuarios del sistema de gestion de consorcio.

---

## 1. Administrador

### Descripcion

Propietario del consorcio que asumio voluntariamente el rol de administrador. No es un administrador profesional ni tiene formacion especifica en administracion de consorcios. Gestiona las operaciones diarias del edificio de forma ad-honorem o con una compensacion minima.

### Perfil tipico

- Propietario que vive en el edificio
- Conocimiento basico/intermedio de tecnologia (usa WhatsApp, Excel, home banking)
- Dedica tiempo parcial a la administracion, fuera de su trabajo principal
- Maneja un consorcio chico: 7 departamentos, 6 cocheras, 7 propietarios
- Opera con herramientas genericas (Excel, WhatsApp, Uala)

### Necesidades y objetivos

- Liquidar expensas ordinarias y extraordinarias de forma rapida y sin errores
- Registrar y categorizar los gastos del consorcio mes a mes
- Controlar el estado de deuda de cada unidad funcional
- Gestionar reclamos y solicitudes de mantenimiento
- Coordinar y registrar pagos a proveedores y servicios (ABSA, electricidad, limpieza)
- Comunicar novedades, avisos y resoluciones a todos los propietarios e inquilinos
- Generar reportes y liquidaciones en formato PDF para distribuir
- Tener trazabilidad completa de movimientos financieros

### Frustraciones actuales

- **Calculo manual propenso a errores**: liquida expensas en Excel aplicando indices a mano; un error en una celda afecta a todas las unidades
- **Tiempo excesivo**: cada liquidacion mensual demanda horas de trabajo entre calculo, armado del PDF y distribucion por WhatsApp
- **Tracking de deudas fragil**: las deudas acumuladas se registran manualmente en el mismo Excel; es facil perder el hilo de quien debe que y desde cuando
- **Sin historial centralizado**: la informacion esta dispersa entre archivos de Excel, conversaciones de WhatsApp y extractos de Uala
- **Gestion de reclamos informal**: los reclamos llegan por WhatsApp mezclados con conversaciones del grupo; se pierden o se olvidan
- **Sin respaldo automatico**: si pierde el archivo Excel o el celular, pierde toda la gestion

### Funcionalidades clave

- Dashboard con resumen del mes: total de gastos, cobranzas, deudas pendientes
- Modulo de liquidacion de expensas con calculo automatico por indices
- ABM de gastos con categorizacion (servicios, mantenimiento, extraordinarios)
- Registro de pagos recibidos y conciliacion con deudas
- Gestion de reclamos con estados (abierto, en progreso, resuelto)
- ABM de proveedores y registro de pagos realizados
- Generacion de PDF de liquidacion mensual
- Envio de comunicados y notificaciones
- Reportes historicos y exportacion de datos

### Permisos y acceso

| Recurso | Permiso |
|---|---|
| Unidades funcionales | Lectura / Escritura / Creacion |
| Propietarios e inquilinos | Lectura / Escritura / Creacion / Baja |
| Gastos | Lectura / Escritura / Creacion / Eliminacion |
| Expensas (liquidacion) | Lectura / Escritura / Creacion / Cierre de periodo |
| Pagos recibidos | Lectura / Escritura / Registro |
| Deudas | Lectura / Escritura / Ajuste manual |
| Reclamos | Lectura / Escritura / Cambio de estado / Asignacion |
| Proveedores | Lectura / Escritura / Creacion / Baja |
| Pagos a proveedores | Lectura / Escritura / Registro |
| Comunicados | Lectura / Escritura / Creacion / Envio |
| Reportes | Generacion / Exportacion |
| Configuracion del sistema | Acceso total |

---

## 2. Propietario

### Descripcion

Dueno de una o mas unidades funcionales (departamento y/o cocheras). Es responsable del pago de expensas de todas sus unidades. Puede tener un inquilino en alguna de sus propiedades.

### Perfil tipico

- Persona adulta, propietario de al menos un departamento (algunos tienen tambien cocheras)
- Nivel de tecnologia variable: desde basico (solo WhatsApp) hasta intermedio (apps bancarias, navegacion web)
- Quiere cumplir con sus obligaciones pero necesita claridad sobre que debe y por que
- Ejemplo real: Elena Michailenko tiene Depto 2 + Cochera E + Cochera F (3 unidades, 3 liquidaciones)

### Necesidades y objetivos

- Ver la liquidacion de expensas del mes actual para cada una de sus unidades
- Consultar el detalle de los gastos que componen su expensa
- Conocer su estado de deuda actualizado (ordinaria y extraordinaria)
- Acceder al historial de expensas y pagos anteriores
- Registrar o reportar un reclamo de mantenimiento
- Recibir comunicados y novedades del consorcio
- Tener un comprobante digital de sus pagos
- Si tiene inquilino, poder ver el estado de la unidad alquilada

### Frustraciones actuales

- **Informacion opaca**: recibe un PDF generico por WhatsApp sin posibilidad de consultar el detalle de cada gasto
- **Sin historial accesible**: si necesita revisar una expensa de hace 3 meses tiene que buscar en el chat de WhatsApp
- **No sabe su deuda real**: el estado de deuda solo se ve en el PDF mensual; entre liquidaciones no tiene forma de consultarlo
- **Reclamos sin seguimiento**: reporta un problema por WhatsApp y no tiene forma de saber en que estado esta
- **Multiples unidades, misma confusion**: si tiene varias unidades, recibe todo mezclado en el mismo PDF grupal
- **Dependencia del administrador**: para cualquier consulta tiene que escribirle al administrador y esperar respuesta

### Funcionalidades clave

- Vista de expensas del mes por unidad funcional propia
- Detalle desglosado de gastos ordinarios y extraordinarios
- Estado de cuenta: deuda acumulada, pagos realizados, saldo
- Historial de expensas y pagos con filtros por periodo
- Formulario de reclamos con seguimiento de estado
- Seccion de comunicados y novedades
- Descarga de liquidacion en PDF
- Notificaciones de nueva liquidacion disponible

### Permisos y acceso

| Recurso | Permiso |
|---|---|
| Unidades funcionales propias | Lectura |
| Datos personales propios | Lectura / Edicion limitada (telefono, email) |
| Expensas propias | Lectura |
| Detalle de gastos del consorcio | Lectura |
| Pagos propios | Lectura |
| Estado de deuda propia | Lectura |
| Reclamos propios | Lectura / Creacion / Comentar |
| Reclamos de otros | Sin acceso |
| Comunicados | Lectura |
| Proveedores | Sin acceso |
| Configuracion del sistema | Sin acceso |

---

## 3. Inquilino

### Descripcion

Persona que alquila una unidad funcional. No tiene obligacion directa de pago de expensas (eso depende del contrato con el propietario), pero en la practica suele pagar las expensas ordinarias. Necesita acceso a informacion basica y un canal de comunicacion con la administracion.

### Perfil tipico

- Persona que alquila un departamento en el edificio
- Generalmente mas joven, con buen manejo de tecnologia
- No conoce la dinamica interna del consorcio ni a todos los vecinos
- Su relacion contractual es con el propietario, no con el consorcio
- Quiere resolver problemas de su unidad de forma rapida y directa

### Necesidades y objetivos

- Ver la expensa del mes correspondiente a la unidad que alquila
- Reportar problemas de mantenimiento en su unidad (filtraciones, roturas, etc.)
- Hacer seguimiento de sus reclamos
- Recibir comunicados relevantes del consorcio (cortes de agua, trabajos programados, etc.)
- Tener un canal directo con la administracion sin depender del propietario como intermediario

### Frustraciones actuales

- **Cadena de informacion rota**: la liquidacion llega al propietario por WhatsApp; el inquilino depende de que el propietario le reenvie la informacion
- **Sin canal directo**: si tiene un problema en la unidad, tiene que avisar al propietario para que este contacte al administrador
- **Tiempos de respuesta lentos**: la cadena inquilino -> propietario -> administrador genera demoras innecesarias
- **Desconocimiento total**: no sabe cuanto se gasta en el consorcio, que trabajos se hicieron ni que esta planificado
- **Sin comprobantes**: no tiene forma de demostrar que pago la expensa ni de verificar el monto correcto

### Funcionalidades clave

- Vista de la expensa del mes de la unidad que alquila
- Formulario de reclamos con seguimiento de estado
- Seccion de comunicados y novedades del consorcio
- Notificaciones de nueva expensa disponible y comunicados
- Datos de contacto de la administracion

### Permisos y acceso

| Recurso | Permiso |
|---|---|
| Unidad funcional alquilada | Lectura limitada (expensa del mes) |
| Datos personales propios | Lectura / Edicion limitada (telefono, email) |
| Expensa de la unidad alquilada | Lectura (solo monto, no detalle completo de gastos) |
| Estado de deuda | Sin acceso (corresponde al propietario) |
| Reclamos propios | Lectura / Creacion / Comentar |
| Reclamos de otros | Sin acceso |
| Comunicados | Lectura |
| Historial de expensas | Sin acceso |
| Proveedores | Sin acceso |
| Configuracion del sistema | Sin acceso |

---

## Matriz comparativa de acceso

| Funcionalidad | Administrador | Propietario | Inquilino |
|---|---|---|---|
| Dashboard general | Total | Solo sus unidades | Solo su unidad |
| Liquidar expensas | Si | No | No |
| Ver expensas | Todas | Solo propias | Solo de su unidad |
| Detalle de gastos | Total | Lectura | Limitado |
| Registrar gastos | Si | No | No |
| Estado de deuda | Todos | Solo propio | No |
| Registrar pagos | Si | No | No |
| Ver pagos | Todos | Solo propios | No |
| Crear reclamos | Si | Si | Si |
| Gestionar reclamos | Si (todos) | No | No |
| Comunicados | Crear / Enviar | Lectura | Lectura |
| Proveedores | CRUD completo | No | No |
| Reportes | Generar / Exportar | No | No |
| Configuracion | Total | No | No |
| Gestion de usuarios | Total | No | No |

---

## Relaciones entre roles

```
Administrador
    |
    |--- gestiona ---> Unidades Funcionales
    |--- liquida ----> Expensas
    |--- resuelve ---> Reclamos
    |
    +--- Propietario (1 por cada unidad)
             |
             |--- paga -------> Expensas de sus unidades
             |--- crea -------> Reclamos
             |--- puede tener -> Inquilino (0 o 1 por unidad)
                                    |
                                    |--- ve ------> Expensa de la unidad
                                    |--- crea ----> Reclamos de la unidad
```

### Notas sobre el modelo de datos

- Un propietario puede tener multiples unidades funcionales (ej: Elena tiene 3 unidades)
- Un inquilino esta asociado a exactamente una unidad funcional
- Una unidad funcional tiene exactamente un propietario y opcionalmente un inquilino
- El administrador es tambien propietario (tiene su propia unidad funcional)
- Los indices de participacion estan vinculados a la unidad funcional, no al propietario
