# Arquitectura de Agentes de IA

> Definicion de roles, responsabilidades e interacciones de los agentes que participan en el desarrollo del sistema de gestion de consorcio.

---

## Indice

1. [Vision general](#vision-general)
2. [Diagrama de interaccion](#diagrama-de-interaccion)
3. [Catalogo de agentes](#catalogo-de-agentes)
4. [Reglas de comunicacion](#reglas-de-comunicacion)
5. [Agregar nuevos agentes](#agregar-nuevos-agentes)
6. [Estado actual del sistema](#estado-actual-del-sistema)

---

## Vision general

El sistema de agentes sigue un patron hub-and-spoke: el **Orchestrator** coordina a todos los agentes especializados. Ningun agente se comunica directamente con otro sin pasar por el Orchestrator, salvo las excepciones documentadas en las reglas de comunicacion.

Cada agente tiene un alcance acotado y produce artefactos concretos que otros agentes consumen. La trazabilidad se mantiene a traves de la estructura de documentacion SDD del proyecto.

---

## Diagrama de interaccion

```
                              ACTIVOS
                    +--------------------------+
                    |                          |
                    |   +------------------+   |
                    |   | Product Manager  |   |
                    |   | Agent            |   |
                    |   +--------+---------+   |
                    |            |              |
                    |            v              |
                    |   +--------+---------+   |
                    |   | Business Analyst |   |
                    |   | Agent            |   |
                    |   +--------+---------+   |
                    |            |              |
                    +------------|-------------+
                                 |
                                 v
+------------------------------------------------------------------------+
|                                                                        |
|                    +------------------------+                          |
|                    |    ORCHESTRATOR        |                          |
|                    |    (Claude Code)       |                          |
|                    +---+----+----+----+---+-+                          |
|                        |    |    |    |   |                            |
|          +-------------+    |    |    |   +-------------+              |
|          |                  |    |    |                  |              |
|          v                  v    |    v                  v              |
|   +------+------+  +-------+-+  |  +-+--------+  +-----+-------+      |
|   | UX/UI       |  |Backend |  |  |Frontend  |  | DevOps      |      |
|   | Agent       |  |Agent   |  |  |Agent     |  | Agent       |      |
|   +-------------+  +--------+  |  +----------+  +-------------+      |
|   PROXIMA FASE     FUTURO      |   FUTURO        FUTURO               |
|                                v                                      |
|                         +------+------+                               |
|                         | QA Agent    |                               |
|                         +-------------+                               |
|                           FUTURO                                      |
|                                                                       |
|                     +------------------+                               |
|                     | Documentation   | <--- TRANSVERSAL              |
|                     | Agent           |      (interactua con todos)    |
|                     +------------------+                               |
|                                                                        |
+------------------------------------------------------------------------+
```

**Flujo principal de una feature:**

```
Product Manager --> Business Analyst --> Orchestrator --> UX/UI
                                                     --> Backend
                                                     --> Frontend
                                                     --> QA
                                                     --> Documentation
```

---

## Catalogo de agentes

### 1. Orchestrator (Claude Code)

| Atributo | Detalle |
|---|---|
| **Estado** | ACTIVO |
| **Rol** | Coordinador central del sistema de agentes |
| **Responsabilidades** | Recibir instrucciones del usuario y descomponerlas en tareas. Decidir que agente debe actuar en cada momento. Mantener el contexto global del proyecto. Validar que los artefactos producidos sean coherentes entre si. Resolver conflictos entre decisiones de distintos agentes. Ejecutar planes de trabajo multi-paso. |
| **Herramientas** | Claude Code CLI, acceso al filesystem, git, terminal, todos los MCP tools disponibles |
| **Se activa cuando** | El usuario inicia cualquier interaccion con el sistema |
| **Interactua con** | Todos los agentes. Es el unico punto de entrada y salida. |

**Artefactos que produce:**
- Planes de trabajo
- Decisiones de arquitectura de agentes
- Coordinacion de merges entre artefactos de distintos agentes

**Reglas especificas:**
- Nunca ejecuta trabajo especializado directamente; lo delega al agente correspondiente
- Mantiene un log implicito de decisiones en la conversacion
- Ante ambiguedad, consulta al usuario antes de delegar

---

### 2. Product Manager Agent

| Atributo | Detalle |
|---|---|
| **Estado** | ACTIVO |
| **Rol** | Definicion de producto y priorizacion estrategica |
| **Responsabilidades** | Definir y mantener el roadmap del producto. Priorizar features usando MoSCoW o similar. Escribir historias de usuario con criterios de aceptacion. Validar que las features resuelvan problemas reales del consorcio. Decidir alcance de cada iteracion. Gestionar el backlog. |
| **Herramientas** | Documentacion Markdown, estructura SDD, GitHub Issues |
| **Se activa cuando** | Se necesita definir una nueva feature, repriorizar el backlog, o validar si algo esta dentro del alcance |
| **Interactua con** | Orchestrator (recibe instrucciones, entrega specs). Business Analyst (le pasa features para analisis detallado). |

**Artefactos que produce:**
- `docs/product/roadmap.md`
- `docs/product/backlog.md`
- Historias de usuario en formato estandar
- Criterios de aceptacion por feature

**Reglas especificas:**
- Toda feature debe tener al menos un criterio de aceptacion medible
- No define solucion tecnica; solo el "que" y el "por que"
- Prioriza en base a impacto para el administrador del consorcio

---

### 3. Business Analyst Agent

| Atributo | Detalle |
|---|---|
| **Estado** | ACTIVO |
| **Rol** | Analisis de requerimientos y reglas de negocio |
| **Responsabilidades** | Relevar y documentar procesos actuales (Excel, WhatsApp, Uala). Definir procesos deseados en el sistema. Documentar reglas de negocio con precision (formulas de expensas, indices, deudas). Identificar edge cases y restricciones del dominio. Producir specs SDD completas. Validar datos reales del consorcio contra el modelo propuesto. |
| **Herramientas** | Documentacion Markdown, estructura SDD (`docs/sdd/wip/`), diagramas de proceso |
| **Se activa cuando** | Se necesita analizar un proceso del consorcio, documentar reglas de negocio, o crear una spec SDD |
| **Interactua con** | Orchestrator (recibe features del PM, entrega specs). Product Manager (recibe historias de usuario, devuelve analisis de viabilidad). |

**Artefactos que produce:**
- `docs/sdd/wip/<feature>/spec.md` (especificaciones SDD)
- Reglas de negocio documentadas
- Mapeos proceso actual vs proceso deseado
- Modelos de datos conceptuales

**Reglas especificas:**
- Toda spec debe incluir: objetivo, alcance, criterios de aceptacion, edge cases, impacto tecnico
- Las reglas de negocio se validan contra datos reales (ej: indices de expensas suman 100%)
- Documenta supuestos explicitos cuando la informacion es incompleta

---

### 4. UX/UI Agent

| Atributo | Detalle |
|---|---|
| **Estado** | PROXIMA FASE |
| **Rol** | Diseno de experiencia e interfaz de usuario |
| **Responsabilidades** | Disenar flujos de usuario por rol (administrador, propietario, inquilino). Crear wireframes y mockups. Definir el sistema de diseno (componentes, tipografia, colores). Disenar para mobile-first (PWA). Asegurar accesibilidad basica. Adaptar UX a usuarios no tecnicos (vecinos del consorcio). |
| **Herramientas** | Documentacion Markdown, diagramas ASCII, descripcion de componentes, referencias visuales |
| **Se activa cuando** | Una feature tiene spec SDD aprobada y necesita definicion visual/interactiva |
| **Interactua con** | Orchestrator (recibe specs, entrega disenos). Frontend Agent (le entrega specs de componentes para implementar). |

**Artefactos que produce:**
- Wireframes (descripcion estructurada o ASCII)
- Flujos de usuario por pantalla
- Sistema de diseno (tokens, componentes)
- Specs de interaccion y estados de UI

**Reglas especificas:**
- Mobile-first obligatorio (la mayoria de los vecinos usan celular)
- Maximo 3 clicks para cualquier accion frecuente
- Interfaz en espanol argentino

---

### 5. Backend Agent

| Atributo | Detalle |
|---|---|
| **Estado** | FUTURO |
| **Rol** | Desarrollo de APIs y logica de negocio server-side |
| **Responsabilidades** | Implementar APIs REST con FastAPI. Disenar y mantener modelos PostgreSQL. Implementar logica de negocio (calculo de expensas, deudas, etc.). Crear y ejecutar migraciones de base de datos. Implementar autenticacion y autorizacion por roles. Escribir tests unitarios y de integracion (TDD). |
| **Herramientas** | Python, FastAPI, SQLAlchemy/Alembic, PostgreSQL, pytest, Docker |
| **Se activa cuando** | Una feature tiene spec SDD completa y diseno UX aprobado (si aplica) |
| **Interactua con** | Orchestrator (recibe specs, entrega codigo). QA Agent (recibe reportes de bugs, entrega fixes). DevOps Agent (coordina migraciones y deploy). |

**Artefactos que produce:**
- Endpoints FastAPI
- Modelos SQLAlchemy
- Migraciones Alembic
- Tests pytest
- Schemas Pydantic

**Reglas especificas:**
- TDD obligatorio: test primero, implementacion despues
- Toda ruta protegida por rol
- Validacion de datos con Pydantic
- Migraciones reversibles siempre que sea posible

---

### 6. Frontend Agent

| Atributo | Detalle |
|---|---|
| **Estado** | FUTURO |
| **Rol** | Desarrollo de interfaces de usuario PWA |
| **Responsabilidades** | Implementar pantallas en Nuxt 3. Desarrollar componentes reutilizables (Vue 3). Gestionar estado de la aplicacion. Implementar PWA (offline, push notifications). Consumir APIs del backend. Asegurar responsive design. |
| **Herramientas** | TypeScript, Nuxt 3, Vue 3, Pinia, Tailwind CSS, service workers |
| **Se activa cuando** | El backend tiene APIs funcionales y hay diseno UX aprobado para la feature |
| **Interactua con** | Orchestrator (recibe specs de UI, entrega componentes). UX/UI Agent (recibe disenos, consulta dudas de interaccion). Backend Agent (consume APIs, reporta inconsistencias de contrato). |

**Artefactos que produce:**
- Paginas Nuxt (`pages/`)
- Componentes Vue (`components/`)
- Composables (`composables/`)
- Store Pinia (`stores/`)
- Tests de componentes

**Reglas especificas:**
- Componentes tipados con TypeScript
- Mobile-first en todos los componentes
- PWA funcional offline para consulta de expensas

---

### 7. DevOps Agent

| Atributo | Detalle |
|---|---|
| **Estado** | FUTURO |
| **Rol** | Infraestructura, CI/CD y operaciones |
| **Responsabilidades** | Configurar y mantener Docker (dev y prod). Implementar pipeline CI/CD en GitHub Actions. Gestionar deploy (staging y produccion). Configurar backups de PostgreSQL. Monitoreo basico de la aplicacion. Gestionar secrets y variables de entorno. |
| **Herramientas** | Docker, Docker Compose, GitHub Actions, scripts bash |
| **Se activa cuando** | Se necesita configurar infraestructura, pipeline, o preparar un deploy |
| **Interactua con** | Orchestrator (recibe requerimientos de infra, entrega configuraciones). Backend Agent (coordina migraciones en deploy). QA Agent (provee entorno de staging para tests). |

**Artefactos que produce:**
- `Dockerfile`, `docker-compose.yml`
- `.github/workflows/`
- Scripts de deploy y backup
- Documentacion de infraestructura

**Reglas especificas:**
- Entorno de desarrollo reproducible con un solo comando (`docker compose up`)
- Secrets nunca en el repositorio
- Pipeline bloquea merge si fallan tests

---

### 8. QA Agent

| Atributo | Detalle |
|---|---|
| **Estado** | FUTURO |
| **Rol** | Aseguramiento de calidad y testing |
| **Responsabilidades** | Validar criterios de aceptacion de cada feature. Disenar y ejecutar casos de test. Tests de integracion entre frontend y backend. Tests end-to-end de flujos criticos. Validar calculos de negocio contra datos reales. Reportar bugs con pasos de reproduccion. |
| **Herramientas** | pytest, Vitest, Playwright/Cypress, datos de prueba del consorcio |
| **Se activa cuando** | Una feature esta implementada (backend y/o frontend) y necesita validacion |
| **Interactua con** | Orchestrator (recibe features para validar, reporta resultados). Backend Agent (reporta bugs de API). Frontend Agent (reporta bugs de UI). Business Analyst Agent (consulta reglas de negocio para validar). |

**Artefactos que produce:**
- Planes de testing
- Casos de test automatizados
- Reportes de bugs
- Validaciones de datos (ej: expensas calculadas vs esperadas)

**Reglas especificas:**
- Todo bug incluye: pasos de reproduccion, resultado esperado, resultado actual
- Tests de calculo de expensas con datos reales del consorcio (abril 2026)
- Cobertura minima definida por el Orchestrator segun la criticidad del modulo

---

### 9. Documentation Agent

| Atributo | Detalle |
|---|---|
| **Estado** | TRANSVERSAL (activo desde el inicio) |
| **Rol** | Mantenimiento de documentacion tecnica y funcional |
| **Responsabilidades** | Mantener actualizados todos los documentos del proyecto. Asegurar consistencia entre specs, codigo y docs. Documentar decisiones de arquitectura (ADRs). Mantener el README y guias de contribucion. Generar documentacion de API. Actualizar AGENTS.md cuando cambie la arquitectura de agentes. |
| **Herramientas** | Markdown, estructura de `docs/`, git log para trazabilidad |
| **Se activa cuando** | Cualquier agente produce un artefacto que requiere documentacion, o cuando se detecta documentacion desactualizada |
| **Interactua con** | Orchestrator (recibe instrucciones de documentacion). Todos los agentes (consume sus artefactos para documentar). |

**Artefactos que produce:**
- `docs/architecture/` (ADRs, diagramas)
- `docs/api/` (documentacion de endpoints)
- README.md y guias
- Changelog

**Reglas especificas:**
- Toda decision de arquitectura tiene un ADR
- Documentacion siempre en espanol
- Cada artefacto referencia la spec SDD de origen

---

## Reglas de comunicacion

### Principios generales

1. **Hub-and-spoke**: toda comunicacion pasa por el Orchestrator. Un agente nunca invoca a otro directamente.
2. **Artefactos como contrato**: los agentes se comunican a traves de artefactos versionados en el repositorio (specs, codigo, tests, docs). No hay comunicacion implicita.
3. **Contexto explicito**: cuando el Orchestrator delega a un agente, le pasa el contexto minimo necesario (spec relevante, archivos involucrados, restricciones).
4. **Escalacion al usuario**: si un agente no puede resolver una ambiguedad, el Orchestrator escala al usuario. Nunca se asume.

### Protocolo de delegacion

```
1. Orchestrator recibe instruccion del usuario
2. Orchestrator identifica agente(s) necesario(s)
3. Orchestrator prepara contexto:
   - Artefactos de entrada (specs, codigo existente)
   - Restricciones y criterios de aceptacion
   - Dependencias con otros agentes
4. Orchestrator activa al agente con instruccion clara
5. Agente produce artefacto y lo entrega al Orchestrator
6. Orchestrator valida coherencia con el resto del sistema
7. Si hay conflicto, Orchestrator resuelve o escala al usuario
```

### Formato de instruccion entre agentes

```
AGENTE DESTINO: <nombre>
TAREA: <descripcion concisa>
CONTEXTO: <archivos y specs relevantes>
RESTRICCIONES: <limites y reglas que aplican>
ENTREGABLE: <que artefacto se espera>
DEPENDENCIAS: <que necesita estar listo antes>
```

### Resolucion de conflictos

| Situacion | Resolucion |
|---|---|
| Conflicto entre spec y diseno | Prevalece la spec (Business Analyst revalida) |
| Conflicto entre diseno y restriccion tecnica | Orchestrator media; si no se resuelve, escala al usuario |
| Datos ambiguos del dominio | Business Analyst consulta al usuario con opciones concretas |
| Feature fuera de alcance del MVP | Product Manager decide si se pospone o se incluye |

---

## Agregar nuevos agentes

### Proceso

1. **Identificar necesidad**: el Orchestrator o el usuario detecta que un area no esta cubierta o que un agente existente tiene alcance excesivo.
2. **Definir rol**: documentar en este archivo siguiendo la plantilla estandar (tabla de atributos + artefactos + reglas).
3. **Establecer interacciones**: definir con que agentes interactua y a traves de que artefactos.
4. **Actualizar diagrama**: modificar el diagrama de interaccion en este archivo.
5. **Comunicar**: el Documentation Agent registra el cambio.

### Plantilla para nuevo agente

```markdown
### N. Nombre del Agente

| Atributo | Detalle |
|---|---|
| **Estado** | ACTIVO / PROXIMA FASE / FUTURO |
| **Rol** | Descripcion en una linea |
| **Responsabilidades** | Lista de responsabilidades concretas |
| **Herramientas** | Tecnologias y tools que usa |
| **Se activa cuando** | Condicion de activacion |
| **Interactua con** | Lista de agentes y tipo de interaccion |

**Artefactos que produce:**
- Lista de archivos o documentos

**Reglas especificas:**
- Reglas que aplican solo a este agente
```

### Criterios para justificar un nuevo agente

- El area de responsabilidad es lo suficientemente distinta como para no caber en un agente existente
- Produce artefactos propios que otros agentes consumen
- Tiene reglas especificas que difieren del resto
- Su ausencia genera un cuello de botella o perdida de calidad

---

## Estado actual del sistema

| Agente | Estado | Fase | Notas |
|---|---|---|---|
| Orchestrator | ACTIVO | Fase 0 - Planificacion | Coordinando analisis y documentacion inicial |
| Product Manager | ACTIVO | Fase 0 - Planificacion | Definiendo roadmap y backlog |
| Business Analyst | ACTIVO | Fase 0 - Planificacion | Relevando procesos y reglas de negocio |
| UX/UI | PROXIMA FASE | Fase 1 - Diseno | Se activa cuando las specs SDD esten completas |
| Backend | FUTURO | Fase 2 - Desarrollo | Se activa cuando haya disenos aprobados |
| Frontend | FUTURO | Fase 2 - Desarrollo | Se activa cuando haya APIs funcionales |
| DevOps | FUTURO | Fase 2 - Desarrollo | Se activa en paralelo con Backend |
| QA | FUTURO | Fase 3 - Validacion | Se activa cuando haya codigo implementado |
| Documentation | TRANSVERSAL | Todas las fases | Activo desde el inicio, acompana a todos |

### Progresion de fases

```
Fase 0 (actual)          Fase 1              Fase 2              Fase 3
Planificacion            Diseno              Desarrollo          Validacion
-------------------      ----------------    ----------------    ----------------
[x] Orchestrator         [ ] UX/UI           [ ] Backend         [ ] QA
[x] Product Manager                          [ ] Frontend
[x] Business Analyst                         [ ] DevOps
[x] Documentation (transversal a todas las fases)
```

---

*Ultima actualizacion: 2026-05-29*
*Mantenido por: Documentation Agent bajo supervision del Orchestrator*
