#!/usr/bin/env python3
import os
import sys
import shutil

def main():
    """
    Основная функция, которая запускается при вызове команды 'reactz'
    """
    if len(sys.argv) < 2:
        print("Использование: reactz [действие] [опции]")
        print("Доступные действия:")
        print("  install [путь] - копировать файлы в указанную папку")
        print("  info            - показать информацию о пакете")
        return

    action = sys.argv[1]
    
    if action == "install":
        if len(sys.argv) < 3:
            print("Пожалуйста, укажите путь для установки")
            return
        
        destination = sys.argv[2]
        install_files(destination)
    
    elif action == "info":
        show_info()
    
    else:
        print(f"Неизвестное действие: {action}")
        print("Доступные действия: install, info")

def install_files(destination):
    """Копирует файлы пакета в указанную папку"""
    import n
    
    # Путь к установленному пакету
    package_path = os.path.dirname(n.__file__)
    
    # Проверяем существование папки назначения
    if not os.path.exists(destination):
        os.makedirs(destination)
    
    print(f"Копирование файлов из {package_path} в {destination}")
    
    # Копируем содержимое пакета в указанную папку
    for item in os.listdir(package_path):
        source_item = os.path.join(package_path, item)
        dest_item = os.path.join(destination, item)
        
        if os.path.isdir(source_item):
            if os.path.exists(dest_item):
                shutil.rmtree(dest_item)
            shutil.copytree(source_item, dest_item)
        else:
            if item.endswith('.py'):  # Пропускаем Python файлы
                continue
            shutil.copy2(source_item, dest_item)
    
    print("Установка завершена!")

def show_info():
    """Показывает информацию о пакете"""
    import n
    
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