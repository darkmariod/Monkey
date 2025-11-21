from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os, json, base64

TZ = ZoneInfo("America/Guayaquil")

class GoogleService:
    def __init__(self):
        creds = None
        last_error = None

        # 🔹 CREDENCIALES: Render → Base64
        b64_env = os.getenv("GOOGLE_CREDENTIALS_B64")

        if b64_env:
            try:
                decoded = base64.b64decode(b64_env)
                info = json.loads(decoded)
                creds = service_account.Credentials.from_service_account_info(
                    info, scopes=["https://www.googleapis.com/auth/calendar"]
                )
            except Exception as e:
                last_error = f"Error en GOOGLE_CREDENTIALS_B64 → {e}"

        # 🔹 Local → credentials.json
        elif os.path.exists("credentials.json"):
            try:
                creds = service_account.Credentials.from_service_account_file(
                    "credentials.json",
                    scopes=["https://www.googleapis.com/auth/calendar"]
                )
            except Exception as e:
                last_error = f"Error leyendo credentials.json → {e}"

        if not creds:
            raise RuntimeError(f"No se pudieron cargar las credenciales. {last_error}")

        self.service = build("calendar", "v3", credentials=creds, cache_discovery=False)

    # 🔹 OBTENER HORAS DISPONIBLES POR SEDE
    def get_free_slots(self, calendar_id: str, date: str, duration_minutes: int = 45):
        try:
            date_start = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=TZ)
            date_end = date_start + timedelta(days=1)

            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=date_start.isoformat(),
                timeMax=date_end.isoformat(),
                singleEvents=True,
                orderBy="startTime"
            ).execute()

            events = events_result.get("items", [])

            # Convertir busy slots
            busy = []
            for ev in events:
                s = ev["start"].get("dateTime")
                e = ev["end"].get("dateTime")
                if s and e:
                    busy.append((datetime.fromisoformat(s), datetime.fromisoformat(e)))

            # Horario de atención
            open_hour = 9
            close_hour = 20
            slots = []
            start_time = date_start.replace(hour=open_hour, minute=0)

            while start_time.hour < close_hour:
                end_time = start_time + timedelta(minutes=duration_minutes)

                # ❌ Evitar solapamiento
                overlap = False
                for s, e in busy:
                    if not (end_time <= s or start_time >= e):
                        overlap = True
                        break

                if not overlap:
                    slots.append(start_time.strftime("%H:%M"))

                start_time = end_time

            return slots

        except Exception as e:
            print("❌ Error generando slots:", e)
            return []

    # 🔹 CREAR EVENTO FINAL (RESERVA)
    def crear_evento(self, calendar_id, resumen, descripcion, inicio, fin, zona="America/Guayaquil"):
        try:
            # Validar doble reserva exacta
            existing = self.service.events().list(
                calendarId=calendar_id,
                timeMin=inicio.isoformat(),
                timeMax=fin.isoformat(),
                singleEvents=True,
            ).execute().get("items", [])

            if existing:
                raise RuntimeError("Ese horario ya está reservado.")

            evento = {
                "summary": resumen,
                "description": descripcion,
                "start": {"dateTime": inicio.isoformat(), "timeZone": zona},
                "end": {"dateTime": fin.isoformat(), "timeZone": zona},
            }

            self.service.events().insert(calendarId=calendar_id, body=evento).execute()
            print("✅ Evento creado correctamente")

        except Exception as e:
            print("❌ Error creando evento:", e)
            raise e
