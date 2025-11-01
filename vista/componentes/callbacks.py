def get_default_callbacks(app):
    """Callbacks de navegación comunes."""
    from .navigation import go_to_dashboard, go_to_users, go_to_books, go_to_loans, go_to_exit
    return {
        "Escritorio": lambda: go_to_dashboard(app),
        "Socios": lambda: go_to_users(app),
        "Libros": lambda: go_to_books(app),
        "Préstamos": lambda: go_to_loans(app),
        "Salir": lambda: go_to_exit(app),
    }