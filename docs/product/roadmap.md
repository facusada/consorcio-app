# Roadmap del Producto

**Proyecto:** Sistema de Gestion de Consorcio Residencial
**Stack:** FastAPI + PostgreSQL + Docker (backend) | Nuxt 3 PWA (frontend)
**Metodologia:** SDD (Specification-Driven Development) + TDD (Test-Driven Development)
**Ultima actualizacion:** Mayo 2026

---

## Vision General

Digitalizar la administracion completa de un consorcio residencial (7 departamentos + 6 cocheras, 7 propietarios), reemplazando los procesos manuales en Excel, WhatsApp y Uala por una plataforma web + PWA centralizada.

```
Fase 1         Fase 2            Fase 3              Fase 4             Fase 5            Fase 6
MVP            Cobranzas         Reclamos             Proveedores        Comunicaciones    Evolucion
Expensas       y Deudas          y Mantenimiento      y Pagos                              
|______________|_________________|____________________|__________________|_________________|
```

---

## Fase 1 - MVP: Modulo de Expensas

### Objetivo

Automatizar la liquidacion mensual de expensas, reemplazando el calculo manual en Excel. El administrador carga gastos, el sistema calcula la expensa de cada unidad funcional por indice de prorrateo y genera el PDF listo para distribuir.

### Funcionalidades Clave

| # | Funcionalidad | Descripcion |
|---|---------------|-------------|
| 1.1 | Gestion de unidades funcionales | CRUD de las 13 unidades (7 deptos + 6 cocheras) con sus indices de prorrateo |
| 1.2 | Gestion de propietarios | CRUD de propietarios con asignacion a unidades (relacion 1:N) |
| 1.3 | Registro de gastos | Carga de gastos ordinarios y extraordinarios por periodo mensual |
| 1.4 | Liquidacion automatica | Calculo: `expensa_unidad = gasto_total * (indice / 100)` aplicado a cada unidad |
| 1.5 | Visualizacion de expensas | Listado de expensas por periodo con desglose por unidad funcional |
| 1.6 | Exportacion PDF | Generacion del PDF de liquidacion mensual con el formato actual |
| 1.7 | Autenticacion basica | Login para el rol administrador (JWT) |
| 1.8 | Infraestructura base | Docker Compose (API + DB + frontend), CI/CD basico, migraciones Alembic |

### Criterio de Completitud

- [ ] El administrador puede cargar gastos de un periodo y obtener la liquidacion calculada automaticamente
- [ ] Los indices de prorrateo producen los mismos valores que el Excel actual (validacion con datos de abril 2026: gasto total $345,000)
- [ ] Se genera un PDF descargable con el desglose de expensas por unidad
- [ ] Existe autenticacion funcional para el administrador
- [ ] Tests unitarios y de integracion cubren el flujo completo de liquidacion
- [ ] La aplicacion corre en Docker Compose (API + PostgreSQL + Nuxt 3)

### Dependencias

- Ninguna (fase inicial)

---

## Fase 2 - Cobranzas y Deudas

### Objetivo

Registrar los pagos de cada propietario y calcular automaticamente la deuda acumulada. El administrador deja de trackear deudas manualmente en Excel y cada propietario puede consultar su estado de cuenta desde el portal.

### Funcionalidades Clave

| # | Funcionalidad | Descripcion |
|---|---------------|-------------|
| 2.1 | Registro de pagos | Carga de pagos parciales o totales por unidad funcional, con fecha, monto y medio de pago |
| 2.2 | Acumulacion automatica de deuda | `total = deuda_ordinaria_anterior + expensa_ordinaria + deuda_extraordinaria_anterior + expensa_extraordinaria` |
| 2.3 | Estado de cuenta | Vista consolidada por propietario: expensas emitidas, pagos realizados, saldo pendiente |
| 2.4 | Portal de propietario | Login con rol propietario, consulta de expensas y deudas propias |
| 2.5 | Historial de pagos | Listado cronologico de pagos por unidad con filtros por periodo |

### Criterio de Completitud

- [ ] El administrador registra pagos y el saldo de deuda se actualiza automaticamente
- [ ] La deuda se acumula correctamente entre periodos (validacion con datos historicos reales)
- [ ] Cada propietario puede loguearse y ver su estado de cuenta actualizado
- [ ] El administrador ve un resumen de cobranzas: quien pago, quien debe, montos pendientes
- [ ] Tests cubren escenarios de pago parcial, pago total, acumulacion multi-periodo y saldo cero

### Dependencias

- Fase 1 completa (unidades, propietarios, expensas liquidadas)

---

## Fase 3 - Reclamos y Mantenimiento

### Objetivo

Centralizar los reclamos de propietarios e inquilinos (hoy dispersos en WhatsApp) con seguimiento de estado y asignacion a proveedores. El administrador tiene trazabilidad completa del ciclo de vida de cada reclamo.

### Funcionalidades Clave

| # | Funcionalidad | Descripcion |
|---|---------------|-------------|
| 3.1 | Creacion de reclamos | Formulario para propietarios/inquilinos con categoria, descripcion, fotos opcionales y ubicacion |
| 3.2 | Seguimiento de estado | Flujo: Abierto -> En revision -> En trabajo -> Resuelto -> Cerrado |
| 3.3 | Asignacion a proveedores | El administrador asigna el reclamo a un proveedor registrado |
| 3.4 | Rol inquilino | Login con rol inquilino (invitado por propietario), acceso limitado a reclamos |
| 3.5 | Historial de reclamos | Listado con filtros por estado, unidad, fecha y categoria |
| 3.6 | Comentarios | Hilo de comunicacion dentro de cada reclamo entre las partes |

### Criterio de Completitud

- [ ] Propietarios e inquilinos pueden crear reclamos desde la PWA
- [ ] El administrador puede cambiar estados y asignar proveedores
- [ ] El historial muestra todos los cambios de estado con timestamps
- [ ] El rol inquilino funciona con permisos acotados (solo reclamos)
- [ ] Tests cubren el ciclo completo de un reclamo y las transiciones de estado validas/invalidas

### Dependencias

- Fase 1 completa (autenticacion, unidades, propietarios)
- Fase 4 parcial (registro basico de proveedores para asignacion; puede implementarse un CRUD minimo de proveedores en esta fase)

---

## Fase 4 - Proveedores y Pagos

### Objetivo

Gestionar el directorio de proveedores del consorcio, registrar sus facturas y pagos, y categorizar los gastos para obtener reportes de egresos. El administrador pasa de trackear pagos en la cuenta personal de Uala a tener un registro centralizado.

### Funcionalidades Clave

| # | Funcionalidad | Descripcion |
|---|---------------|-------------|
| 4.1 | Registro de proveedores | CRUD de proveedores con datos de contacto, CUIT, rubro y datos bancarios |
| 4.2 | Registro de facturas | Carga de facturas con proveedor, monto, fecha, categoria y archivo adjunto |
| 4.3 | Registro de pagos a proveedores | Pagos asociados a facturas con fecha, monto, medio de pago y comprobante |
| 4.4 | Categorizacion de gastos | Categorias configurables (limpieza, mantenimiento, servicios, seguros, etc.) |
| 4.5 | Reportes de gastos | Reporte por periodo, por categoria y por proveedor con totales y porcentajes |

### Criterio de Completitud

- [ ] El administrador registra proveedores, carga facturas y registra pagos
- [ ] Los gastos cargados en Fase 1 se vinculan con proveedores y categorias
- [ ] Los reportes muestran distribucion de gastos por categoria y por proveedor
- [ ] Se pueden adjuntar comprobantes (imagenes/PDF) a facturas y pagos
- [ ] Tests cubren CRUD completo, vinculacion factura-pago y generacion de reportes

### Dependencias

- Fase 1 completa (gastos registrados, autenticacion)

---

## Fase 5 - Comunicaciones

### Objetivo

Reemplazar el grupo de WhatsApp como canal principal de comunicacion del consorcio. El administrador envia comunicados, actas y notificaciones desde la plataforma, y los propietarios los reciben en la PWA.

### Funcionalidades Clave

| # | Funcionalidad | Descripcion |
|---|---------------|-------------|
| 5.1 | Comunicados a vecinos | Creacion y envio de comunicados con titulo, cuerpo y archivos adjuntos |
| 5.2 | Notificaciones push | Notificaciones PWA para nuevas expensas, comunicados, cambios de estado de reclamos |
| 5.3 | Actas de asamblea | Carga y consulta de actas de asamblea con fecha, asistentes y resoluciones |
| 5.4 | Bandeja de entrada | Vista unificada para propietarios con comunicados, notificaciones y novedades |

### Criterio de Completitud

- [ ] El administrador crea comunicados y todos los propietarios los reciben como notificacion push
- [ ] Las notificaciones push funcionan en la PWA (service worker configurado)
- [ ] Las actas de asamblea se pueden cargar, consultar y descargar
- [ ] Los propietarios ven una bandeja con todas las comunicaciones ordenadas cronologicamente
- [ ] Tests cubren creacion de comunicados, envio de notificaciones y consulta de actas

### Dependencias

- Fase 1 completa (autenticacion, roles)
- Fase 2 completa (portal de propietario)

---

## Fase 6 - Evolucion

### Objetivo

Incorporar herramientas avanzadas de gestion, metricas y preparar la plataforma para escalar a multiples consorcios o integrar con servicios financieros externos.

### Funcionalidades Clave

| # | Funcionalidad | Descripcion |
|---|---------------|-------------|
| 6.1 | Dashboard con metricas | Panel del administrador con indicadores clave: cobranza del mes, deuda total, gastos por categoria, reclamos abiertos |
| 6.2 | Reportes avanzados | Comparativos entre periodos, proyecciones, exportacion a Excel |
| 6.3 | Multi-consorcio | Arquitectura multi-tenant para administrar mas de un consorcio desde la misma instancia |
| 6.4 | Integracion con Uala | Consulta de movimientos y conciliacion automatica de pagos via API |
| 6.5 | Integracion con servicios | Consulta de deuda de servicios (ABSA, luz, gas) si existen APIs disponibles |

### Criterio de Completitud

- [ ] El dashboard muestra al menos 5 metricas clave actualizadas en tiempo real
- [ ] Los reportes comparativos se generan y exportan correctamente
- [ ] (Si aplica) La arquitectura soporta al menos 2 consorcios aislados
- [ ] (Si aplica) La integracion con Uala permite consultar movimientos y matchear pagos
- [ ] Tests cubren la generacion de metricas, reportes y el aislamiento multi-tenant

### Dependencias

- Fases 1 a 4 completas (datos suficientes para metricas y reportes)
- Fase 5 deseable pero no bloqueante

---

## Resumen de Fases

| Fase | Nombre | Foco Principal | Prerequisitos |
|------|--------|----------------|---------------|
| 1 | MVP: Expensas | Liquidacion automatica | Ninguno |
| 2 | Cobranzas y Deudas | Pagos y estado de cuenta | Fase 1 |
| 3 | Reclamos y Mantenimiento | Gestion de reclamos | Fase 1 |
| 4 | Proveedores y Pagos | Egresos y reportes | Fase 1 |
| 5 | Comunicaciones | Notificaciones y actas | Fases 1, 2 |
| 6 | Evolucion | Metricas y escalabilidad | Fases 1-4 |

> Las fases 2, 3 y 4 pueden desarrollarse en paralelo una vez completada la Fase 1. La Fase 5 requiere el portal de propietario (Fase 2). La Fase 6 se alimenta de los datos generados en las fases anteriores.
