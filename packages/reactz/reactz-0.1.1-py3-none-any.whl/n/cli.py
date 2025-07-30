import os
import sys
import shutil
from pathlib import Path

def main():
    """Точка входа для CLI"""
    if len(sys.argv) < 2:
        print("Использование: reactz [команда] [аргументы]")
        print("Доступные команды:")
        print("  info    - показать информацию о пакете")
        print("  install [путь] - установить файлы в указанную папку")
        print("  desktop - установить файлы на рабочий стол")
        return

    command = sys.argv[1]
    
    if command == "info":
        show_info()
    elif command == "install" and len(sys.argv) > 2:
        destination = sys.argv[2]
        install_files(destination)
    elif command == "desktop":
        # Новая команда для установки на рабочий стол
        install_on_desktop()
    else:
        print(f"Неизвестная команда: {command}")
        print("Введите 'reactz' без аргументов для получения справки")

def install_files(destination):
    """Копирует файлы пакета в указанную папку"""
    import n  # Импортируем ваш пакет 'n'
    
    # Путь к установленному пакету
    package_path = os.path.dirname(n.__file__)
    
    if not os.path.exists(destination):
        os.makedirs(destination)
    
    # Копирование всех файлов из пакета в указанную папку
    for root, dirs, files in os.walk(package_path):
        for file in files:
            src_file = os.path.join(root, file)
            # Создаем относительный путь от package_path
            rel_path = os.path.relpath(src_file, package_path)
            dst_file = os.path.join(destination, rel_path)
            
            # Создаем папки в назначении, если их нет
            dst_dir = os.path.dirname(dst_file)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            
            # Копируем файл
            shutil.copy2(src_file, dst_file)
    
    print(f"Файлы успешно установлены в {destination}")

def install_on_desktop():
    """Установка файлов на рабочий стол пользователя"""
    # Определяем путь к рабочему столу
    desktop = Path.home() / "Desktop"
    
    # Если папка Desktop не найдена (может отличаться в разных локализациях)
    if not desktop.exists():
        desktop = Path.home() / "Рабочий стол"  # Для русской локализации
    
    if not desktop.exists():
        print("Не удалось найти папку рабочего стола. Укажите путь вручную:")
        print("reactz install [путь]")
        return
    
    # Создаем папку reactz на рабочем столе
    target_folder = desktop / "reactz"
    target_path = str(target_folder)
    
    # Проверяем, существует ли уже такая папка
    if target_folder.exists():
        print(f"Папка {target_path} уже существует.")
        overwrite = input("Перезаписать? (y/n): ").lower()
        if overwrite != 'y':
            print("Установка отменена.")
            return
        # Удаляем существующую папку
        shutil.rmtree(target_path)
    
    # Устанавливаем файлы
    install_files(target_path)
    print(f"Успешно")

def show_info():
    """Показывает информацию о пакете"""
    import n  # Импортируем ваш пакет 'n'
    
    package_path = os.path.dirname(n.__file__)
    
    print("Информация о пакете:")
    print(f"Название: reactz")
    print(f"Версия: 0.1.0")
    print(f"Путь установки: {package_path}")
    
    # Подсчет файлов
    php_files = 0
    other_files = 0
    
    for root, _, files in os.walk(package_path):
        for file in files:
            if file.endswith('.php'):
                php_files += 1
            elif not file.endswith('.py'):
                other_files += 1
    
    print(f"PHP файлов: {php_files}")
    print(f"Других файлов: {other_files}")

if __name__ == "__main__":
    main()