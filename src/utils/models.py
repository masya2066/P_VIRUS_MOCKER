def model_to_dict(model_instance):
    """Convert SQLAlchemy model instance to dictionary."""
    return {column.name: getattr(model_instance, column.name) for column in model_instance.__table__.columns}
