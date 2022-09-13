"""empty message

Revision ID: c0effbb32638
Revises: 24674d14e611
Create Date: 2022-09-13 12:17:24.460908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0effbb32638'
down_revision = '24674d14e611'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('piece', sa.Column('image_url', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'piece', ['image_url'])
    op.drop_column('piece', 'image')
    op.drop_column('piece', 'mimetype')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('piece', sa.Column('mimetype', sa.TEXT(), nullable=False))
    op.add_column('piece', sa.Column('image', sa.VARCHAR(length=36), nullable=True))
    op.drop_constraint(None, 'piece', type_='unique')
    op.drop_column('piece', 'image_url')
    # ### end Alembic commands ###
