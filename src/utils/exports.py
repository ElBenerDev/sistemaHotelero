import csv
from io import StringIO
from flask import make_response
from datetime import datetime

def export_reservations_csv(reservations):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Habitación', 'Huésped', 'Check-in', 'Check-out', 'Estado', 'Precio Total'])
    
    for reservation in reservations:
        writer.writerow([
            reservation.id,
            reservation.room.number,
            reservation.guest.full_name,
            reservation.check_in.strftime('%Y-%m-%d %H:%M'),
            reservation.check_out.strftime('%Y-%m-%d %H:%M'),
            reservation.status.value,
            f"${reservation.total_price:.2f}"
        ])
    
    output.seek(0)
    return output.getvalue()