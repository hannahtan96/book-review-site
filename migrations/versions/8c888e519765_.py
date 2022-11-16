"""empty message

Revision ID: 8c888e519765
Revises: 262ae0d57a3c
Create Date: 2022-11-11 23:26:13.394821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c888e519765'
down_revision = '262ae0d57a3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book', 'description')
    # ### end Alembic commands ###