"""
Задание 3: Создание приложения в форме как экран телефона
Простое приложение, где пользователь вводит текст, нажимает кнопку, 
и текст меняет свой шрифт на один из предопределенных вариантов.

Требуется библиотека tkinter, которая обычно входит в стандартную поставку Python.
"""

import tkinter as tk
from tkinter import font as tkfont

class PhoneApp:
    def __init__(self, root):
        # Настройка основного окна
        self.root = root
        self.root.title("Экран телефона")
        self.root.geometry("300x600")  # Размер как у телефона
        self.root.configure(bg="#f0f0f0")
        
        # Доступные шрифты
        self.fonts = [
            ("Arial", 12),
            ("Times New Roman", 12),
            ("Courier New", 12),
            ("Verdana", 12),
            ("Comic Sans MS", 12),
            ("Impact", 12)
        ]
        self.current_font_index = 0
        
        # Создаем элементы интерфейса
        self.create_widgets()
    
    def create_widgets(self):
        # Верхняя панель (статус-бар)
        self.status_bar = tk.Frame(self.root, bg="#444444", height=30)
        self.status_bar.pack(fill=tk.X)
        
        # Время в статус-баре
        time_label = tk.Label(self.status_bar, text="12:34", fg="white", bg="#444444")
        time_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Основная область экрана
        main_frame = tk.Frame(self.root, bg="#ffffff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Поле для ввода текста
        self.text_entry = tk.Text(main_frame, height=10, width=30, wrap=tk.WORD, 
                                  font=self.fonts[self.current_font_index])
        self.text_entry.pack(fill=tk.BOTH, expand=True, pady=10)
        self.text_entry.insert(tk.END, "Введите текст здесь...")
        
        # Информация о текущем шрифте
        self.font_info = tk.Label(main_frame, text=f"Шрифт: {self.fonts[self.current_font_index][0]}")
        self.font_info.pack(pady=5)
        
        # Кнопка для изменения шрифта
        change_font_button = tk.Button(main_frame, text="Изменить шрифт", 
                                       command=self.change_font, bg="#4CAF50", fg="white",
                                       relief=tk.FLAT, padx=20, pady=10)
        change_font_button.pack(pady=20)
        
        # Нижняя панель с кнопками навигации (как на телефоне)
        nav_bar = tk.Frame(self.root, bg="#444444", height=50)
        nav_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Добавляем три кнопки навигации
        for i in range(3):
            button = tk.Button(nav_bar, text=["←", "○", "□"][i], bg="#444444", fg="white",
                              relief=tk.FLAT, width=3, height=1)
            button.pack(side=tk.LEFT, expand=True, fill=tk.Y, padx=10, pady=5)
    
    def change_font(self):
        # Переключаемся на следующий шрифт
        self.current_font_index = (self.current_font_index + 1) % len(self.fonts)
        
        # Применяем новый шрифт
        font_name, font_size = self.fonts[self.current_font_index]
        new_font = tkfont.Font(family=font_name, size=font_size)
        self.text_entry.configure(font=new_font)
        
        # Обновляем информацию о шрифте
        self.font_info.config(text=f"Шрифт: {font_name}")

# Запуск приложения
def main():
    root = tk.Tk()
    app = PhoneApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 