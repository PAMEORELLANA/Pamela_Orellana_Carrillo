import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

# Conexión a la base de datos MySQL
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="logistica"
    )

# Función para agregar un nuevo envío
def add_envio():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = "INSERT INTO Envios (NumeroSeguimiento, Origen, Destino, FechaEntregaPrevista, Estado) VALUES (%s, %s, %s, %s, %s)"
        values = (
            entry_numero.get(),
            entry_origen.get(),
            entry_destino.get(),
            entry_fecha.get(),
            "En tránsito"
        )
        cursor.execute(sql, values)
        conn.commit()
        messagebox.showinfo("Éxito", "Envío agregado correctamente")
        clear_entries()
        display_envios()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()
        conn.close()

# Función para mostrar los envíos registrados
def display_envios():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Envios")
        rows = cursor.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for row in rows:
            tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()
        conn.close()

# Función para actualizar el estado de un envío
def update_envio():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = "UPDATE Envios SET Estado=%s, FechaEntregaPrevista=%s WHERE NumeroSeguimiento=%s"
        values = (
            combo_estado.get(),
            entry_fecha.get(),
            entry_numero.get()
        )
        cursor.execute(sql, values)
        conn.commit()
        messagebox.showinfo("Éxito", "Envío actualizado correctamente")
        clear_entries()
        display_envios()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()
        conn.close()

# Función para limpiar los campos de entrada
def clear_entries():
    entry_numero.delete(0, tk.END)
    entry_origen.delete(0, tk.END)
    entry_destino.delete(0, tk.END)
    entry_fecha.delete(0, tk.END)
    combo_estado.set("En tránsito")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Gestión de Envíos de Mercancías")

tk.Label(root, text="Número de Seguimiento").grid(row=0, column=0)
tk.Label(root, text="Origen").grid(row=1, column=0)
tk.Label(root, text="Destino").grid(row=2, column=0)
tk.Label(root, text="Fecha de Entrega Prevista (YYYY-MM-DD)").grid(row=3, column=0)
tk.Label(root, text="Estado").grid(row=4, column=0)

entry_numero = tk.Entry(root)
entry_origen = tk.Entry(root)
entry_destino = tk.Entry(root)
entry_fecha = tk.Entry(root)
combo_estado = ttk.Combobox(root, values=["En tránsito", "Entregado"])

entry_numero.grid(row=0, column=1)
entry_origen.grid(row=1, column=1)
entry_destino.grid(row=2, column=1)
entry_fecha.grid(row=3, column=1)
combo_estado.grid(row=4, column=1)
combo_estado.set("En tránsito")

btn_add = tk.Button(root, text="Agregar Envío", command=add_envio)
btn_update = tk.Button(root, text="Actualizar Envío", command=update_envio)
btn_clear = tk.Button(root, text="Limpiar Campos", command=clear_entries)

btn_add.grid(row=5, column=0)
btn_update.grid(row=5, column=1)
btn_clear.grid(row=5, column=2)

columns = ("ID", "NumeroSeguimiento", "Origen", "Destino", "FechaEntregaPrevista", "Estado")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.grid(row=6, column=0, columnspan=3)

display_envios()

root.mainloop()

