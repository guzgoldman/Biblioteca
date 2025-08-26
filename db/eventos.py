from sqlalchemy import event, inspect
from sqlalchemy.orm import Session
from modelo import Prestamo, Historial

@event.listens_for(Session, "after_flush")
def audit_prestamos(session: Session, flush_context):
    # Nuevos préstamos → PRESTAR
    for obj in session.new:
        if isinstance(obj, Prestamo):
            session.add(Historial(
                accion="PRESTAR",
                prestamo_id=obj.id,
                ejemplar_id=obj.ejemplar_id,
                usuario_id=obj.usuario_id,
                detalle=f"Prestamo {obj.id} creado"
            ))
    # Cambios en préstamos → DEVOLVER (solo si cambió fecha_devolucion a no-NULL)
    for obj in session.dirty:
        if isinstance(obj, Prestamo):
            hist = inspect(obj).attrs.fecha_devolucion.history
            if hist.has_changes() and obj.fecha_devolucion is not None:
                session.add(Historial(
                    accion="DEVOLVER",
                    prestamo_id=obj.id,
                    ejemplar_id=obj.ejemplar_id,
                    usuario_id=obj.usuario_id,
                    detalle=f"Prestamo {obj.id} devuelto"
                ))
