"""Add translation tables

Revision ID: 0002
Revises: 0001
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    # Create translations table
    op.create_table('translations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('key', sa.String(length=255), nullable=False),
        sa.Column('locale', sa.String(length=10), nullable=False),
        sa.Column('value', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_translations_key'), 'translations', ['key'], unique=False)
    op.create_index(op.f('ix_translations_locale'), 'translations', ['locale'], unique=False)
    op.create_index(op.f('ix_translations_category'), 'translations', ['category'], unique=False)

    # Create translation_sets table
    op.create_table('translation_sets',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('locale', sa.String(length=10), nullable=False),
        sa.Column('translations', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('version', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_translation_sets_locale'), 'translation_sets', ['locale'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_translation_sets_locale'), table_name='translation_sets')
    op.drop_table('translation_sets')
    op.drop_index(op.f('ix_translations_category'), table_name='translations')
    op.drop_index(op.f('ix_translations_locale'), table_name='translations')
    op.drop_index(op.f('ix_translations_key'), table_name='translations')
    op.drop_table('translations')