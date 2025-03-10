# conn_guide
Тест соединений к разным БД



#### Ветка `docker`

В ветке находятся:

1. `src/app.py` - пример приложения
2. `Dockerfile`
3. `requirements.txt` - необходимый файл для скачивания нужных библиотек

`Dockerfile` представлен следующим образом:

```
FROM python:3.12
WORKDIR /usr/local/app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY src ./src
EXPOSE 5000

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

# Command to run the application
CMD ["python", "src/app.py"]
```

Разберем Dockerfile пошагово, описывая каждую команду и соответствующий ей слой:

### **1. `FROM python:3.12`**
**Слой**: Использует базовый образ Python 3.12, он становится основой для всех последующих инструкций

### **2. `WORKDIR /usr/local/app`**
**Слой**: Устанавливает рабочую директорию внутри контейнера в `/usr/local/app`.

### **3. `COPY requirements.txt ./`**
**Слой**: Копирует файл зависимостей `requirements.txt` в рабочую директорию контейнера (`/usr/local/app`).

### **4. `RUN pip install --no-cache-dir -r requirements.txt`**
**Слой**: Устанавливает зависимости из `requirements.txt` через `pip`, флаг `--no-cache-dir` отключает сохранение кэша.

### **5. `COPY src ./src`**
**Слой**: Копирует исходный код из директории `src` в директорию  `/usr/local/app/src` внутри контейнера.

### **6. `EXPOSE 5000`**
**Слой**: Метаданные о порте, указывает, что контейнер слушает порт `5000`.

**Важно**: Это не открывает порт на хосте! Информация используется для:
 - Документации (порт виден через `docker inspect`).
 - Автоматической проброски портов при использовании `docker run -P`.

---

### **7. `RUN useradd app`**
- **Слой**: Создает пользователя.
- **Что делает**:
  - Создает нового системного пользователя `app` внутри контейнера.
  - Это повышает безопасность, чтобы приложение не работало от имени `root`.

---

### **8. `USER app`**
- **Слой**: устанавливает пользователя `app` как текущего для всех последующих команд.

### **9. `CMD ["python", "src/app.py"]`**
- **Слой**: Команда по умолчанию (задает команду при запуске контейнера `python src/app.py`).


### **Пример команды для сборки и запуска**
```bash
# Сборка образа
docker build -t my-app .

# Запуск контейнера с пробросом порта
docker run -p 5000:5000 my-app
```

---

### **Проверка информации о слоях**
Чтобы посмотреть слои образа:
```bash
docker history my-app
```
Вы увидите все слои, их размер и соответствующие команды из Dockerfile.
