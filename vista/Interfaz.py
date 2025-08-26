from db.Conector import SessionLocal
from helpers.prestamos import prestar_por_dni_y_codigo, devolver_por_id

session = SessionLocal()
try:
    # PRESTAR
    p = prestar_por_dni_y_codigo(session, dni="87654321", codigo_ejemplar="LIB-1-1")
    session.commit()
    session.refresh(p)
    print("Prestamo creado:", p.id)

    # DEVOLVER
    devolver_por_id(session, p.id)
    session.commit()
    print("Préstamo devuelto:", p.id)

except Exception as e:
    session.rollback()
    print("Error:", e)
finally:
    session.close()
