import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
import funciones

# Crea ventana principal
root = tkinter.Tk()
root.title("App OCR")
root.resizable(width=False, height=False)
# redimensiona
root.geometry("300x300")
# Panel para pestañas
panel =ttk.Notebook(root)
panel.pack(fill='both', expand='yes')
# Crea pestañas
pest1 = ttk.Frame(panel)
pest2 = ttk.Frame(panel)
# Elementos de la pestaña 1
label = ttk.Label(pest1,text="Aquí podrá leer un archivo pdf\ny configurar los datos a extraer.")
#label.place()
label.pack(padx=20, pady=20)

#label.pack()
btnDir = ttk.Button(pest1, text='CONFIGURAR PDF', command=funciones.selectFilesConfig )
btnDir.pack(padx=20, pady=70)
# Elementos de la pestaña 2
label2 = ttk.Label(pest2,text="Aquí podrá seleccionar el directorio\n     que contiene sus archivos.")
label2.pack(padx=20, pady=20)
open_button = ttk.Button(pest2, text='SELECCIONE UN DIRECTORIO',command=funciones.selectFolder )
open_button.pack(padx=20, pady=40)
#progressBar = ttk.Progressbar(pest2, orient='horizontal',length=200).pack()



# Agrega pestañas
panel.add(pest1,text='  CONFIGURAR  ')
panel.add(pest2,text='  LEER DOCUMENTOS  ')
root.mainloop()