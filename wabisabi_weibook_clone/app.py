
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# SEDES

BRANCHES = [
    {
        "id": 0,
        "key": "Matriz",
        "name": "Wabi Sabi Barber - Matriz",
        "address": "Cra 7ma con Calle 48 · Ciudad",
        "rating": 5.0,
        "reviews": 120,
        "type": "Barbería",
        "hero_text": "Foto de la sede Wabi Sabi Barber - Matriz",
    },
    {
        "id": 1,
        "key": "Centro",
        "name": "Wabi Sabi Barber - Centro",
        "address": "Centro Histórico · Ciudad",
        "rating": 4.8,
        "reviews": 103,
        "type": "Barbería",
        "hero_text": "Foto de la sede Wabi Sabi Barber - Centro",
    },
    {
        "id": 2,
        "key": "Veloz",
        "name": "Wabi Sabi Barber - Veloz",
        "address": "Av Veloz · Ciudad",
        "rating": 5.0,
        "reviews": 87,
        "type": "Barbería",
        "hero_text": "Foto de la sede Wabi Sabi Barber - Veloz",
    },
    {
        "id": 3,
        "key": "Training",
        "name": "Wabi Sabi Barber - Training",
        "address": "Centro Histórico · Ciudad",
        "rating": 4.8,
        "reviews": 103,
        "type": "Barbería",
        "hero_text": "Foto de la sede Wabi Sabi Barber - Training",
    },
    {
        "id": 4,
        "key": "Urban",
        "name": "Wabi Sabi Barber - Urban",
        "address": "Av Urban · Ciudad",
        "rating": 4.8,
        "reviews": 103,
        "type": "Barbería",
        "hero_text": "Foto de la sede Wabi Sabi Barber - Urban",
    },
]

# BARBEROS POR SEDE

BARBEROS_POR_SEDE = {
    "Matriz": [
        {"id": "carlos", "nombre": "Carlos", "foto": "static/img/Carlos_SedeMatriz.jpg"},
        {"id": "jose", "nombre": "José", "foto": "static/img/Jose_SedeMatriz.jpg"},
        {"id": "josue", "nombre": "Josue", "foto": "static/img/Josue_SedeMatriz.jpg"},
        {"id": "santiago", "nombre": "Santiago", "foto": "static/img/Santiago_SedeMatriz.jpg"},
        {"id": "wilson", "nombre": "Wilson", "foto": "static/img/Wilson_SedeMatriz.jpg"},
    ],
    "Centro": [
        {"id": "dani", "nombre": "Dani", "foto": "static/img/barber-dani.jpg"},
        {"id": "donluis", "nombre": "Don Luis", "foto": "static/img/barber-don-luis.jpg"},
    ],
    "Urban": [
        {"id": "anthony", "nombre": "Anthony", "foto": "static/img/Anthony_SedeUrban.jpg"},
        {"id": "israel", "nombre": "Israel", "foto": "static/img/barber-isra.jpg"},
    ],
    "Veloz": [
        {"id": "fabian", "nombre": "Fabián", "foto": "static/img/Fabian_SedeVeloz.jpg"},
        {"id": "kevin", "nombre": "Kevin", "foto": "static/img/Kevin_SedeVeloz.jpg"},
        {"id": "marcos", "nombre": "Marcos", "foto": "static/img/Marcos_SedeVeloz.jpg"},
        {"id": "joseveloz", "nombre": "José", "foto": "static/img/barber-jose.jpg"},
    ],
    "Training": [],
}

# SERVICIOS

SERVICIOS = [
    {
        "id": 0,
        "nombre": "Corte de Cabello Clásico",
        "precio": 7,
        "duracion": 40,
        "descripcion": "Incluye: diagnóstico, corte a máquina/tijera y estilizado final.",
    },
    {
        "id": 1,
        "nombre": "Corte Tendencia: Fade o Degradado",
        "precio": 8,
        "duracion": 45,
        "descripcion": "Degradado premium + asesoramiento de estilizado.",
    },
    {
        "id": 2,
        "nombre": "Arreglo y Perfilado de Barba",
        "precio": 5,
        "duracion": 30,
        "descripcion": "Barba + navaja + humectación.",
    },
    {
        "id": 3,
        "nombre": "Corte de Cabello y Barba",
        "precio": 12,
        "duracion": 60,
        "descripcion": "Corte + arreglo de barba con toalla caliente.",
    },
    {
        "id": 4,
        "nombre": "Barba SPA (Ritual tradicional)",
        "precio": 8,
        "duracion": 45,
        "descripcion": "Vapor + navaja + tónico.",
    },
    {
        "id": 5,
        "nombre": "Servicio VIP Completo",
        "precio": 20,
        "duracion": 120,
        "descripcion": "Corte + barba + lavado + masaje + mascarilla.",
    },
]


def get_branch_by_id(branch_id: int):
    for b in BRANCHES:
        if b["id"] == branch_id:
            return b
    return BRANCHES[0]


def get_service_by_id(service_id: int):
    for s in SERVICIOS:
        if s["id"] == service_id:
            return s
    return None


# RUTAS

@app.route("/")
def home():
    # Home simple: redirigimos a la Matriz
    return redirect(url_for("branch", branch_id=0))


@app.route("/branch/<int:branch_id>")
def branch(branch_id: int):
    branch = get_branch_by_id(branch_id)
    return render_template("branch.html", branch=branch, branches=BRANCHES)


@app.route("/services")
def services():
    branch_id = request.args.get("branch_id", type=int)
    if branch_id is None:
        return redirect(url_for("branch", branch_id=0))

    branch = get_branch_by_id(branch_id)

    return render_template(
        "services.html",
        services=SERVICIOS,
        branch=branch,
        branch_id=branch_id,
    )


@app.route("/barbers")
def barbers():
    branch_key = request.args.get("branch")
    service_id = request.args.get("service_id", type=int)

    if branch_key not in BARBEROS_POR_SEDE:
        return "Sede inválida", 404

    barberos = BARBEROS_POR_SEDE[branch_key]
    servicio = get_service_by_id(service_id)

    return render_template(
        "barbers.html",
        barberos=barberos,
        branch_key=branch_key,
        servicio=servicio,
    )


@app.route("/booking")
def booking():
    barber_id = request.args.get("barber_id")
    service_id = request.args.get("service_id", type=int)
    branch_key = request.args.get("branch")

    # Buscar nombres legibles
    barber_name = barber_id
    for b in BARBEROS_POR_SEDE.get(branch_key, []):
        if b["id"] == barber_id:
            barber_name = b["nombre"]
            break

    servicio = get_service_by_id(service_id)

    return render_template(
        "booking.html",
        barber_id=barber_id,
        barber_name=barber_name,
        service_id=service_id,
        servicio=servicio,
        branch_key=branch_key,
    )


@app.route("/success")
def success():
    name = request.args.get("name", "")
    phone = request.args.get("phone", "")
    notes = request.args.get("notes", "")
    date = request.args.get("date", "")
    time = request.args.get("time", "")
    barber = request.args.get("barber", "")
    service = request.args.get("service", "")
    branch = request.args.get("branch", "")

    return render_template(
        "success.html",
        name=name,
        phone=phone,
        notes=notes,
        date=date,
        time=time,
        barber=barber,
        service=service,
        branch=branch,
    )


if __name__ == "__main__":
    app.run(debug=True)
