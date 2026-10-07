from datetime import datetime, timezone

LIMITE_HORAS = 24


def analizar_publicaciones(publicaciones, nombre_usuario):

    publicaciones = sorted(
        publicaciones,
        key=lambda p: p["fecha"] or datetime.min.replace(tzinfo=timezone.utc)
    )

    ahora = datetime.now(timezone.utc).astimezone()

    resultado = []

    tiempos_respuesta = []

    pendientes = 0

    vencidas = 0

    for post in publicaciones:

        # Solo analizar publicaciones de estudiantes
        if post["es_mio"]:
            continue

        respondido = False
        tiempo_respuesta = None
        fecha_respuesta = None
        respondio = ""

        autor_post = post["autor"].strip().upper()

        # Buscar cualquier respuesta del tutor posterior
        for siguiente in publicaciones:

            if not siguiente["es_mio"]:
                continue

            if (
                post["fecha"] is not None and
                siguiente["fecha"] is not None and
                siguiente["fecha"] <= post["fecha"]
            ):
                continue

            respuesta = (
                siguiente.get("respuesta_a") or ""
            ).strip().upper()

            if autor_post == respuesta:

                respondido = True

                respondio = siguiente["autor"]

                fecha_respuesta = siguiente["fecha"]

                if (
                    post["fecha"] is not None and
                    siguiente["fecha"] is not None
                ):

                    tiempo = (
                        siguiente["fecha"] -
                        post["fecha"]
                    )

                    tiempo_respuesta = round(
                        tiempo.total_seconds() / 3600,
                        2
                    )

                    tiempos_respuesta.append(
                        tiempo_respuesta
                    )

                break

        horas_transcurridas = None

        if post["fecha"] is not None:

            horas_transcurridas = round(
                (
                    ahora -
                    post["fecha"]
                ).total_seconds() / 3600,
                2
            )

        requiere = not respondido

        vencido = False

        prioridad = "OK"

        motivo = ""

        if requiere:

            pendientes += 1

            if horas_transcurridas is not None:

                if horas_transcurridas >= LIMITE_HORAS:

                    vencido = True
                    vencidas += 1
                    prioridad = "ALTA"
                    motivo = "Sin responder - vencida"

                elif horas_transcurridas >= 18:

                    prioridad = "MEDIA"
                    motivo = "Sin responder"

                else:

                    prioridad = "BAJA"
                    motivo = "Sin responder"

        else:

            motivo = "Respondida"

        resultado.append({

            "id": post["id"],

            "autor": post["autor"],

            "fecha": post["fecha"],

            "asunto": post["asunto"],

            "contenido": post["contenido"],

            "respuesta_a": post["respuesta_a"],

            "respondido": respondido,

            "respondio": respondio,

            "fecha_respuesta": fecha_respuesta,

            "requiere_respuesta": requiere,

            "horas_transcurridas": horas_transcurridas,

            "tiempo_respuesta": tiempo_respuesta,

            "vencido": vencido,

            "prioridad": prioridad,

            "motivo": motivo

        })

    promedio = 0

    if tiempos_respuesta:

        promedio = round(
            sum(tiempos_respuesta) /
            len(tiempos_respuesta),
            2
        )

    return {

        "publicaciones": resultado,

        "total_publicaciones": len(resultado),

        "pendientes": pendientes,

        "vencidas": vencidas,

        "promedio_respuesta": promedio

    }