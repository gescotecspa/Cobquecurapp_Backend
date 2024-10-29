from app import create_app

# Aquí puedes configurar el entorno o cualquier otro ajuste previo al lanzamiento
# Por ejemplo, puedes establecer variables de entorno

app = create_app()

if __name__ == '__main__':
    # Aquí puedes configurar opciones adicionales para la ejecución del servidor
    # como el puerto, el modo de depuración, etc.
    app.run(host='0.0.0.0', port=7500, debug=False)  # Cambia debug a False en un entorno de producción
