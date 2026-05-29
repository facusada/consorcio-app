# CLAUDE.md - Consorcio App

## Descripcion del proyecto

Aplicacion web + PWA para la gestion integral de un consorcio residencial en Argentina. Administra 13 unidades funcionales (7 departamentos + 6 cocheras) pertenecientes a 7 propietarios. Reemplaza el proceso manual actual basado en Excel, WhatsApp y transferencias bancarias por un sistema digitalizado con liquidacion automatica de expensas, gestion de cobranzas, reclamos y proveedores.

Roles de usuario: Administrador, Propietario, Inquilino.

Modulos principales: Expensas, Reclamos/Mantenimiento, Proveedores/Pagos, Cobranzas/Deudas.

## Stack tecnologico

| Capa | Tecnologia |
|------|-----------|
| Backend | FastAPI (Python) |
| Base de datos | PostgreSQL |
| Infraestructura | Docker + Docker Compose |
| Frontend | Nuxt 3 (Vue 3) como PWA |
| Repositorio | GitHub |

## Metodologia de trabajo

### SDD (Specification-Driven Development)

Toda feature arranca con una especificacion antes de escribir codigo.

1. Crear spec en `docs/sdd/wip/<feature>/spec.md`
2. La spec debe incluir: objetivo, alcance, criterios de aceptacion, edge cases, impacto tecnico
3. Una vez aprobada la spec, se crea el ticket y la rama

### TDD (Test-Driven Development)

Ciclo estricto: Red -> Green -> Refactor.

1. Escribir el test que falla (Red)
2. Escribir el codigo minimo para que pase (Green)
3. Refactorizar manteniendo los tests en verde (Refactor)

### Flujo completo

```
SDD (spec) -> Ticket -> Rama -> TDD -> Validacion DB -> PR -> Pipeline -> Merge
```

## Estructura del repositorio

```
consorcio-app/
├── CLAUDE.md                  # Este archivo
├── AGENTS.md                  # Arquitectura de agentes (ver referencia abajo)
├── docs/
│   ├── product/               # Documentacion de producto
│   ├── architecture/
│   │   └── adr/               # Architecture Decision Records
│   └── sdd/
│       ├── wip/               # Specs en progreso
│       ├── done/              # Specs completadas
│       └── archived/          # Specs archivadas
├── backend/                   # FastAPI + PostgreSQL
├── frontend/                  # Nuxt 3 PWA
├── docker-compose.yml
└── .github/                   # Workflows CI/CD
```

## Convencion de commits

Formato obligatorio:

```
feature(modulo): descripcion breve
fix(modulo): descripcion breve
docs(modulo): descripcion breve
test(modulo): descripcion breve
refactor(modulo): descripcion breve
chore(modulo): descripcion breve
```

Modulos validos: `expensas`, `reclamos`, `proveedores`, `cobranzas`, `auth`, `core`, `frontend`, `backend`, `infra`, `docs`.

Ejemplos:
- `feature(expensas): agregar liquidacion mensual automatica`
- `fix(cobranzas): corregir calculo de deuda acumulada`
- `test(expensas): tests unitarios para calculo por indice`

## Referencia a AGENTS.md

La arquitectura de agentes del proyecto esta documentada en `AGENTS.md` en la raiz del repositorio. Consultar ese archivo para entender la organizacion de agentes, sus responsabilidades y como interactuan entre si.

## Reglas de desarrollo

### Control de versiones

- **No pushear directamente a `main`**. Siempre trabajar en ramas feature.
- **PRs obligatorios** para todo merge a `main`.
- Nombrar ramas: `feature/<modulo>-<descripcion>`, `fix/<modulo>-<descripcion>`.
- Ejemplo: `feature/expensas-liquidacion-mensual`, `fix/cobranzas-calculo-deuda`.

### Calidad de codigo

- **Tests antes de merge**: todo PR debe incluir tests que cubran la funcionalidad.
- Los tests deben pasar en el pipeline de CI antes de aprobar el PR.
- Seguir el ciclo TDD estrictamente: no escribir codigo de produccion sin test previo.

### Documentacion

- Toda feature nueva requiere spec en `docs/sdd/wip/` antes de empezar.
- Decisiones de arquitectura se registran como ADR en `docs/architecture/adr/`.
- Specs completadas se mueven de `wip/` a `done/`.

### Base de datos

- Todo cambio de esquema requiere migracion versionada.
- Validar migraciones en entorno local con Docker antes del PR.

## Idioma

Todo el proyecto se escribe en espanol: codigo, documentacion, commits, specs, comentarios y nombres de variables/funciones donde sea posible. Las excepciones son palabras tecnicas sin traduccion natural (e.g., `endpoint`, `middleware`, `query`).

## Logica de negocio clave

### Calculo de expensas

```
expensa_unidad = gasto_total_mes * (indice_unidad / 100)
total_unidad = deuda_ordinaria + expensa_ordinaria + deuda_extraordinaria + expensa_extraordinaria
```

- La deuda se acumula de periodos anteriores.
- Los indices son fijos por unidad funcional y suman 100%.
