"""Initial migration

Revision ID: 0001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enum types
    op.execute("CREATE TYPE user_role AS ENUM ('superadmin', 'business', 'customer')")
    op.execute("CREATE TYPE request_status AS ENUM ('pending', 'approved', 'rejected')")
    op.execute("CREATE TYPE plan_status AS ENUM ('active', 'completed', 'defaulted', 'cancelled')")
    op.execute("CREATE TYPE payment_status AS ENUM ('pending', 'paid', 'overdue', 'cancelled')")
    op.execute("CREATE TYPE alert_type AS ENUM ('rapid_requests', 'high_debt_ratio', 'cross_business_chain', 'payment_default_pattern')")
    op.execute("CREATE TYPE alert_severity AS ENUM ('low', 'medium', 'high', 'critical')")
    op.execute("CREATE TYPE alert_status AS ENUM ('active', 'investigating', 'resolved', 'false_positive')")

    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', postgresql.ENUM('superadmin', 'business', 'customer', name='user_role'), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)
    op.create_index(op.f('ix_users_is_active'), 'users', ['is_active'], unique=False)

    # Create businesses table
    op.create_table('businesses',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('business_name', sa.String(length=255), nullable=False),
        sa.Column('business_type', sa.String(length=100), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('registration_number', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_businesses_owner_id'), 'businesses', ['owner_id'], unique=False)
    op.create_index(op.f('ix_businesses_is_verified'), 'businesses', ['is_verified'], unique=False)

    # Create installment_requests table
    op.create_table('installment_requests',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('customer_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('business_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('product_name', sa.String(length=255), nullable=False),
        sa.Column('product_description', sa.Text(), nullable=True),
        sa.Column('product_value', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('installment_months', sa.Integer(), nullable=False),
        sa.Column('monthly_amount', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('status', postgresql.ENUM('pending', 'approved', 'rejected', name='request_status'), nullable=True),
        sa.Column('business_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['customer_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_installment_requests_customer_id'), 'installment_requests', ['customer_id'], unique=False)
    op.create_index(op.f('ix_installment_requests_business_id'), 'installment_requests', ['business_id'], unique=False)
    op.create_index(op.f('ix_installment_requests_status'), 'installment_requests', ['status'], unique=False)
    op.create_index(op.f('ix_installment_requests_created_at'), 'installment_requests', ['created_at'], unique=False)

    # Create installment_plans table
    op.create_table('installment_plans',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('request_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('customer_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('business_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('total_amount', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('paid_amount', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('remaining_amount', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('total_installments', sa.Integer(), nullable=False),
        sa.Column('paid_installments', sa.Integer(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('status', postgresql.ENUM('active', 'completed', 'defaulted', 'cancelled', name='plan_status'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['customer_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['request_id'], ['installment_requests.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_installment_plans_customer_id'), 'installment_plans', ['customer_id'], unique=False)
    op.create_index(op.f('ix_installment_plans_business_id'), 'installment_plans', ['business_id'], unique=False)
    op.create_index(op.f('ix_installment_plans_status'), 'installment_plans', ['status'], unique=False)
    op.create_index(op.f('ix_installment_plans_start_date'), 'installment_plans', ['start_date', 'end_date'], unique=False)

    # Create payments table
    op.create_table('payments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('plan_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=False),
        sa.Column('paid_date', sa.Date(), nullable=True),
        sa.Column('status', postgresql.ENUM('pending', 'paid', 'overdue', 'cancelled', name='payment_status'), nullable=True),
        sa.Column('payment_method', sa.String(length=50), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['plan_id'], ['installment_plans.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payments_plan_id'), 'payments', ['plan_id'], unique=False)
    op.create_index(op.f('ix_payments_status'), 'payments', ['status'], unique=False)
    op.create_index(op.f('ix_payments_due_date'), 'payments', ['due_date'], unique=False)

    # Create fraud_alerts table
    op.create_table('fraud_alerts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('customer_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('alert_type', postgresql.ENUM('rapid_requests', 'high_debt_ratio', 'cross_business_chain', 'payment_default_pattern', name='alert_type'), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('alert_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('severity', postgresql.ENUM('low', 'medium', 'high', 'critical', name='alert_severity'), nullable=False),
        sa.Column('status', postgresql.ENUM('active', 'investigating', 'resolved', 'false_positive', name='alert_status'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fraud_alerts_customer_id'), 'fraud_alerts', ['customer_id'], unique=False)
    op.create_index(op.f('ix_fraud_alerts_alert_type'), 'fraud_alerts', ['alert_type'], unique=False)
    op.create_index(op.f('ix_fraud_alerts_status'), 'fraud_alerts', ['status'], unique=False)
    op.create_index(op.f('ix_fraud_alerts_created_at'), 'fraud_alerts', ['created_at'], unique=False)

    # Create fraud_patterns table
    op.create_table('fraud_patterns',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('customer_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('pattern_type', sa.String(length=100), nullable=False),
        sa.Column('pattern_data', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('risk_score', sa.Numeric(precision=3, scale=2), nullable=False),
        sa.Column('detected_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fraud_patterns_customer_id'), 'fraud_patterns', ['customer_id'], unique=False)
    op.create_index(op.f('ix_fraud_patterns_pattern_type'), 'fraud_patterns', ['pattern_type'], unique=False)
    op.create_index(op.f('ix_fraud_patterns_risk_score'), 'fraud_patterns', ['risk_score'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('fraud_patterns')
    op.drop_table('fraud_alerts')
    op.drop_table('payments')
    op.drop_table('installment_plans')
    op.drop_table('installment_requests')
    op.drop_table('businesses')
    op.drop_table('users')
    
    # Drop enum types
    op.execute("DROP TYPE IF EXISTS alert_status")
    op.execute("DROP TYPE IF EXISTS alert_severity")
    op.execute("DROP TYPE IF EXISTS alert_type")
    op.execute("DROP TYPE IF EXISTS payment_status")
    op.execute("DROP TYPE IF EXISTS plan_status")
    op.execute("DROP TYPE IF EXISTS request_status")
    op.execute("DROP TYPE IF EXISTS user_role")