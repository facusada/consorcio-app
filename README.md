# Consorcio App

Aplicacion web y PWA para la gestion integral de un consorcio residencial en Argentina. Reemplaza el flujo manual basado en planillas Excel, PDFs y mensajes de WhatsApp por una plataforma centralizada donde administradores, propietarios e inquilinos pueden gestionar expensas, reclamos, pagos y deudas.

El sistema esta diseñado para un consorcio de 13 unidades funcionales (7 departamentos + 6 cocheras) con 7 propietarios, pero su arquitectura permite escalar a otros consorcios en el futuro.

## Problema que resuelve

Hoy la administracion del consorcio se realiza de forma completamente manual:

- **Calculo de expensas** en Excel (gasto total x indice de cada unidad)
- **Distribucion** mediante PDF enviado al grupo de WhatsApp
- **Cobros y pagos** a traves de una cuenta bancaria personal (Uala)
- **Seguimiento de deudas** trackeado manualmente en la misma planilla
- **Reclamos y mantenimiento** gestionados por mensajes informales

Esto genera errores de calculo, falta de trazabilidad, demoras en la comunicacion y carga administrativa innecesaria. Consorcio App automatiza estos procesos y brinda transparencia a todos los involucrados.

## Stack tecnologico

| Capa | Tecnologia |
|------|-----------|
| Backend | FastAPI (Python) |
| Base de datos | PostgreSQL |
| Frontend | Nuxt 3 (Vue 3) + PWA |
| Infraestructura | Docker / Docker Compose |
| Repositorio | GitHub |

## Estado actual

**Fase: Analisis y Planificacion**

El proyecto se encuentra en etapa de definicion de arquitectura, modelado de dominio y especificacion de features. No hay codigo de aplicacion implementado todavia. Toda la actividad actual esta en la carpeta `docs/`.

## Estructura del repositorio

```
consorcio-app/
├── docs/
│   ├── product/          # Documentacion de producto (PRD, user stories)
│   ├── architecture/     # Arquitectura tecnica
│   │   └── adr/          # Architecture Decision Records
│   └── sdd/              # Specification-Driven Development
│       ├── wip/          # Specs en progreso
│       ├── done/         # Specs completadas
│       └── archived/     # Specs archivadas
├── .github/              # Configuracion de GitHub (CI/CD, templates)
└── README.md
```

Las carpetas de codigo (`backend/`, `frontend/`, etc.) se crearan cuando comience la fase de implementacion.

## Metodologia

El proyecto sigue **SDD (Specification-Driven Development)** combinado con **TDD (Test-Driven Development)**:

1. **Spec primero** -- Toda feature arranca con una especificacion en `docs/sdd/wip/<feature>/spec.md` que incluye objetivo, alcance, criterios de aceptacion, edge cases e impacto tecnico.
2. **Ticket y rama** -- De la spec se crea el ticket y la rama de trabajo.
3. **TDD** -- Red, Green, Refactor. Los tests se escriben antes que el codigo de produccion.
4. **Validacion** -- Verificacion contra la base de datos y criterios de aceptacion.
5. **PR y merge** -- Pipeline de CI, code review y merge a main.

Las decisiones de arquitectura se documentan como ADRs en `docs/architecture/adr/`.

### Convenciones de commits

```
feature(modulo): descripcion
fix(modulo): descripcion
docs(modulo): descripcion
```

## Como contribuir

1. Leer la documentacion en `docs/` para entender el contexto del proyecto.
2. Revisar las specs existentes en `docs/sdd/`.
3. Seguir el flujo SDD/TDD descrito arriba para cualquier nueva feature o correccion.
4. Abrir un PR con descripcion clara y referencia a la spec correspondiente.

## Licencia

Por definir.
