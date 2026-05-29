# SDD: Modulo de Expensas

## Status

Work in progress.

---

## 1. Objetivo

Digitalizar el calculo y la distribucion de expensas del consorcio, reemplazando el proceso manual en Excel por una liquidacion automatica que aplique los indices de prorrateo sobre los gastos del periodo y genere el detalle por unidad funcional listo para consultar y exportar en PDF.

---

## 2. Alcance

### Incluido en esta version

- CRUD de gastos ordinarios y extraordinarios por periodo mensual.
- Liquidacion automatica: calculo de expensa por unidad funcional aplicando indice de prorrateo.
- Acumulacion de deuda de periodos anteriores en el total de cada unidad.
- Consulta de liquidaciones por periodo y por unidad funcional.
- Exportacion de la liquidacion mensual a PDF (replicando la estructura del formato actual).
- Historial de liquidaciones anteriores.
- Validacion contra datos reales del consorcio (abril 2026).

### Excluido de esta version

- Registro de pagos y conciliacion de cobranzas (Fase 2).
- Portal de propietario con login propio (Fase 2).
- Calculo automatico de intereses por mora.
- Envio automatico de liquidaciones por email o notificacion push (Fase 5).
- Generacion de reportes comparativos entre periodos (Fase 6).
- Multi-consorcio (Fase 6).

---

## 3. Contexto

### Proceso actual

1. El administrador registra los gastos del mes en una planilla Excel.
2. Calcula manualmente la expensa de cada unidad: `gasto_total * (indice / 100)`.
3. Agrega las deudas acumuladas de periodos anteriores al total de cada unidad.
4. Exporta la planilla a PDF.
5. Envia el PDF al grupo de WhatsApp del consorcio.

### Problemas del proceso actual

- **Errores de calculo**: una formula mal copiada o un indice incorrecto afecta a todas las unidades y se arrastra entre periodos.
- **Tiempo excesivo**: cada liquidacion demanda 2-3 horas entre armado, revision y distribucion.
- **Sin historial consultable**: los PDFs quedan enterrados en el chat de WhatsApp; no hay forma rapida de consultar un periodo anterior.
- **Deuda fragil**: los saldos pendientes se actualizan a mano en el mismo Excel; cualquier olvido genera inconsistencias.
- **Cero auditabilidad**: los propietarios reciben un PDF final sin posibilidad de verificar como se llego a cada monto.

### Por que se quiere cambiar

Reducir el tiempo de liquidacion de horas a minutos, eliminar errores de calculo manual, dar a los propietarios una forma de consultar sus expensas sin depender del administrador, y establecer una base de datos confiable sobre la cual construir los modulos de cobranzas, reclamos y reportes.

---

## 4. Reglas de Negocio

### RN-1: Distribucion por indice de prorrateo

El gasto total del periodo se distribuye entre las unidades funcionales segun su indice de prorrateo. Cada unidad recibe una proporcion fija del gasto.

**Formula:**

```
expensa_unidad = gasto_total * (indice / 100)
```

### RN-2: Indices fijos que suman 100%

Los indices de prorrateo estan definidos en el reglamento de copropiedad y son inmutables salvo reforma del reglamento (requiere asamblea extraordinaria y escritura publica). La suma de todos los indices del consorcio debe ser exactamente 100%.

**Indices vigentes:**

| Unidad | Indice (%) |
|---|---|
| Depto 1 | 16.68 |
| Depto 2 | 13.13 |
| Depto 3 | 12.91 |
| Depto 4 | 13.13 |
| Depto 5 | 12.91 |
| Depto 6 | 13.13 |
| Depto 7 | 12.91 |
| Cochera A | 0.85 |
| Cochera B | 0.85 |
| Cochera C | 0.85 |
| Cochera D | 0.85 |
| Cochera E | 0.85 |
| Cochera F | 0.95 |
| **Total** | **100.00** |

### RN-3: Dos tipos de expensas

Los gastos del consorcio se clasifican en dos tipos:

- **Ordinarios**: gastos periodicos y previsibles (limpieza, servicios, mantenimiento, honorarios del administrador, seguro, ABL, etc.).
- **Extraordinarios**: gastos no habituales aprobados por asamblea (reparaciones mayores, mejoras, inversiones).

Cada tipo se liquida y acumula de forma independiente.

### RN-4: Calculo del total por unidad

El monto total que un propietario debe abonar en un periodo combina la expensa del mes con la deuda acumulada de periodos anteriores:

```
total_unidad = deuda_ordinaria + expensa_ordinaria + deuda_extraordinaria + expensa_extraordinaria
```

### RN-5: Acumulacion de deuda

Si un propietario no paga (total o parcialmente) la expensa de un periodo, el saldo impago se acumula como deuda y se suma al total del periodo siguiente. La deuda se mantiene separada por tipo (ordinaria / extraordinaria).

### RN-6: Gasto extraordinario con alcance variable

Un gasto extraordinario puede aplicar a todas las unidades (se distribuye por indice) o solo a un subconjunto de unidades (por ejemplo, una reparacion que afecta unicamente a las cocheras). En el segundo caso, el indice se recalcula proporcionalmente entre las unidades alcanzadas para que la suma parcial sea 100%.

### RN-7: Periodo mensual

Cada liquidacion corresponde a un mes calendario. Un periodo se identifica por mes y anio (ejemplo: 2026-04). No puede existir mas de una liquidacion activa por periodo.

### RN-8: Estado de la liquidacion

Una liquidacion pasa por los siguientes estados:

```
Abierto --> Liquidado --> Cerrado
```

- **Abierto**: el administrador esta cargando gastos. Se pueden agregar, editar y eliminar gastos. No se calcularon expensas aun.
- **Liquidado**: se ejecuto el calculo de expensas para todas las unidades. Los montos son visibles. Se puede revertir a abierto si hay errores.
- **Cerrado**: la liquidacion es definitiva. No se pueden modificar gastos ni montos. La deuda generada se traslada al periodo siguiente.

### RN-9: Redondeo

Los montos se redondean a dos decimales (centavos). El redondeo se aplica por unidad funcional. Las diferencias de redondeo (si la suma de las expensas redondeadas no coincide con el gasto total) se absorben en la unidad de mayor indice.

---

## 5. Entidades del Dominio

### 5.1 UnidadFuncional

Representa cada unidad del consorcio (departamento o cochera).

| Campo | Tipo | Descripcion |
|---|---|---|
| id | UUID | Identificador unico |
| codigo | string | Codigo de la unidad (ej: "DEPTO-1", "COCH-A") |
| tipo | enum | `departamento` o `cochera` |
| indice_prorrateo | decimal(5,2) | Porcentaje de participacion (ej: 16.68) |
| piso | string (nullable) | Piso de la unidad |
| numero | string (nullable) | Numero o letra de la unidad |
| activa | boolean | Si esta activa para liquidacion |

### 5.2 Propietario

Persona titular del dominio de una o mas unidades.

| Campo | Tipo | Descripcion |
|---|---|---|
| id | UUID | Identificador unico |
| nombre | string | Nombre completo |
| email | string (nullable) | Email de contacto |
| telefono | string (nullable) | Telefono de contacto |
| activo | boolean | Si esta activo en el consorcio |

### 5.3 PropietarioUnidad (relacion N:M)

Vincula propietarios con unidades funcionales. Un propietario puede tener multiples unidades y una unidad puede tener co-propietarios.

| Campo | Tipo | Descripcion |
|---|---|---|
| propietario_id | UUID (FK) | Referencia al propietario |
| unidad_id | UUID (FK) | Referencia a la unidad funcional |
| desde | date | Fecha de inicio de titularidad |
| hasta | date (nullable) | Fecha de fin de titularidad (null = vigente) |

### 5.4 Periodo

Intervalo mensual al que corresponde una liquidacion.

| Campo | Tipo | Descripcion |
|---|---|---|
| id | UUID | Identificador unico |
| anio | integer | Anio (ej: 2026) |
| mes | integer | Mes (1-12) |
| estado | enum | `abierto`, `liquidado`, `cerrado` |
| fecha_liquidacion | datetime (nullable) | Timestamp de cuando se ejecuto la liquidacion |
| fecha_cierre | datetime (nullable) | Timestamp de cuando se cerro el periodo |

**Restriccion**: combinacion (anio, mes) es unica.

### 5.5 Gasto

Cada egreso o costo que el consorcio tuvo en un periodo.

| Campo | Tipo | Descripcion |
|---|---|---|
| id | UUID | Identificador unico |
| periodo_id | UUID (FK) | Periodo al que pertenece |
| tipo | enum | `ordinario` o `extraordinario` |
| categoria | string | Categoria del gasto (limpieza, servicios, etc.) |
| descripcion | string | Descripcion del gasto |
| monto | decimal(12,2) | Monto total del gasto |
| fecha | date | Fecha del gasto |
| aplica_a_todas | boolean | Si aplica a todas las unidades |
| created_at | datetime | Fecha de creacion del registro |

### 5.6 GastoUnidad (para gastos con alcance parcial)

Cuando un gasto extraordinario aplica solo a algunas unidades.

| Campo | Tipo | Descripcion |
|---|---|---|
| gasto_id | UUID (FK) | Referencia al gasto |
| unidad_id | UUID (FK) | Referencia a la unidad funcional alcanzada |

### 5.7 Liquidacion

Resultado del calculo de expensas de un periodo.

| Campo | Tipo | Descripcion |
|---|---|---|
| id | UUID | Identificador unico |
| periodo_id | UUID (FK) | Periodo al que pertenece (1:1) |
| total_ordinario | decimal(12,2) | Suma total de gastos ordinarios del periodo |
| total_extraordinario | decimal(12,2) | Suma total de gastos extraordinarios del periodo |
| created_at | datetime | Fecha de generacion |

### 5.8 DetalleExpensa

Monto calculado para cada unidad funcional en una liquidacion.

| Campo | Tipo | Descripcion |
|---|---|---|
| id | UUID | Identificador unico |
| liquidacion_id | UUID (FK) | Referencia a la liquidacion |
| unidad_id | UUID (FK) | Referencia a la unidad funcional |
| expensa_ordinaria | decimal(12,2) | Monto calculado de expensa ordinaria |
| expensa_extraordinaria | decimal(12,2) | Monto calculado de expensa extraordinaria |
| deuda_ordinaria | decimal(12,2) | Deuda ordinaria acumulada de periodos anteriores |
| deuda_extraordinaria | decimal(12,2) | Deuda extraordinaria acumulada de periodos anteriores |
| total | decimal(12,2) | Suma de los cuatro conceptos |

**Restriccion**: combinacion (liquidacion_id, unidad_id) es unica.

---

## 6. Funcionalidades Detalladas

### 6.1 CRUD de Gastos del Periodo

**Descripcion**: El administrador carga, edita y elimina los gastos del consorcio para un periodo dado.

**Flujo**:
1. El administrador selecciona o crea un periodo (mes/anio).
2. Agrega gastos indicando tipo (ordinario/extraordinario), categoria, descripcion, monto y fecha.
3. Para gastos extraordinarios, puede indicar si aplica a todas las unidades o seleccionar un subconjunto.
4. El sistema muestra el total de gastos ordinarios y extraordinarios del periodo en tiempo real.
5. El administrador puede editar o eliminar gastos mientras el periodo este en estado `abierto`.

**Restricciones**:
- Solo se pueden agregar/editar/eliminar gastos en periodos con estado `abierto`.
- El monto del gasto debe ser mayor a cero.
- La categoria es obligatoria.

### 6.2 Liquidacion Automatica

**Descripcion**: El sistema calcula la expensa de cada unidad funcional aplicando el indice de prorrateo sobre el total de gastos del periodo.

**Flujo**:
1. El administrador revisa los gastos cargados y confirma la liquidacion.
2. El sistema calcula para cada unidad activa:
   - `expensa_ordinaria = total_gastos_ordinarios * (indice / 100)`
   - `expensa_extraordinaria = total_gastos_extraordinarios * (indice / 100)` (si aplica a todas) o con indice proporcional (si aplica a un subconjunto).
3. El sistema recupera la deuda acumulada de cada unidad del periodo anterior (si existe y esta cerrado).
4. Genera un `DetalleExpensa` por cada unidad con los cuatro componentes y el total.
5. El periodo pasa a estado `liquidado`.

**Restricciones**:
- Solo se puede liquidar un periodo en estado `abierto`.
- Debe haber al menos un gasto cargado.
- Todas las unidades activas deben tener un propietario asignado vigente.
- Si ya existe una liquidacion para el periodo (por re-liquidacion), se reemplaza la anterior.

### 6.3 Consulta por Periodo y por Unidad

**Descripcion**: Consulta del detalle de expensas filtrable por periodo y por unidad funcional.

**Vistas**:
- **Por periodo**: listado de todas las unidades con su detalle (expensa ordinaria, extraordinaria, deuda ordinaria, deuda extraordinaria, total). Incluye totales generales.
- **Por unidad**: historial de expensas de una unidad funcional a lo largo de los periodos.
- **Por propietario**: agrupacion de las expensas de todas las unidades de un propietario en un periodo dado.

### 6.4 Exportacion a PDF

**Descripcion**: Generacion de un documento PDF con la liquidacion mensual, replicando la informacion y estructura del formato actual que se envia por WhatsApp.

**Contenido del PDF**:
- Encabezado: nombre del consorcio, direccion, periodo (mes/anio).
- Tabla de gastos: listado de todos los gastos del periodo con categoria, descripcion y monto.
- Totales de gastos: subtotal ordinario, subtotal extraordinario.
- Tabla de expensas por unidad: codigo de unidad, indice, expensa ordinaria, expensa extraordinaria, deuda ordinaria, deuda extraordinaria, total.
- Totales generales.
- Fecha de generacion.

### 6.5 Historial de Liquidaciones

**Descripcion**: Listado cronologico de todas las liquidaciones generadas, con acceso al detalle de cada una.

**Funcionalidad**:
- Listado de periodos con estado, fecha de liquidacion y totales.
- Acceso al detalle completo de cualquier liquidacion pasada.
- Filtros por anio y por estado.
- Indicador visual del estado de cada periodo (abierto / liquidado / cerrado).

### 6.6 Cierre de Periodo

**Descripcion**: El administrador cierra un periodo liquidado, lo que congela los montos y traslada la deuda generada al periodo siguiente.

**Flujo**:
1. El administrador revisa la liquidacion y confirma el cierre.
2. El sistema marca el periodo como `cerrado`.
3. Los gastos y detalles de expensa quedan inmutables.
4. La deuda no pagada queda disponible como insumo para la liquidacion del periodo siguiente.

**Restricciones**:
- Solo se puede cerrar un periodo en estado `liquidado`.
- Una vez cerrado, no se puede reabrir (salvo mecanismo de ajuste, ver edge cases).

---

## 7. Criterios de Aceptacion

### AC-1: Calculo correcto con datos reales

**Dado** el gasto total ordinario de $345,000 y los indices del consorcio, **cuando** se ejecuta la liquidacion, **entonces** los montos generados para cada unidad coinciden con los valores del Excel de abril 2026:

| Unidad | Indice (%) | Expensa esperada ($) |
|---|---|---|
| Depto 1 | 16.68 | 57,546.00 |
| Depto 2 | 13.13 | 45,298.50 |
| Depto 3 | 12.91 | 44,539.50 |
| Depto 4 | 13.13 | 45,298.50 |
| Depto 5 | 12.91 | 44,539.50 |
| Depto 6 | 13.13 | 45,298.50 |
| Depto 7 | 12.91 | 44,539.50 |
| Cochera A | 0.85 | 2,932.50 |
| Cochera B | 0.85 | 2,932.50 |
| Cochera C | 0.85 | 2,932.50 |
| Cochera D | 0.85 | 2,932.50 |
| Cochera E | 0.85 | 2,932.50 |
| Cochera F | 0.95 | 3,277.50 |
| **Total** | **100.00** | **345,000.00** |

### AC-2: Deuda acumulada correcta

**Dado** que Depto 6 tiene una deuda ordinaria acumulada de $108,895, **cuando** se genera la liquidacion de abril 2026, **entonces** el total de Depto 6 es $108,895 + $45,298.50 = $154,193.50 (mas cualquier componente extraordinario si aplica).

### AC-3: PDF con informacion completa

**Dado** una liquidacion en estado `liquidado` o `cerrado`, **cuando** el administrador exporta a PDF, **entonces** el documento contiene: encabezado del consorcio, listado de gastos con categorias, tabla de expensas por unidad con los cuatro componentes (expensa ord., exp. ext., deuda ord., deuda ext.) y totales.

### AC-4: Indices suman 100%

**Dado** el conjunto de unidades funcionales activas del consorcio, **cuando** se consultan los indices de prorrateo, **entonces** la suma de todos los indices es exactamente 100.00%.

### AC-5: Integridad de la liquidacion

**Dado** un periodo en estado `abierto` con gastos cargados, **cuando** se ejecuta la liquidacion, **entonces** se genera exactamente un `DetalleExpensa` por cada unidad funcional activa, y la suma de todas las expensas ordinarias es igual al total de gastos ordinarios del periodo (tolerancia de +/- $0.01 por redondeo).

### AC-6: Inmutabilidad del periodo cerrado

**Dado** un periodo en estado `cerrado`, **cuando** se intenta agregar, editar o eliminar un gasto, **entonces** el sistema rechaza la operacion con un mensaje de error descriptivo.

### AC-7: Liquidacion de gastos extraordinarios parciales

**Dado** un gasto extraordinario de $50,000 que aplica solo a las 6 cocheras, **cuando** se liquida el periodo, **entonces** el monto se distribuye proporcionalmente entre las cocheras segun sus indices relativos (re-normalizados a 100%), y los departamentos reciben $0 de expensa extraordinaria por ese gasto.

### AC-8: Re-liquidacion en abierto

**Dado** un periodo en estado `liquidado`, **cuando** el administrador decide revertir a `abierto` para corregir un gasto, **entonces** los detalles de expensa anteriores se eliminan y el administrador puede modificar gastos y re-liquidar.

### AC-9: Periodo sin gastos

**Dado** un periodo en estado `abierto` sin gastos cargados, **cuando** se intenta ejecutar la liquidacion, **entonces** el sistema rechaza la operacion indicando que no hay gastos registrados.

### AC-10: Propietario con multiples unidades

**Dado** que Elena Michailenko es propietaria de Depto 2, Cochera E y Cochera F, **cuando** se consulta la liquidacion por propietario, **entonces** se muestran las tres unidades agrupadas con sus respectivos montos y un subtotal consolidado.

---

## 8. Edge Cases

### EC-1: Cambio de propietario mid-periodo

**Situacion**: Un departamento se vende y cambia de propietario durante el mes.

**Resolucion**: La expensa del periodo se asigna al propietario vigente al momento de la liquidacion. El sistema registra la fecha de inicio/fin de titularidad en `PropietarioUnidad`, pero no prorratea la expensa dentro del mes. Si hay una transferencia de deuda pendiente entre propietarios, el administrador la ajusta manualmente.

### EC-2: Unidad sin propietario activo

**Situacion**: Una unidad funcional no tiene propietario asignado (o el propietario fue dado de baja) al momento de liquidar.

**Resolucion**: El sistema impide la liquidacion y muestra un error indicando las unidades sin propietario vigente. El administrador debe regularizar la situacion antes de liquidar.

### EC-3: Ajuste retroactivo sobre periodo cerrado

**Situacion**: Se detecta un error en un gasto despues de cerrar el periodo (por ejemplo, una factura mal cargada).

**Resolucion**: El periodo cerrado no se reabre. El administrador carga un gasto de ajuste (positivo o negativo) en el periodo corriente con la descripcion "Ajuste periodo [mes/anio] - [motivo]". El ajuste se incluye en la liquidacion actual.

### EC-4: Gasto extraordinario parcial

**Situacion**: Un gasto extraordinario aplica solo a un subconjunto de unidades (ej: reparacion del porton de cocheras).

**Resolucion**: El sistema permite asociar el gasto a las unidades afectadas via `GastoUnidad`. Al liquidar, recalcula los indices proporcionalmente entre las unidades seleccionadas para que sumen 100% entre ellas. Ejemplo: si las 6 cocheras tienen indices 0.85, 0.85, 0.85, 0.85, 0.85, 0.95 (total 5.20%), los indices relativos son 16.35%, 16.35%, 16.35%, 16.35%, 16.35%, 18.27%.

### EC-5: Pago parcial

**Situacion**: Un propietario paga menos del total de su expensa.

**Resolucion**: El registro de pagos es parte de la Fase 2 (Cobranzas y Deudas). En esta fase, la deuda se gestiona como un monto total que el administrador puede ajustar manualmente al cargar los datos del periodo anterior. En Fase 2 se automatiza la conciliacion.

### EC-6: Redondeo de centavos

**Situacion**: Al aplicar un indice como 12.91% sobre $345,000, el resultado es $44,539.50 (exacto en este caso). Pero con otros montos puede haber diferencias de centavos donde la suma de las partes no coincide con el total.

**Resolucion**: Se redondea cada expensa a dos decimales. Si la suma de las expensas redondeadas difiere del gasto total, la diferencia (siempre menor a $0.13 con 13 unidades) se ajusta en la unidad de mayor indice (Depto 1, 16.68%).

### EC-7: Periodo duplicado

**Situacion**: Se intenta crear un periodo para un mes/anio que ya existe.

**Resolucion**: El sistema rechaza la creacion con un error indicando que ya existe un periodo para ese mes/anio. La restriccion se aplica a nivel de base de datos (unique constraint en anio+mes).

### EC-8: Gasto con monto cero o negativo

**Situacion**: Se intenta cargar un gasto con monto $0 o negativo.

**Resolucion**: Monto $0 se rechaza. Montos negativos se permiten exclusivamente para gastos de tipo "ajuste" que corrigen errores de periodos anteriores (ver EC-3).

### EC-9: Cambio de indice de prorrateo

**Situacion**: Se modifica el reglamento de copropiedad y cambian los indices.

**Resolucion**: Los indices se almacenan en la tabla `UnidadFuncional` y pueden ser actualizados por el administrador. Las liquidaciones ya cerrados conservan los montos calculados con los indices vigentes al momento de la liquidacion. El `DetalleExpensa` almacena los valores absolutos, no los indices, por lo que los cambios futuros no afectan periodos pasados.

---

## 9. Impacto Tecnico

### 9.1 Base de Datos (PostgreSQL)

**Tablas nuevas:**

- `unidades_funcionales` - Las 13 unidades del consorcio con sus indices
- `propietarios` - Los 7 propietarios del consorcio
- `propietarios_unidades` - Relacion N:M con fechas de vigencia
- `periodos` - Periodos mensuales con estado
- `gastos` - Gastos cargados por periodo
- `gastos_unidades` - Relacion de gastos parciales con unidades
- `liquidaciones` - Cabecera de cada liquidacion
- `detalles_expensa` - Detalle calculado por unidad por liquidacion

**Migraciones**: Alembic para versionado del schema.

**Seed data**: Script de carga inicial con las 13 unidades, 7 propietarios y sus asignaciones.

### 9.2 API (FastAPI)

**Endpoints:**

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | `/api/v1/unidades` | Listar unidades funcionales |
| GET | `/api/v1/unidades/{id}` | Detalle de una unidad |
| GET | `/api/v1/propietarios` | Listar propietarios |
| GET | `/api/v1/propietarios/{id}` | Detalle de un propietario con sus unidades |
| GET | `/api/v1/periodos` | Listar periodos con filtros (anio, estado) |
| POST | `/api/v1/periodos` | Crear un nuevo periodo |
| GET | `/api/v1/periodos/{id}` | Detalle de un periodo |
| PATCH | `/api/v1/periodos/{id}/estado` | Cambiar estado del periodo |
| GET | `/api/v1/periodos/{id}/gastos` | Listar gastos de un periodo |
| POST | `/api/v1/periodos/{id}/gastos` | Agregar gasto a un periodo |
| PUT | `/api/v1/periodos/{id}/gastos/{gasto_id}` | Editar un gasto |
| DELETE | `/api/v1/periodos/{id}/gastos/{gasto_id}` | Eliminar un gasto |
| POST | `/api/v1/periodos/{id}/liquidar` | Ejecutar liquidacion del periodo |
| GET | `/api/v1/periodos/{id}/liquidacion` | Consultar liquidacion del periodo |
| GET | `/api/v1/periodos/{id}/liquidacion/pdf` | Descargar PDF de la liquidacion |
| GET | `/api/v1/unidades/{id}/expensas` | Historial de expensas de una unidad |
| GET | `/api/v1/propietarios/{id}/expensas` | Expensas agrupadas por propietario |

**Autenticacion**: JWT con rol `administrador` (unico rol en esta fase).

### 9.3 Frontend (Nuxt 3 PWA)

**Paginas:**

| Ruta | Descripcion |
|---|---|
| `/admin/periodos` | Listado de periodos con estado |
| `/admin/periodos/:id` | Detalle del periodo: gastos y liquidacion |
| `/admin/periodos/:id/gastos/nuevo` | Formulario de carga de gasto |
| `/admin/periodos/:id/liquidacion` | Vista de la liquidacion con tabla de expensas |
| `/admin/unidades` | Listado de unidades funcionales |
| `/admin/propietarios` | Listado de propietarios con sus unidades |

**Componentes clave:**

- `GastoForm.vue` - Formulario de carga/edicion de gastos.
- `TablaExpensas.vue` - Tabla con el detalle de expensas por unidad.
- `ResumenLiquidacion.vue` - Totales y estado del periodo.
- `PeriodoEstadoBadge.vue` - Indicador visual del estado del periodo.

### 9.4 Generacion de PDF

Libreria server-side (WeasyPrint o similar) para generar el PDF desde un template HTML/CSS. El template replica la estructura actual del Excel exportado a PDF.

---

## 10. Dependencias

### Prerequisitos (deben existir antes de iniciar)

| Dependencia | Estado | Descripcion |
|---|---|---|
| Modelo de datos base | Pendiente | Tablas de unidades funcionales y propietarios |
| Autenticacion JWT | Pendiente | Login y middleware de autenticacion para el administrador |
| Infraestructura Docker | Pendiente | Docker Compose con FastAPI + PostgreSQL + Nuxt 3 |
| Migraciones Alembic | Pendiente | Setup de Alembic para versionado del schema |
| CI/CD basico | Pendiente | Pipeline para tests y build |

### Dependencias externas

- Ninguna integracion con servicios externos en esta fase.
- La generacion de PDF es server-side, sin dependencia de servicios de terceros.

### Bloqueante para

- **Fase 2 (Cobranzas y Deudas)**: requiere unidades, propietarios, periodos y liquidaciones.
- **Fase 3 (Reclamos)**: requiere unidades, propietarios y autenticacion.
- **Fase 4 (Proveedores)**: requiere gastos y periodos para vincular facturas.

---

## 11. Datos de Validacion

Datos reales del consorcio para abril 2026. Estos valores se usan en los tests de integracion para validar que el sistema produce resultados identicos al proceso manual actual.

### Gastos del periodo

- Gasto total ordinario: **$345,000**
- Gasto total extraordinario: **$0** (no hubo extraordinarios en abril 2026)

### Deudas acumuladas conocidas

| Unidad | Deuda Ordinaria ($) | Deuda Extraordinaria ($) |
|---|---|---|
| Depto 6 | 108,895.00 | 0.00 |
| (demas unidades) | 0.00 | 0.00 |

### Resultado esperado de la liquidacion (abril 2026)

| Unidad | Propietario | Exp. Ord. ($) | Deuda Ord. ($) | Total ($) |
|---|---|---|---|---|
| Depto 1 | Pitscheider Pamela | 57,546.00 | 0.00 | 57,546.00 |
| Depto 2 | Michailenko Elena | 45,298.50 | 0.00 | 45,298.50 |
| Depto 3 | Iafolla Eliana | 44,539.50 | 0.00 | 44,539.50 |
| Depto 4 | Ghida Claudio | 45,298.50 | 0.00 | 45,298.50 |
| Depto 5 | Duarte Maria | 44,539.50 | 0.00 | 44,539.50 |
| Depto 6 | Farina Graciela | 45,298.50 | 108,895.00 | 154,193.50 |
| Depto 7 | Villordo Lautaro | 44,539.50 | 0.00 | 44,539.50 |
| Coch. A | Villordo Lautaro | 2,932.50 | 0.00 | 2,932.50 |
| Coch. B | Farina Graciela | 2,932.50 | 0.00 | 2,932.50 |
| Coch. C | Iafolla Eliana | 2,932.50 | 0.00 | 2,932.50 |
| Coch. D | Duarte Maria | 2,932.50 | 0.00 | 2,932.50 |
| Coch. E | Michailenko Elena | 2,932.50 | 0.00 | 2,932.50 |
| Coch. F | Michailenko Elena | 3,277.50 | 0.00 | 3,277.50 |

### Subtotales por propietario (abril 2026)

| Propietario | Unidades | Total ($) |
|---|---|---|
| Pitscheider Pamela | Depto 1 | 57,546.00 |
| Michailenko Elena | Depto 2 + Coch. E + Coch. F | 51,508.50 |
| Iafolla Eliana | Depto 3 + Coch. C | 47,472.00 |
| Ghida Claudio | Depto 4 | 45,298.50 |
| Duarte Maria | Depto 5 + Coch. D | 47,472.00 |
| Farina Graciela | Depto 6 + Coch. B | 157,126.00 |
| Villordo Lautaro | Depto 7 + Coch. A | 47,472.00 |
