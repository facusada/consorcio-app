"""schema inicial: consorcio, unidades, personas, periodos, gastos, liquidaciones

Revision ID: 001
Revises:
Create Date: 2026-05-29

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "consorcios",
        sa.Column("id", sa.UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("nombre", sa.String(200), nullable=False),
        sa.Column("direccion", sa.String(300), nullable=False),
        sa.Column("localidad", sa.String(100), nullable=False),
        sa.Column("provincia", sa.String(100), nullable=False, server_default="Buenos Aires"),
        sa.Column("cuit", sa.String(13), nullable=True),
        sa.Column("reglamento_url", sa.Text(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("cuit"),
    )

    op.create_table(
        "unidades_funcionales",
        sa.Column("id", sa.UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("consorcio_id", sa.UUID(), nullable=False),
        sa.Column("tipo", sa.String(20), nullable=False),
        sa.Column("numero", sa.String(10), nullable=False),
        sa.Column("piso", sa.String(10), nullable=True),
        sa.Column("indice_prorrateo", sa.Numeric(5, 2), nullable=False),
        sa.Column("activa", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["consorcio_id"], ["consorcios.id"]),
        sa.UniqueConstraint("consorcio_id", "tipo", "numero", name="uq_unidad_consorcio_tipo_numero"),
        sa.CheckConstraint("tipo IN ('departamento', 'cochera')", name="ck_unidad_tipo"),
        sa.CheckConstraint("indice_prorrateo > 0 AND indice_prorrateo <= 100", name="ck_unidad_indice"),
    )
    op.create_index("ix_unidad_consorcio_id", "unidades_funcionales", ["consorcio_id"])
    op.create_index("ix_unidad_tipo", "unidades_funcionales", ["tipo"])

    op.create_table(
        "personas",
        sa.Column("id", sa.UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("nombre", sa.String(100), nullable=False),
        sa.Column("apellido", sa.String(100), nullable=False),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("telefono", sa.String(20), nullable=True),
        sa.Column("tipo", sa.String(20), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("tipo IN ('propietario', 'inquilino')", name="ck_persona_tipo"),
    )
    op.create_index("ix_persona_apellido", "personas", ["apellido"])

    op.create_table(
        "unidades_personas",
        sa.Column("id", sa.UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("unidad_id", sa.UUID(), nullable=False),
        sa.Column("persona_id", sa.UUID(), nullable=False),
        sa.Column("rol", sa.String(20), nullable=False),
        sa.Column("fecha_desde", sa.Date(), nullable=False),
        sa.Column("fecha_hasta", sa.Date(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["unidad_id"], ["unidades_funcionales.id"]),
        sa.ForeignKeyConstraint(["persona_id"], ["personas.id"]),
        sa.CheckConstraint("rol IN ('propietario', 'inquilino')", name="ck_unidad_persona_rol"),
        sa.CheckConstraint("fecha_hasta IS NULL OR fecha_hasta >= fecha_desde", name="ck_unidad_persona_fechas"),
    )
    op.create_index("ix_unidad_persona_unidad_id", "unidades_personas", ["unidad_id"])
    op.create_index("ix_unidad_persona_persona_id", "unidades_personas", ["persona_id"])

    op.create_table(
        "usuarios",
        sa.Column("id", sa.UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("persona_id", sa.UUID(), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("rol", sa.String(20), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("last_login", sa.TIMESTAMP(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["persona_id"], ["personas.id"]),
        sa.UniqueConstraint("persona_id"),
        sa.UniqueConstraint("email"),
        sa.CheckConstraint("rol IN ('admin', 'propietario', 'inquilino')", name="ck_usuario_rol"),
    )
    op.create_index("ix_usuario_email", "usuarios", ["email"], unique=True)
    op.create_index("ix_usuario_rol", "usuarios", ["rol"])

    op.create_table(
        "periodos",
        sa.Column("id", sa.UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("consorcio_id", sa.UUID(), nullable=False),
        sa.Column("mes", sa.SmallInteger(), nullable=False),
        sa.Column("anio", sa.SmallInteger(), nullable=False),
        sa.Column("estado", sa.String(20), nullable=False, server_default="abierto"),
        sa.Column("fecha_cierre", sa.Date(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["consorcio_id"], ["consorcios.id"]),
        sa.UniqueConstraint("consorcio_id", "mes", "anio", name="uq_periodo_consorcio_mes_anio"),
        sa.CheckConstraint("mes BETWEEN 1 AND 12", name="ck_periodo_mes"),
        sa.CheckConstraint("anio >= 2020", name="ck_periodo_anio"),
        sa.CheckConstraint("estado IN ('abierto', 'liquidado', 'cerrado')", name="ck_periodo_estado"),
    )
    op.create_index("ix_periodo_consorcio_id", "periodos", ["consorcio_id"])
    op.create_index("ix_periodo_estado", "periodos", ["estado"])
    op.create_index("ix_periodo_anio_mes", "periodos", ["anio", "mes"])

    op.create_table(
        "gastos",
        sa.Column("id", sa.UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("periodo_id", sa.UUID(), nullable=False),
        sa.Column("descripcion", sa.String(300), nullable=False),
        sa.Column("monto", sa.Numeric(12, 2), nullable=False),
        sa.Column("tipo", sa.String(20), nullable=False),
        sa.Column("categoria", sa.String(50), nullable=False),
        sa.Column("fecha", sa.Date(), nullable=False),
        sa.Column("comprobante_url", sa.Text(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["periodo_id"], ["periodos.id"]),
        sa.CheckConstraint("tipo IN ('ordinario', 'extraordinario')", name="ck_gasto_tipo"),
        sa.CheckConstraint("monto > 0", name="ck_gasto_monto_positivo"),
    )
    op.create_index("ix_gasto_periodo_id", "gastos", ["periodo_id"])
    op.create_index("ix_gasto_tipo", "gastos", ["tipo"])
    op.create_index("ix_gasto_categoria", "gastos", ["categoria"])
    op.create_index("ix_gasto_fecha", "gastos", ["fecha"])

    op.create_table(
        "liquidaciones",
        sa.Column("id", sa.UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("periodo_id", sa.UUID(), nullable=False),
        sa.Column("fecha_generacion", sa.TIMESTAMP(), nullable=False, server_default=sa.text("now()")),
        sa.Column("gasto_total_ordinario", sa.Numeric(12, 2), nullable=False),
        sa.Column("gasto_total_extraordinario", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["periodo_id"], ["periodos.id"]),
        sa.UniqueConstraint("periodo_id"),
        sa.CheckConstraint("gasto_total_ordinario >= 0", name="ck_liquidacion_ordinario"),
        sa.CheckConstraint("gasto_total_extraordinario >= 0", name="ck_liquidacion_extraordinario"),
    )
    op.create_index("ix_liquidacion_periodo_id", "liquidaciones", ["periodo_id"], unique=True)

    op.create_table(
        "detalles_expensa",
        sa.Column("id", sa.UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("liquidacion_id", sa.UUID(), nullable=False),
        sa.Column("unidad_id", sa.UUID(), nullable=False),
        sa.Column("indice", sa.Numeric(5, 2), nullable=False),
        sa.Column("monto_ordinario", sa.Numeric(12, 2), nullable=False),
        sa.Column("monto_extraordinario", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("deuda_ordinaria", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("deuda_extraordinaria", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("total", sa.Numeric(12, 2), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["liquidacion_id"], ["liquidaciones.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["unidad_id"], ["unidades_funcionales.id"]),
        sa.UniqueConstraint("liquidacion_id", "unidad_id", name="uq_detalle_liquidacion_unidad"),
        sa.CheckConstraint("monto_ordinario >= 0", name="ck_detalle_ordinario"),
        sa.CheckConstraint("monto_extraordinario >= 0", name="ck_detalle_extraordinario"),
        sa.CheckConstraint("deuda_ordinaria >= 0", name="ck_detalle_deuda_ordinaria"),
        sa.CheckConstraint("deuda_extraordinaria >= 0", name="ck_detalle_deuda_extraordinaria"),
        sa.CheckConstraint("total >= 0", name="ck_detalle_total"),
    )
    op.create_index("ix_detalle_liquidacion_id", "detalles_expensa", ["liquidacion_id"])
    op.create_index("ix_detalle_unidad_id", "detalles_expensa", ["unidad_id"])


def downgrade() -> None:
    op.drop_table("detalles_expensa")
    op.drop_table("liquidaciones")
    op.drop_table("gastos")
    op.drop_table("periodos")
    op.drop_table("usuarios")
    op.drop_table("unidades_personas")
    op.drop_table("personas")
    op.drop_table("unidades_funcionales")
    op.drop_table("consorcios")
