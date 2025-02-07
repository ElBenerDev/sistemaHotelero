"""add notifications table

Revision ID: add_notifications_table
Revises: # aquí irá el ID de tu última migración
Create Date: 2025-02-06 23:37:33.000000

"""
from alembic import op
import sqlalchemy as sa
from src.models.notification import NotificationType

# revision identifiers, used by Alembic.
revision = 'add_notifications_table'
down_revision = None  # Cambia esto al ID de tu última migración
branch_labels = None
depends_on = None

def upgrade():
    # Crear la tabla de notificaciones
    op.create_table('notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.Enum(NotificationType), nullable=False),
        sa.Column('message', sa.String(length=255), nullable=False),
        sa.Column('link', sa.String(length=255), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Crear índices
    op.create_index(op.f('ix_notifications_created_at'), 'notifications', ['created_at'], unique=False)
    op.create_index(op.f('ix_notifications_user_id'), 'notifications', ['user_id'], unique=False)

def downgrade():
    # Eliminar índices
    op.drop_index(op.f('ix_notifications_user_id'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_created_at'), table_name='notifications')
    
    # Eliminar tabla
    op.drop_table('notifications')