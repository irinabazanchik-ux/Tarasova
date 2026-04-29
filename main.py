import tkinter as tk
from tkinter import ttk, messagebox
import json

BOOKS_FILE = 'books.json'

def load_data():
    try:
        with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_book():
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    genre = entry_genre.get().strip()
    pages = entry_pages.get().strip()

    # Проверка на пустые поля
    if not (title and author and genre and pages):
        messagebox.showwarning("Ошибка", "Все поля должны быть заполнены!")
        return

    # Проверка, что страницы — это число
    if not pages.isdigit():
        messagebox.showwarning("Ошибка", "Количество страниц должно быть числом!")
        return

    new_book = {
        "title": title,
        "author": author,
        "genre": genre,
        "pages": int(pages)
    }

    books.append(new_book)
    save_data(books)
    refresh_list(books)
    
    # Очистка полей
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_pages.delete(0, tk.END)

def refresh_list(data_to_display):
    # Очистка таблицы
    for item in tree.get_children():
        tree.delete(item)
    # Заполнение
    for book in data_to_display:
        tree.insert('', tk.END, values=(book['title'], book['author'], book['genre'], book['pages']))

def apply_filter():
    genre_filter = entry_filter_genre.get().strip().lower()
    try:
        min_pages = int(entry_filter_pages.get().strip() or 0)
    except ValueError:
        min_pages = 0

    filtered = [
        b for b in books 
        if (not genre_filter or genre_filter in b['genre'].lower()) and 
           (b['pages'] >= min_pages)
    ]
    refresh_list(filtered)

books = load_data()

root = tk.Tk()
root.title("Book Tracker")
root.geometry("700x500")

# --- Форма ввода ---
frame_input = ttk.LabelFrame(root, text="Добавить новую книгу")
frame_input.pack(padx=10, pady=10, fill='x')

labels = ["Название:", "Автор:", "Жанр:", "Страниц:"]
entries = []

for i, text in enumerate(labels):
    ttk.Label(frame_input, text=text).grid(row=0, column=i*2, padx=5, pady=5)
    entry = ttk.Entry(frame_input, width=15)
    entry.grid(row=0, column=i*2+1, padx=5, pady=5)
    entries.append(entry)

entry_title, entry_author, entry_genre, entry_pages = entries

btn_add = ttk.Button(frame_input, text="Добавить", command=add_book)
btn_add.grid(row=1, column=0, columnspan=8, pady=10)

# --- Блок фильтрации ---
frame_filter = ttk.LabelFrame(root, text="Фильтрация")
frame_filter.pack(padx=10, pady=5, fill='x')

ttk.Label(frame_filter, text="Жанр:").grid(row=0, column=0, padx=5)
entry_filter_genre = ttk.Entry(frame_filter)
entry_filter_genre.grid(row=0, column=1, padx=5)

ttk.Label(frame_filter, text="Мин. страниц:").grid(row=0, column=2, padx=5)
entry_filter_pages = ttk.Entry(frame_filter)
entry_filter_pages.grid(row=0, column=3, padx=5)

btn_filter = ttk.Button(frame_filter, text="Применить", command=apply_filter)
btn_filter.grid(row=0, column=4, padx=10)

btn_reset = ttk.Button(frame_filter, text="Сброс", command=lambda: refresh_list(books))
btn_reset.grid(row=0, column=5, padx=5)

# --- Таблица вывода ---
columns = ('title', 'author', 'genre', 'pages')
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading('title', text='Название')
tree.heading('author', text='Автор')
tree.heading('genre', text='Жанр')
tree.heading('pages', text='Стр.')

tree.column('pages', width=50)
tree.pack(padx=10, pady=10, fill='both', expand=True)

refresh_list(books)
root.mainloop()