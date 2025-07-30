from __future__ import print_function  # Для совместимости с Python 2.7
import os
import sys
import shutil
try:
    from pathlib import Path  # Python 3.4+
except ImportError:
    # Для Python 2.7
    import os.path
    class Path:
        @staticmethod
        def home():
            return Path(os.path.expanduser("~"))
            
        def __init__(self, path):
            self.path = path
            
        def __truediv__(self, other):
            return Path(os.path.join(self.path, other))
            
        def exists(self):
            return os.path.exists(self.path)
            
        def __str__(self):
            return self.path

def main():
    """Точка входа для CLI"""
    if len(sys.argv) < 2:
        print("Использование: reactz [команда] [аргументы]")
        print("Доступные команды:")
        print("  info    - показать информацию о пакете")
        print("  install [путь] - установить файлы в указанную папку")
        print("  desktop - установить файлы на рабочий стол")
        print("  version - показать версию и информацию о сборке")
        return

    command = sys.argv[1]
    
    if command == "info":
        show_info()
    elif command == "install" and len(sys.argv) > 2:
        destination = sys.argv[2]
        install_files(destination)
    elif command == "desktop":
        install_on_desktop()
    elif command == "version":
        show_version()
    else:
        print("Неизвестная команда: {}".format(command))
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
    
    print("Файлы успешно установлены в {}".format(destination))

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
        print("Папка {} уже существует.".format(target_path))
        if sys.version_info[0] >= 3:
            overwrite = input("Перезаписать? (y/n): ").lower()
        else:
            overwrite = raw_input("Перезаписать? (y/n): ").lower()  # Python 2.x
        if overwrite != 'y':
            print("Установка отменена.")
            return
        # Удаляем существующую папку
        shutil.rmtree(target_path)
    
    # Устанавливаем файлы
    install_files(target_path)
    print("Успешно установлено на рабочий стол")

def show_info():
    """Показывает информацию о пакете"""
    import n  # Импортируем ваш пакет 'n'
    
    package_path = os.path.dirname(n.__file__)
    
    print("Информация о пакете:")
    print("Название: reactz")
    print("Версия: 0.1.3")
    print("Путь установки: {}".format(package_path))
    
    # Подсчет файлов
    php_files = 0
    other_files = 0
    
    for root, _, files in os.walk(package_path):
        for file in files:
            if file.endswith('.php'):
                php_files += 1
            elif not file.endswith('.py'):
                other_files += 1
    
    print("PHP файлов: {}".format(php_files))
    print("Других файлов: {}".format(other_files))

def show_version():
    """Показывает версию и информацию о сборке"""
    print("reactz версия 0.1.3")
    print("Дата сборки: 2025-05-19 14:50:50")
    print("Автор: katarymba")
    print("Опубликовано на PyPI")

if __name__ == "__main__":
    main()