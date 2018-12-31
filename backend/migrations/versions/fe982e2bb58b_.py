"""empty message

Revision ID: fe982e2bb58b
Revises: f753a6101f34
Create Date: 2018-12-30 23:28:40.000975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe982e2bb58b'
down_revision = 'f753a6101f34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('discordserver', sa.Column('admin_role', sa.BIGINT(), nullable=True))
    op.drop_column('discordserver', 'admin_roles')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('discordserver', sa.Column('admin_roles', sa.BIGINT(), autoincrement=False, nullable=True))
    op.drop_column('discordserver', 'admin_role')
    # ### end Alembic commands ###
