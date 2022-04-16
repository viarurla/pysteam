"""empty message

Revision ID: 01c9dae0f6c7
Revises: 47772eebc191
Create Date: 2022-04-16 15:02:17.135798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01c9dae0f6c7'
down_revision = '47772eebc191'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('steam_app_details')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('steam_app_details',
    sa.Column('steam_appid', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('type', sa.VARCHAR(), nullable=True),
    sa.Column('is_free', sa.BOOLEAN(), nullable=True),
    sa.Column('about_the_game', sa.VARCHAR(), nullable=True),
    sa.Column('header_image', sa.VARCHAR(), nullable=True),
    sa.Column('platforms_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['platforms_id'], ['platforms.id'], ),
    sa.PrimaryKeyConstraint('steam_appid'),
    sa.UniqueConstraint('steam_appid')
    )
    # ### end Alembic commands ###
