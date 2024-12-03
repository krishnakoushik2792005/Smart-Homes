"""empty message

Revision ID: f79c8d82e1d2
Revises: 
Create Date: 2024-11-16 13:40:58.102552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f79c8d82e1d2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('listing',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('contact_name', sa.String(length=100), nullable=False),
    sa.Column('contact_phone', sa.String(length=20), nullable=False),
    sa.Column('video_filename', sa.String(length=100), nullable=False),
    sa.Column('listing_type', sa.String(length=10), nullable=False),
    sa.Column('city_type', sa.String(length=50), nullable=True),
    sa.Column('area', sa.String(length=100), nullable=True),
    sa.Column('specifications', sa.Text(), nullable=True),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('listing')
    op.drop_table('user')
    # ### end Alembic commands ###