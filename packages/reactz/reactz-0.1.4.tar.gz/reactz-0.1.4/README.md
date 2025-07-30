# reactz

PHP проект, упакованный как Python-библиотека с инструментами командной строки.

## Установка

```bash
pip install reactz

Поддерживаемые версии Python
Пакет поддерживает:

Python 2.7
Python 3.x (все версии)
Команды
После установки доступны следующие команды:

Показать справку
bash
reactz
Показать информацию о пакете
bash
reactz info
Показать версию и информацию о сборке
bash
reactz version
Установить файлы в указанную директорию
bash
reactz install /путь/к/папке
Установить файлы на рабочий стол
bash
reactz desktop
Информация о версии
Версия: 0.1.3
Дата сборки: 2025-05-19 14:53:42
Автор: katarymba
Примеры использования
Быстрая установка на рабочий стол
bash
pip install reactz
reactz desktop
Проверка информации о пакете
bash
reactz info
Установка в веб-директорию (для веб-серверов)
bash
# Для Apache/XAMPP
reactz install C:\xampp\htdocs\my-reactz-app

# Для Nginx
reactz install /var/www/html/my-reactz-app