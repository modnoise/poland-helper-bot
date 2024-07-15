"""FirstMigration

Revision ID: 7792aded0544
Revises: 
Create Date: 2024-07-15 21:48:43.917915

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7792aded0544'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('telegram_id', sa.BIGINT(), nullable=True),
    sa.Column('username', sa.VARCHAR(length=128), nullable=True),
    sa.Column('full_name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('active', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.Column('messages_limit', sa.Integer(), nullable=True),
    sa.Column('language', sa.VARCHAR(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.Column('is_verify', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.Column('invite_code', sa.String(length=255), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('telegram_id')
    )
    op.create_table('message_statistics',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('messages_total', sa.Integer(), nullable=True),
    sa.Column('messages_today', sa.Integer(), nullable=True),
    sa.Column('messages_hour', sa.Integer(), nullable=True),
    sa.Column('last_message_time', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('message_store',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.UUID(), nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['session_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message_store')
    op.drop_table('message_statistics')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('invites')
    # ### end Alembic commands ###