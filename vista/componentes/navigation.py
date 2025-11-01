def go_to_dashboard(current_window=None):
    from vista.main_dashboard import MainDashboard
    if current_window: current_window.destroy()
    MainDashboard().mainloop()

def go_to_users(current_window=None):
    from vista.users_list import UserList
    if current_window: current_window.destroy()
    UserList().mainloop()

def go_to_books(current_window=None):
    from vista.books_list import BookList
    if current_window: current_window.destroy()
    BookList().mainloop()

def go_to_loans(current_window=None):
    from vista.loan_history_list import LoanHistoryList
    if current_window: current_window.destroy()
    LoanHistoryList().mainloop()

def go_to_exit(current_window=None):
    if current_window:
        current_window.destroy()