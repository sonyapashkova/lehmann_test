import os
import tkinter as tk
import tkinter.messagebox as mb
from lehmann import PRIME_NUMBER, PRIME_NUMBER_ERROR


def print_error(error):
    """ Выводит описание ошибки """
    mb.showerror("Ошибка", error)


def print_result(text_number: tk.Text, label_count_iter: tk.Label, label_time: tk.Label):
    """ Выводит результаты операции генерации простого числа """
    file_result = "result.txt"
    with open(file_result, "r", encoding="utf-8") as file_in:
        number = int(file_in.readline().rstrip())
        count_iter = int(file_in.readline().rstrip())
        time = float(file_in.readline().rstrip())
    text_number.delete(1.0, tk.END)
    text_number.insert(1.0, str(number))
    label_count_iter["text"] = "Количество итераций: " + str(count_iter)
    label_time["text"] = "Время: " + str(time) + " c."
    msg = f"Результаты генератора сохранены в файл: {file_result}. Открыть файл {file_result}?"
    if mb.askyesno("Открыть файл", msg):
        os.startfile(file_result)


def generate_prime_number(text_number: tk.Text, label_count_iter: tk.Label, label_time: tk.Label):
    """ Обрабатывает кнопку генерации простого числа """
    try:
        G = PRIME_NUMBER("attrs.txt")
        G.generate()
        print_result(text_number, label_count_iter, label_time)
    except PRIME_NUMBER_ERROR as prime_number_err:
        print_error(prime_number_err)


def change_file_attrs():
    """ Обрабатывает кнопку для изменения файла с параметрами для генератора простых чисел"""
    file_attrs = "attrs.txt"
    msg = f"Изменить файл {file_attrs} с параметрами для генератора простых чисел?"
    if mb.askyesno("Открыть файл", msg):
        os.startfile(file_attrs)
    

def  create_app():
    """ Создает окно приложения """
    root = tk.Tk()
    root.title("Генерирование РРСП")
    root.geometry("400x210+200+100")
    root.resizable(False, False)
   
    label_number = tk.Label(text="Простое число: ", font=("Arial", 10))
    label_number.grid(row=0, column=0, stick="w", padx=20, pady=10)
    text_number = tk.Text(width=50, height=1, font=("Arial", 10), wrap="char")
    text_number.grid(row=1, column=0, stick="w", padx=20)
    label_count_iter = tk.Label(text="Количество итераций: ", font="Arial 10 italic")
    label_count_iter.grid(row=2, column=0, stick="w", padx=20, pady=10)
    label_time = tk.Label(text="Время: ", font="Arial 10 italic")
    label_time.grid(row=3, column=0, stick="w", padx=20)
    button_generate = tk.Button(text="Сгенерировать", width=20, font=("Arial", 10), activebackground="#00CED1", background="#FFFFFF",
                                command=lambda: generate_prime_number(text_number, label_count_iter, label_time))
    button_generate.grid(row=4, column=0, stick="we", padx=20, pady=5)
    button_change_attrs = tk.Button(text="Изменить параметры", width=20, font=("Arial", 10), activebackground="#00CED1", background="#FFFFFF", 
                                    command=lambda: change_file_attrs())
    button_change_attrs.grid(row=5, column=0, stick="we", padx=20, pady=5)
    
    root.mainloop()