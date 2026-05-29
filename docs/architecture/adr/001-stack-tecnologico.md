# ADR-001: Stack Tecnologico

## Estado

Aceptado.

## Fecha

2026-05-29.

## Contexto

Se necesita definir el stack tecnologico para una aplicacion web + PWA de gestion de consorcio residencial en Argentina. La aplicacion debe soportar 3 roles de usuario (administrador, propietario, inquilino) y cubrir modulos de expensas, reclamos/mantenimiento, proveedores/pagos y cobranzas/deudas.

El desarrollador principal tiene experiencia diaria con FastAPI, PostgreSQL y Docker en backend, y experiencia con Vue/Nuxt para frontend. Se adopta la metodologia SDD (Specification-Driven Development) combinada con TDD (Test-Driven Development).

## Decision

- **Backend**: FastAPI (Python 3.12+)
- **Base de datos**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.x con Alembic para migraciones
- **Contenedores**: Docker + Docker Compose
- **Frontend**: Nuxt 3 como PWA
- **Autenticacion**: JWT con roles (admin, propietario, inquilino)
- **Estructura de repositorio**: Monorepo con directorios `backend/` y `frontend/`

## Alternativas consideradas

### Django REST Framework

- Framework mas opinado con admin panel integrado.
- Descartado porque agrega complejidad innecesaria para una API centrada en JSON. FastAPI ofrece mejor rendimiento, tipado nativo con Pydantic y documentacion automatica con OpenAPI.

### Node.js + Express

- Permite compartir lenguaje entre frontend y backend.
- Descartado porque el desarrollador tiene mayor dominio de Python y el ecosistema de FastAPI resuelve mejor las necesidades de validacion, documentacion y async.

### Dos repositorios separados (backend y frontend)

- Desacoplamiento total entre servicios.
- Descartado para simplificar la gestion en etapa inicial. Un monorepo permite compartir configuracion de CI/CD, documentacion unificada y coordinacion mas simple de versiones. Se puede migrar a repos separados en el futuro si escala el equipo.

### React / Next.js

- Ecosistema mas grande y mayor cantidad de librerias.
- Descartado porque el desarrollador ya trabaja con Vue/Nuxt y no hay ventaja tecnica que justifique el cambio de stack.

## Justificacion

1. **Familiaridad del desarrollador**: FastAPI + PostgreSQL + Docker es el stack de uso diario, lo que reduce la curva de aprendizaje y acelera el desarrollo.
2. **Ecosistema maduro**: SQLAlchemy y Alembic tienen soporte solido para migraciones, relaciones complejas y queries optimizadas. FastAPI genera documentacion OpenAPI automatica.
3. **Containerizacion**: Docker Compose permite levantar backend, base de datos y cualquier servicio auxiliar con un solo comando, tanto en desarrollo como en produccion.
4. **PWA nativa**: Nuxt 3 tiene soporte integrado para PWA, lo que permite a los propietarios instalar la app en el celular sin pasar por las tiendas de aplicaciones.
5. **Tipado de punta a punta**: Pydantic en backend + TypeScript en frontend aseguran validacion y contratos claros entre capas.
6. **Compatibilidad con SDD/TDD**: FastAPI con Pydantic facilita definir contratos de API antes de implementar (SDD), y pytest se integra naturalmente para el ciclo Red-Green-Refactor (TDD).

## Consecuencias

### Positivas

- Desarrollo rapido gracias al dominio previo del stack.
- Documentacion de API autogenerada (Swagger/ReDoc) disponible desde el dia uno.
- Entorno reproducible con Docker para cualquier colaborador o entorno de deploy.
- PWA permite acceso movil sin publicacion en tiendas.
- Testing integrado: pytest para backend, Vitest/Playwright para frontend.

### Negativas

- Python es single-threaded por defecto; se necesita configuracion de workers (uvicorn con gunicorn) para manejar concurrencia en produccion.
- Monorepo requiere disciplina en la estructura de directorios y en el pipeline de CI/CD para no acoplar los deploys.
- SQLAlchemy 2.x tiene una API distinta a la 1.x; hay que verificar compatibilidad de librerias y tutoriales.
- Nuxt 3 agrega complejidad de framework respecto a una SPA pura con Vue, aunque el beneficio de PWA y SSR lo justifica.

## Notas

- Este ADR se complementa con la metodologia SDD/TDD definida para el proyecto. Toda feature debe arrancar con una spec en `docs/sdd/wip/<feature>/spec.md` antes de escribir codigo.
- Las decisiones de arquitectura futuras (estructura de base de datos, estrategia de deploy, integraciones externas) se documentaran en ADRs separados.
