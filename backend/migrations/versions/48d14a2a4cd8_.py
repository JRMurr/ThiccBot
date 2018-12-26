"""empty message

Revision ID: 48d14a2a4cd8
Revises: 
Create Date: 2018-12-26 15:48:46.164064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48d14a2a4cd8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('discordserver', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.BIGINT(),
               autoincrement=True,
               existing_server_default=sa.text("nextval('discordserver_id_seq'::regclass)"))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('discordserver', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.INTEGER(),
               autoincrement=True,
               existing_server_default=sa.text("nextval('discordserver_id_seq'::regclass)"))
    # ### end Alembic commands ###
