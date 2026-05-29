"""seed: datos reales del consorcio (unidades, propietarios, vinculos, admin)

Revision ID: 002
Revises: 001
Create Date: 2026-05-29

"""
from datetime import date
from typing import Sequence, Union

import bcrypt
import sqlalchemy as sa
from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

CONSORCIO_ID = "00000000-0000-0000-0000-000000000001"

UNIDADES = [
    ("10000000-0000-0000-0000-000000000001", "departamento", "1", "1", "16.68"),
    ("10000000-0000-0000-0000-000000000002", "departamento", "2", "2", "13.13"),
    ("10000000-0000-0000-0000-000000000003", "departamento", "3", "3", "12.91"),
    ("10000000-0000-0000-0000-000000000004", "departamento", "4", "4", "13.13"),
    ("10000000-0000-0000-0000-000000000005", "departamento", "5", "5", "12.91"),
    ("10000000-0000-0000-0000-000000000006", "departamento", "6", "6", "13.13"),
    ("10000000-0000-0000-0000-000000000007", "departamento", "7", "7", "12.91"),
    ("10000000-0000-0000-0000-00000000000A", "cochera", "A", None, "0.85"),
    ("10000000-0000-0000-0000-00000000000B", "cochera", "B", None, "0.85"),
    ("10000000-0000-0000-0000-00000000000C", "cochera", "C", None, "0.85"),
    ("10000000-0000-0000-0000-00000000000D", "cochera", "D", None, "0.85"),
    ("10000000-0000-0000-0000-00000000000E", "cochera", "E", None, "0.85"),
    ("10000000-0000-0000-0000-00000000000F", "cochera", "F", None, "0.95"),
]

# (id, nombre, apellido, email, tipo)
PERSONAS = [
    ("20000000-0000-0000-0000-000000000001", "Pamela", "Pitscheider", None, "propietario"),
    ("20000000-0000-0000-0000-000000000002", "Elena", "Michailenko", None, "propietario"),
    ("20000000-0000-0000-0000-000000000003", "Eliana", "Iafolla", None, "propietario"),
    ("20000000-0000-0000-0000-000000000004", "Claudio", "Ghida", None, "propietario"),
    ("20000000-0000-0000-0000-000000000005", "Maria", "Duarte", None, "propietario"),
    ("20000000-0000-0000-0000-000000000006", "Graciela", "Farina", None, "propietario"),
    ("20000000-0000-0000-0000-000000000007", "Lautaro", "Villordo", None, "propietario"),
]

# (unidad_id, persona_id)
VINCULOS = [
    ("10000000-0000-0000-0000-000000000001", "20000000-0000-0000-0000-000000000001"),  # Depto1 -> Pitscheider
    ("10000000-0000-0000-0000-000000000002", "20000000-0000-0000-0000-000000000002"),  # Depto2 -> Michailenko
    ("10000000-0000-0000-0000-00000000000E", "20000000-0000-0000-0000-000000000002"),  # CochE -> Michailenko
    ("10000000-0000-0000-0000-00000000000F", "20000000-0000-0000-0000-000000000002"),  # CochF -> Michailenko
    ("10000000-0000-0000-0000-000000000003", "20000000-0000-0000-0000-000000000003"),  # Depto3 -> Iafolla
    ("10000000-0000-0000-0000-00000000000C", "20000000-0000-0000-0000-000000000003"),  # CochC -> Iafolla
    ("10000000-0000-0000-0000-000000000004", "20000000-0000-0000-0000-000000000004"),  # Depto4 -> Ghida
    ("10000000-0000-0000-0000-000000000005", "20000000-0000-0000-0000-000000000005"),  # Depto5 -> Duarte
    ("10000000-0000-0000-0000-00000000000D", "20000000-0000-0000-0000-000000000005"),  # CochD -> Duarte
    ("10000000-0000-0000-0000-000000000006", "20000000-0000-0000-0000-000000000006"),  # Depto6 -> Farina
    ("10000000-0000-0000-0000-00000000000B", "20000000-0000-0000-0000-000000000006"),  # CochB -> Farina
    ("10000000-0000-0000-0000-000000000007", "20000000-0000-0000-0000-000000000007"),  # Depto7 -> Villordo
    ("10000000-0000-0000-0000-00000000000A", "20000000-0000-0000-0000-000000000007"),  # CochA -> Villordo
]

ADMIN_PERSONA_ID = "20000000-0000-0000-0000-000000000099"
ADMIN_USUARIO_ID = "30000000-0000-0000-0000-000000000001"
ADMIN_EMAIL = "admin@consorcio.local"
ADMIN_PASSWORD = "Admin1234!"


def upgrade() -> None:
    conn = op.get_bind()

    conn.execute(
        sa.text("""
            INSERT INTO consorcios (id, nombre, direccion, localidad, provincia)
            VALUES (:id, :nombre, :direccion, :localidad, :provincia)
        """),
        {
            "id": CONSORCIO_ID,
            "nombre": "Consorcio de Propietarios",
            "direccion": "Direccion del Edificio",
            "localidad": "Localidad",
            "provincia": "Buenos Aires",
        },
    )

    for uid, tipo, numero, piso, indice in UNIDADES:
        conn.execute(
            sa.text("""
                INSERT INTO unidades_funcionales (id, consorcio_id, tipo, numero, piso, indice_prorrateo)
                VALUES (:id, :consorcio_id, :tipo, :numero, :piso, :indice)
            """),
            {
                "id": uid, "consorcio_id": CONSORCIO_ID,
                "tipo": tipo, "numero": numero, "piso": piso, "indice": indice,
            },
        )

    for pid, nombre, apellido, email, tipo in PERSONAS:
        conn.execute(
            sa.text("""
                INSERT INTO personas (id, nombre, apellido, email, tipo)
                VALUES (:id, :nombre, :apellido, :email, :tipo)
            """),
            {"id": pid, "nombre": nombre, "apellido": apellido, "email": email, "tipo": tipo},
        )

    for unidad_id, persona_id in VINCULOS:
        conn.execute(
            sa.text("""
                INSERT INTO unidades_personas (id, unidad_id, persona_id, rol, fecha_desde)
                VALUES (gen_random_uuid(), :unidad_id, :persona_id, 'propietario', :fecha)
            """),
            {"unidad_id": unidad_id, "persona_id": persona_id, "fecha": date(2024, 1, 1)},
        )

    conn.execute(
        sa.text("""
            INSERT INTO personas (id, nombre, apellido, email, tipo)
            VALUES (:id, 'Administrador', 'Sistema', :email, 'propietario')
        """),
        {"id": ADMIN_PERSONA_ID, "email": ADMIN_EMAIL},
    )

    password_hash = bcrypt.hashpw(ADMIN_PASSWORD.encode(), bcrypt.gensalt()).decode()
    conn.execute(
        sa.text("""
            INSERT INTO usuarios (id, persona_id, email, password_hash, rol)
            VALUES (:id, :persona_id, :email, :hash, 'admin')
        """),
        {
            "id": ADMIN_USUARIO_ID,
            "persona_id": ADMIN_PERSONA_ID,
            "email": ADMIN_EMAIL,
            "hash": password_hash,
        },
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM usuarios WHERE id = :id"), {"id": ADMIN_USUARIO_ID})
    conn.execute(sa.text("DELETE FROM personas WHERE id = :id"), {"id": ADMIN_PERSONA_ID})
    conn.execute(sa.text("DELETE FROM unidades_personas WHERE unidad_id IN (SELECT id FROM unidades_funcionales WHERE consorcio_id = :id)"), {"id": CONSORCIO_ID})
    conn.execute(sa.text("DELETE FROM personas WHERE id IN (:p1,:p2,:p3,:p4,:p5,:p6,:p7)"), {
        "p1": "20000000-0000-0000-0000-000000000001",
        "p2": "20000000-0000-0000-0000-000000000002",
        "p3": "20000000-0000-0000-0000-000000000003",
        "p4": "20000000-0000-0000-0000-000000000004",
        "p5": "20000000-0000-0000-0000-000000000005",
        "p6": "20000000-0000-0000-0000-000000000006",
        "p7": "20000000-0000-0000-0000-000000000007",
    })
    conn.execute(sa.text("DELETE FROM unidades_funcionales WHERE consorcio_id = :id"), {"id": CONSORCIO_ID})
    conn.execute(sa.text("DELETE FROM consorcios WHERE id = :id"), {"id": CONSORCIO_ID})
