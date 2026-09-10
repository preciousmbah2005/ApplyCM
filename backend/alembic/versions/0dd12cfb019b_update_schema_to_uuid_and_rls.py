"""Update schema to UUID and enable RLS policies

Revision ID: 0dd12cfb019b
Revises: 0dd12cfb019a
Create Date: 2026-08-19 09:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '0dd12cfb019b'
down_revision: Union[str, Sequence[str], None] = '0dd12cfb019a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Enable required extensions
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

    # 2. Drop old integer tables if they exist
    op.execute("DROP TABLE IF EXISTS favorites CASCADE;")
    op.execute("DROP TABLE IF EXISTS documents CASCADE;")
    op.execute("DROP TABLE IF EXISTS applications CASCADE;")
    op.execute("DROP TABLE IF EXISTS student_profiles CASCADE;")
    op.execute("DROP TABLE IF EXISTS programs CASCADE;")
    op.execute("DROP TABLE IF EXISTS schools CASCADE;")
    op.execute("DROP TABLE IF EXISTS users CASCADE;")

    # 3. Create Users table (UUID)
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=True),
        sa.Column('role', sa.String(), server_default=sa.text("'student'"), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # 4. Create Student Profiles table (UUID)
    op.create_table(
        'student_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('education_summary', sa.Text(), nullable=True),
        sa.Column('writing_sample', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', name='uq_student_profiles_user')
    )
    op.create_index(op.f('ix_student_profiles_id'), 'student_profiles', ['id'], unique=False)

    # 5. Create Schools table (UUID)
    op.create_table(
        'schools',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('city', sa.String(), nullable=True),
        sa.Column('arrondissement', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_schools_id'), 'schools', ['id'], unique=False)
    op.create_index('idx_schools_city', 'schools', ['city'], unique=False)

    # 6. Create Programs table (UUID)
    op.create_table(
        'programs',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('school_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('field_of_study', sa.String(), nullable=False),
        sa.Column('tuition', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('admission_requirements', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_programs_id'), 'programs', ['id'], unique=False)
    op.create_index('idx_programs_school_id', 'programs', ['school_id'], unique=False)
    op.create_index('idx_programs_field_of_study', 'programs', ['field_of_study'], unique=False)

    # 7. Create Applications table (UUID)
    op.create_table(
        'applications',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('student_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('program_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(), server_default=sa.text("'submitted'"), nullable=False),
        sa.Column('submitted_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['program_id'], ['programs.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['student_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('student_id', 'program_id', name='uq_applications_student_program')
    )
    op.create_index(op.f('ix_applications_id'), 'applications', ['id'], unique=False)
    op.create_index('idx_applications_student_id', 'applications', ['student_id'], unique=False)
    op.create_index('idx_applications_program_id', 'applications', ['program_id'], unique=False)
    op.create_index('idx_applications_status', 'applications', ['status'], unique=False)

    # 8. Create Favorites table (UUID)
    op.create_table(
        'favorites',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('student_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('school_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['school_id'], ['schools.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['student_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('student_id', 'school_id', name='uq_favorites_student_school')
    )
    op.create_index(op.f('ix_favorites_id'), 'favorites', ['id'], unique=False)
    op.create_index('idx_favorites_student_id', 'favorites', ['student_id'], unique=False)
    op.create_index('idx_favorites_school_id', 'favorites', ['school_id'], unique=False)

    # 9. Create Documents table (UUID)
    op.create_table(
        'documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('student_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('file_url', sa.String(), nullable=False),
        sa.Column('doc_type', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['student_id'], ['student_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documents_id'), 'documents', ['id'], unique=False)
    op.create_index('idx_documents_student_id', 'documents', ['student_id'], unique=False)

    # NOTE: Row Level Security was intentionally removed.
    #
    # The original policies depended on Supabase primitives that do not exist on
    # pure PostgreSQL: the `auth.uid()` function and the `authenticated` role.
    # ApplyCM runs on Neon with no BaaS layer, so authorization is enforced in
    # the application tier by `app.dependencies.get_current_user` and the
    # service layer, which scope every query to the authenticated student.
    #
    # These policies would also have been inert in practice: the backend
    # connects as the table owner, and owners bypass RLS unless the table is
    # explicitly marked FORCE ROW LEVEL SECURITY.


def downgrade() -> None:
    op.execute("DROP FUNCTION IF EXISTS current_student_id() CASCADE;")
    op.execute("DROP TABLE IF EXISTS favorites CASCADE;")
    op.execute("DROP TABLE IF EXISTS documents CASCADE;")
    op.execute("DROP TABLE IF EXISTS applications CASCADE;")
    op.execute("DROP TABLE IF EXISTS student_profiles CASCADE;")
    op.execute("DROP TABLE IF EXISTS programs CASCADE;")
    op.execute("DROP TABLE IF EXISTS schools CASCADE;")
    op.execute("DROP TABLE IF EXISTS users CASCADE;")
