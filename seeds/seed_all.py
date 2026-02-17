# Orquestador de seeds — Ejecutar con: python seeds/seed_all.py
# Crea contexto Flask, luego ejecuta seed_games, seed_users y seed_reviews en orden.
# Los seeds son idempotentes: se pueden re-ejecutar sin duplicar datos.
# Ver: docs/02-Estructura-y-archivos.md (sección seeds/)


def seed_all():
    # TODO: Implementar orquestador de seeds
    # 1. Crear app con create_app()
    # 2. Dentro de app.app_context():
    #    a. Ejecutar seed_games() → imprimir conteo
    #    b. Ejecutar seed_users() → imprimir conteo
    #    c. Ejecutar seed_reviews() → imprimir conteo
    # 3. Imprimir resumen total
    pass


if __name__ == '__main__':
    seed_all()
