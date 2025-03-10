from app import app

if __name__ == '__main__':
    # Запуск приложения на хосте 0.0.0.0 и порту 5000
    app.run(host='0.0.0.0', port=5000)