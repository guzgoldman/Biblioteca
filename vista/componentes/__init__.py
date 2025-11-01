# vistas/componentes/__init__.py
from tkinter import ttk
from .base_app import BaseApp
from .layout import AppLayout
from .table import Table
from .callbacks import get_default_callbacks
from .dashboard_cards import DashboardCards

# Reexportamos navegación
from .navigation import (
    go_to_dashboard,
    go_to_users,
    go_to_books,
    go_to_loans,
    go_to_exit,
)

__all__ = [
    "BaseApp",
    "AppLayout",
    "Table",
    "DashboardCards",
    "get_default_callbacks",
    "go_to_dashboard",
    "go_to_users",
    "go_to_books",
    "go_to_loans",
    "go_to_exit",
]
