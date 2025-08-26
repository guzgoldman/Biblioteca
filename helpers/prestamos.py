from sqlalchemy import select
from sqlalchemy.orm import Session
from db.Conector import SessionLocal
from modelo import Prestamo, Usuario, Ejemplar

def prestar_por_dni_y_codigo(session: Session, dni: str, codigo_ejemplar: str) -> Prestamo:
    """Crea un préstamo para el ejemplar (por código) a un usuario (por DNI)."""
    dni = (dni or "").strip()
    codigo_ejemplar = (codigo_ejemplar or "").strip()

    if not dni or not codigo_ejemplar:
        raise ValueError("DNI y código de ejemplar son obligatorios")

    # Traer datos
    usuario = session.execute(select(Usuario).where(Usuario.dni == dni)).scalar_one_or_none()
    if not usuario:
        raise ValueError(f"Usuario con DNI {dni} no existe")

    ejemplar = session.execute(select(Ejemplar).where(Ejemplar.codigo == codigo_ejemplar)).scalar_one_or_none()
    if not ejemplar:
        raise ValueError(f"Ejemplar con código {codigo_ejemplar} no existe")

    # (Opcional) Bloquear fila del ejemplar para evitar carreras
    session.execute(select(Ejemplar).where(Ejemplar.id == ejemplar.id).with_for_update())

    # Validar que no haya préstamo activo de ese ejemplar
    prestamo_activo = session.execute(
        select(Prestamo).where(Prestamo.ejemplar_id == ejemplar.id, Prestamo.fecha_devolucion.is_(None))
    ).scalar_one_or_none()
    if prestamo_activo:
        raise ValueError("Ya existe un préstamo activo para ese ejemplar")

    # Crear usando el método del modelo
    prestamo = Prestamo.crear(session, ejemplar, usuario)
    return prestamo


def devolver_por_id(session: Session, id_prestamo: int) -> Prestamo:
    """Devuelve un préstamo por id y libera el ejemplar."""
    prestamo = session.get(Prestamo, id_prestamo)
    if not prestamo:
        raise ValueError("Préstamo no encontrado")

    prestamo.devolver(session)
    return prestamo
