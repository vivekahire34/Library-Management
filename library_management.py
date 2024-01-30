import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database setup
conn = sqlite3.connect('library.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        year INTEGER
    )
''')
conn.commit()

# GUI functions
def add_book():
    title = entry_title.get()
    author = entry_author.get()
    year = entry_year.get()

    if title and author and year:
        cursor.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)', (title, author, year))
        conn.commit()
        messagebox.showinfo('Success', 'Book added successfully!')
        clear_entries()
        display_books()
    else:
        messagebox.showerror('Error', 'Please fill in all fields.')

def display_books():
    listbox.delete(0, tk.END)
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    for book in books:
        listbox.insert(tk.END, f"{book[1]} by {book[2]} ({book[3]})")

def clear_entries():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_year.delete(0, tk.END)

def delete_book():
    selected_index = listbox.curselection()
    if selected_index:
        book_id = cursor.execute('SELECT id FROM books').fetchall()[selected_index[0]][0]
        cursor.execute('DELETE FROM books WHERE id=?', (book_id,))
        conn.commit()
        messagebox.showinfo('Success', 'Book deleted successfully!')
        display_books()
    else:
        messagebox.showerror('Error', 'Please select a book to delete.')

def update_book():
    selected_index = listbox.curselection()
    if selected_index:
        book_id = cursor.execute('SELECT id FROM books').fetchall()[selected_index[0]][0]
        title = entry_title.get()
        author = entry_author.get()
        year = entry_year.get()
        if title and author and year:
            cursor.execute('UPDATE books SET title=?, author=?, year=? WHERE id=?', (title, author, year, book_id))
            conn.commit()
            messagebox.showinfo('Success', 'Book updated successfully!')
            clear_entries()
            display_books()
        else:
            messagebox.showerror('Error', 'Please fill in all fields.')
    else:
        messagebox.showerror('Error', 'Please select a book to update.')

def show_details():
    selected_index = listbox.curselection()
    if selected_index:
        book_id = cursor.execute('SELECT id FROM books').fetchall()[selected_index[0]][0]
        book_details = cursor.execute('SELECT * FROM books WHERE id=?', (book_id,)).fetchone()
        messagebox.showinfo('Book Details', f'Title: {book_details[1]}\nAuthor: {book_details[2]}\nYear: {book_details[3]}')
    else:
        messagebox.showerror('Error', 'Please select a book to view details.')

# Main window setup
root = tk.Tk()
root.title('Library Management System')

# Entry fields
label_title = tk.Label(root, text='Title:')
label_title.grid(row=0, column=0, padx=10, pady=5)
entry_title = tk.Entry(root)
entry_title.grid(row=0, column=1, padx=10, pady=5)

label_author = tk.Label(root, text='Author:')
label_author.grid(row=1, column=0, padx=10, pady=5)
entry_author = tk.Entry(root)
entry_author.grid(row=1, column=1, padx=10, pady=5)

label_year = tk.Label(root, text='Year:')
label_year.grid(row=2, column=0, padx=10, pady=5)
entry_year = tk.Entry(root)
entry_year.grid(row=2, column=1, padx=10, pady=5)

# Buttons
button_add = tk.Button(root, text='Add Book', command=add_book)
button_add.grid(row=3, column=0, pady=10)

button_update = tk.Button(root, text='Update Book', command=update_book)
button_update.grid(row=3, column=1, pady=10)

button_delete = tk.Button(root, text='Delete Book', command=delete_book)
button_delete.grid(row=4, column=0, pady=10)

button_details = tk.Button(root, text='Book Details', command=show_details)
button_details.grid(row=4, column=1, pady=10)

# Listbox to display books
listbox = tk.Listbox(root, width=50)
listbox.grid(row=5, column=0, columnspan=2, pady=10)
display_books()

# Run the application
root.mainloop()

# Close the database connection
conn.close()
