from datetime import datetime

def is_valid_appointment_time(dt: datetime) -> tuple[bool, str]:
    weekday = dt.weekday()  # 0=lunes … 6=domingo
    hour = dt.hour + dt.minute/60

    # Domingo cerrado
    if weekday == 6:
        return False, "Los domingos la clínica está cerrada."

    # Lunes–Viernes
    if weekday < 5:
        if 9 <= hour <= 20:
            return True, ""
        return False, "El horario entre semana es de 9:00 a 20:00."

    # Sábado
    if weekday == 5:
        if 10 <= hour <= 14:
            return True, ""
        return False, "El horario del sábado es de 10:00 a 14:00."
