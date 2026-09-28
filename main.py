from fastapi import FastAPI, UploadFile, Form, HTTPException # type: ignore
from fastapi.responses import FileResponse # type: ignore
import tempfile
import os
import sys
import uvicorn # type: ignore
from fastapi.responses import HTMLResponse # type: ignore

print("=== Запуск сервера ===")
print(f"Текущая директория: {os.getcwd()}")

# Добавляем путь к папке с модулем в sys.path
module_dir = os.getcwd()
if module_dir not in sys.path:
    sys.path.insert(0, module_dir)
    print(f"Добавлен путь: {module_dir}")

# Импортируем модуль напрямую
try:
    import papina_shtuka3obolochka as script
    print("✓ Модуль успешно импортирован")
    print(f"  Функции в модуле: {dir(script)}")
except Exception as e:
    print(f"✗ Ошибка импорта: {e}")
    script = None

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Обработчик файлов</title>
        </head>
        <body>
            <h2>Обработка файла</h2>
            <form action="/process" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required><br><br>
                <select name="option">
                    <option value="type1">Teleon</option>
                    <option value="type2">Hoya</option>
                </select><br><br>
                <button type="submit">Отправить</button>
            </form>
        </body>
    </html>
    """

@app.post("/process")
async def process_file(
    file: UploadFile,
    option: str = Form(...)
):
    print(f"\n✓ Получен файл: {file.filename}")
    print(f"✓ Опция: {option}")
    
    if script is None:
        raise HTTPException(500, "Модуль обработки не загружен")
    
    # Сохраняем входной файл во временный
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp_in:
        content = await file.read()
        tmp_in.write(content)
        input_path = tmp_in.name
        print(f"✓ Файл сохранен: {input_path}, размер: {len(content)} байт")

    try:
        # Вызываем твой скрипт
        print("✓ Запуск обработки...")
        output_path = script.process_file(input_path, option, file.filename)
        print(f"✓ Результат: {output_path}")
        
        # Возвращаем файл пользователю
        filename = os.path.basename(output_path)
        return FileResponse(
            output_path,
            media_type="application/octet-stream",
            filename=filename
        )
    except Exception as e:
        print(f"✗ Ошибка обработки: {e}")
        raise HTTPException(500, f"Ошибка обработки: {str(e)}")

if __name__ == "__main__":
    print("\n=== Запуск сервера на http://127.0.0.1:8000 ===")
    uvicorn.run(app, host="127.0.0.1", port=8000)