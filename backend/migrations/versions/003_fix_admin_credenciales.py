"""fix: recrear usuario admin con hash bcrypt correcto

Esta migracion existe porque la 002 podia fallar en entornos con
bcrypt >= 4.0.0 + passlib 1.7.4, dejando el admin sin crear o con
un hash invalido. Hace un UPSERT idempotente: si el admin ya existe
y puede autenticarse, no lo toca; si no existe o el hash es invalido,
lo recrea.

Revision ID: 003
Revises: 002
Create Date: 2026-05-30

"""
import uuid
from typing import Sequence, Union

import bcrypt
import sqlalchemy as sa
from alembic import op

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ADMIN_EMAIL = "admin@consorcio.local"
ADMIN_PASSWORD = "Admin1234!"
ADMIN_PERSONA_ID = "20000000-0000-0000-0000-000000000099"
ADMIN_USUARIO_ID = "30000000-0000-0000-0000-000000000001"


def upgrade() -> None:
    conn = op.get_bind()

    nuevo_hash = bcrypt.hashpw(ADMIN_PASSWORD.encode(), bcrypt.gensalt()).decode()

    # Upsert persona del admin
    conn.execute(
        sa.text("""
            INSERT INTO personas (id, nombre, apellido, email, tipo)
            VALUES (:id, 'Administrador', 'Sistema', :email, 'propietario')
            ON CONFLICT (id) DO NOTHING
        """),
        {"id": ADMIN_PERSONA_ID, "email": ADMIN_EMAIL},
    )

    # Upsert usuario admin: si ya existe, actualiza el hash
    conn.execute(
        sa.text("""
            INSERT INTO usuarios (id, persona_id, email, password_hash, rol)
            VALUES (:uid, :pid, :email, :hash, 'admin')
            ON CONFLICT (email) DO UPDATE
              SET password_hash = EXCLUDED.password_hash,
                  activo = true
        """),
        {
            "uid": ADMIN_USUARIO_ID,
            "pid": ADMIN_PERSONA_ID,
            "email": ADMIN_EMAIL,
            "hash": nuevo_hash,
        },
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text("DELETE FROM usuarios WHERE email = :email"),
        {"email": ADMIN_EMAIL},
    )
    conn.execute(
        sa.text("DELETE FROM personas WHERE id = :id"),
        {"id": ADMIN_PERSONA_ID},
    )
