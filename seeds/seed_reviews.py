# Seed de reseñas — Genera ~50-80 reseñas variadas entre usuarios demo y juegos populares.
# Ratings con distribución realista (más 3s y 4s). Textos de un array predefinido.
# Fechas repartidas en los últimos 30 días. Respeta constraint unique (user_id, game_id).
# Ver: docs/02-Estructura-y-archivos.md (sección seeds/seed_reviews.py)

# Frases variadas para reseñas de ejemplo
REVIEW_TEXTS = [
    'Gran juego para pasar el rato, lo recomiendo.',
    'Los gráficos podrían mejorar pero el gameplay es sólido.',
    'Demasiado pay-to-win para mi gusto.',
    'Lo recomiendo al 100%, llevo más de 200 horas.',
    'Está bien para ser gratuito, nada del otro mundo.',
    'Me enganchó desde el primer momento, no puedo parar de jugar.',
    'La comunidad es muy tóxica, pero el juego en sí está genial.',
    'Buen juego casual para jugar en ratos libres.',
    'El mejor free-to-play que he probado este año.',
    'Se nota que los desarrolladores se esfuerzan con las actualizaciones.',
    'Bastante repetitivo después de unas horas.',
    'La historia es sorprendentemente buena para un juego gratuito.',
    'Perfecto para jugar con amigos, en solitario aburre un poco.',
    'Los controles son fluidos y el rendimiento es excelente.',
    'Necesita más contenido pero tiene una base muy sólida.',
    'Me sorprendió gratamente, no esperaba tanto de un F2P.',
    'Regular, hay opciones mejores en el mismo género.',
    'Adictivo y divertido, ideal para sesiones cortas.',
    'El sistema de progresión está bien diseñado.',
    'Buena propuesta, aunque le faltan modos de juego.',
]

# Distribución de ratings (más 3s y 4s, menos 1s y 5s)
RATING_WEIGHTS = [1, 2, 3, 3, 2]  # pesos para ratings 1, 2, 3, 4, 5


def seed_reviews():
    """Genera reseñas de ejemplo. Retorna el número de reseñas creadas."""
    # TODO: Implementar seed de reseñas
    # 1. Obtener usuarios demo (no admin)
    # 2. Seleccionar 20-30 juegos de la BD
    # 3. Por cada usuario, asignar 8-15 juegos aleatorios
    # 4. Crear Review con rating (distribución realista con RATING_WEIGHTS),
    #    texto (aleatorio de REVIEW_TEXTS),
    #    fecha (aleatoria en los últimos 30 días)
    # 5. Respetar constraint unique (user_id, game_id)
    # 6. db.session.commit()
    # 7. Retornar conteo
    pass
