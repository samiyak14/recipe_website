"""Added is_premium column

Revision ID: 74d7f7632a41
Revises: cf1567be911d
Create Date: 2025-03-11 19:02:31.934113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74d7f7632a41'
down_revision = 'cf1567be911d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_recipe')
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tags', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('instructions', sa.Text(), nullable=False))
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.drop_column('steps')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.add_column(sa.Column('steps', sa.TEXT(), nullable=False))
        batch_op.alter_column('title',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.drop_column('instructions')
        batch_op.drop_column('tags')

    op.create_table('_alembic_tmp_recipe',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), nullable=False),
    sa.Column('image_path', sa.VARCHAR(length=255), nullable=True),
    sa.Column('video_path', sa.VARCHAR(length=255), nullable=True),
    sa.Column('tags', sa.VARCHAR(length=255), nullable=True),
    sa.Column('instructions', sa.TEXT(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
