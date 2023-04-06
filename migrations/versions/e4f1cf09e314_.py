"""empty message

Revision ID: e4f1cf09e314
Revises: bed1f2477feb
Create Date: 2023-04-06 20:38:32.190042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4f1cf09e314'
down_revision = 'bed1f2477feb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('homework_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('due_date', sa.String(length=50), nullable=True))

    with op.batch_alter_table('homework', schema=None) as batch_op:
        batch_op.drop_column('file_data')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('homework', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file_data', sa.BLOB(), nullable=True))

    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.drop_column('due_date')
        batch_op.drop_column('homework_id')

    # ### end Alembic commands ###
