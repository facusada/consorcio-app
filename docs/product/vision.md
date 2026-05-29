# Vision del Producto

## 1. Problema

La administracion de consorcios residenciales pequenos en Argentina se gestiona, en la mayoria de los casos, de forma completamente manual. El flujo actual presenta multiples puntos de friccion:

- **Calculo manual de expensas en Excel**: cada mes el administrador arma una planilla donde multiplica el gasto total por el indice de cada unidad funcional. Cualquier error de tipeo o formula mal copiada genera diferencias que se arrastran entre periodos.
- **Distribucion por WhatsApp**: la liquidacion se exporta a PDF y se envia al grupo de vecinos. No hay registro formal de envio, no hay acuse de recibo, y el historial se pierde en el scroll del chat.
- **Sin trazabilidad de pagos**: los cobros se realizan a traves de una cuenta bancaria personal (Uala). El administrador debe cruzar manualmente las transferencias recibidas con las unidades que pagaron, sin ningun vinculo automatico.
- **Deudas trackeadas a mano**: los saldos pendientes se acumulan en la misma planilla Excel. Si el administrador olvida actualizar un pago o arrastra un monto incorrecto, la deuda de esa unidad queda desactualizada indefinidamente.
- **Cero visibilidad para propietarios e inquilinos**: los vecinos no tienen forma de consultar su estado de cuenta, historial de expensas o detalle de gastos fuera de los PDFs que recibieron (si es que los guardaron).
- **Reclamos informales**: los pedidos de mantenimiento o reclamos se hacen por mensaje de texto al administrador, sin seguimiento, sin prioridad, sin registro de resolucion.
- **Gestion de proveedores opaca**: no hay registro centralizado de proveedores, presupuestos ni historial de trabajos realizados.

El resultado es un proceso fragil, propenso a errores, que consume tiempo desproporcionado y genera desconfianza entre vecinos y administrador.

---

## 2. Solucion

Una aplicacion web progresiva (PWA) que centraliza y automatiza la gestion integral del consorcio:

- **Liquidacion automatica de expensas**: carga de gastos del periodo, aplicacion automatica de indices por unidad funcional, generacion de liquidaciones con desglose completo.
- **Gestion de cobranzas y deudas**: registro de pagos, conciliacion con unidades, calculo automatico de saldos y acumulacion de deuda entre periodos.
- **Portal de propietarios/inquilinos**: cada vecino accede a su estado de cuenta, historial de expensas, detalle de gastos y comprobantes desde su celular.
- **Sistema de reclamos y mantenimiento**: carga, seguimiento y resolucion de reclamos con estados, prioridades y notificaciones.
- **Registro de proveedores y pagos**: base centralizada de proveedores con historial de trabajos y pagos asociados.
- **PWA mobile-first**: instalable en el celular como una app nativa, sin necesidad de publicar en stores.

---

## 3. Propuesta de Valor

### Para el Administrador
- Reduccion drastica del tiempo de liquidacion mensual: de horas a minutos.
- Eliminacion de errores de calculo manual.
- Trazabilidad completa de cobros, pagos y deudas.
- Registro formal de reclamos con seguimiento de estado.
- Un solo lugar para toda la informacion del consorcio.

### Para el Propietario
- Acceso permanente a su estado de cuenta y detalle de expensas.
- Transparencia total sobre los gastos del consorcio.
- Canal formal para reclamos con visibilidad del estado de resolucion.
- Historial de pagos y comprobantes siempre disponible.
- Notificaciones de nuevas liquidaciones y vencimientos.

### Para el Inquilino
- Visibilidad de las expensas que le corresponden.
- Canal directo para reportar problemas de mantenimiento.
- Acceso al historial de pagos del periodo de alquiler.
- Independencia del propietario para consultar su situacion.

---

## 4. Publico Objetivo

**Consorcios residenciales pequenos y medianos en Argentina** que cumplen estas caracteristicas:

- Entre 5 y 30 unidades funcionales.
- Administracion ejercida por un propietario (administrador no profesional) o un administrador independiente con pocos consorcios.
- Gestion actual basada en herramientas genericas (Excel, WhatsApp, email).
- Sin presupuesto ni necesidad de un software de administracion empresarial.

**No es el publico objetivo**: administradoras profesionales con decenas de consorcios, consorcios comerciales o de gran escala, ni edificios con infraestructura de gestion existente.

---

## 5. Principios de Diseno

### Simplicidad
La interfaz debe ser comprensible para un administrador que hoy resuelve todo con Excel. Cada pantalla tiene un proposito claro. Sin menus anidados innecesarios ni configuraciones complejas.

### Mobile-first
El uso principal va a ser desde el celular. El diseno parte de pantallas moviles y escala hacia desktop, no al reves. La PWA debe sentirse nativa.

### Accesibilidad
La app va a ser usada por personas de distintas edades y niveles de familiaridad con tecnologia. Tipografia legible, contraste adecuado, navegacion intuitiva.

### Transparencia
Toda la informacion financiera del consorcio es visible para los propietarios. Los calculos son auditables: cualquier vecino puede verificar como se llego al monto de su expensa.

### Datos reales desde el dia uno
El sistema se disena y valida con los datos reales del consorcio (13 unidades, 7 propietarios, indices reales, montos reales). No se trabaja con datos ficticios.

---

## 6. Que NO Es

- **No es un ERP**: no busca cubrir contabilidad general, impuestos, RRHH ni procesos empresariales.
- **No es un software de administracion profesional masivo**: no compite con plataformas como ConsorcioAbierto, Consorcio3 o SisCons que estan pensadas para administradoras con cientos de edificios.
- **No es una red social de vecinos**: no incluye foro, chat entre vecinos ni funcionalidades comunitarias mas alla de reclamos formales.
- **No es una plataforma de cobro**: no procesa pagos directamente. Registra y concilia pagos realizados por los canales existentes (transferencia bancaria, Uala, etc.).
- **No es un sistema de gestion de edificios inteligentes**: no integra con sistemas de seguridad, camaras, porteros electricos ni IoT.

---

## 7. Metricas de Exito

### Eficiencia operativa
| Metrica | Situacion actual | Objetivo |
|---|---|---|
| Tiempo de liquidacion mensual | 2-3 horas (manual en Excel) | Menos de 15 minutos |
| Errores de calculo por periodo | Frecuentes, detectados tarde | Cero (calculo automatico) |
| Tiempo de conciliacion de pagos | 30-60 min (cruce manual) | Menos de 5 minutos |

### Transparencia y comunicacion
| Metrica | Situacion actual | Objetivo |
|---|---|---|
| Acceso de propietarios a su estado de cuenta | Solo si guardaron el PDF | Permanente, en tiempo real |
| Consultas al administrador por estado de cuenta | Multiples por mes (WhatsApp) | Autoservicio via la app |
| Reclamos sin seguimiento | Todos (mensajes sueltos) | 100% con estado y resolucion |

### Adopcion
| Metrica | Objetivo |
|---|---|
| Propietarios con cuenta activa | 100% (7/7) en el primer mes |
| Uso mensual de la app por propietarios | Al menos 1 ingreso por mes por propietario |
| Liquidaciones generadas desde la app | 100% de los periodos desde el lanzamiento |
