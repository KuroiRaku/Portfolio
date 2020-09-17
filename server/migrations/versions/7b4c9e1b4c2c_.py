"""Create Project and User models.

Revision ID: 7b4c9e1b4c2c
Revises: 
Create Date: 2018-08-11 15:21:30.561878

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '7b4c9e1b4c2c'
down_revision = None
branch_labels = None
depends_on = None


# pylint: disable=E1101
def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'project',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=30), nullable=False),
        sa.Column('imgfile', sa.String(length=30), nullable=False),
        sa.Column('website', sqlalchemy_utils.types.url.URLType(), nullable=True),
        sa.Column('github_url', sqlalchemy_utils.types.url.URLType(), nullable=False),
        sa.Column('abandoned', sa.Boolean(), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('long_desc', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('title')
    )
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=30), nullable=False),
        sa.Column('password_hash', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('project')
    # ### end Alembic commands ###