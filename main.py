import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime

class CourtsBquillaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Court's Bquilla")
        self.root.geometry("420x350")
        self.root.resizable(False, False)

        # Variables para capturar los datos del usuario
        self.nombre_var = tk.StringVar()
        self.cancha_var = tk.StringVar(value="Cancha Norte (Fútbol 5)")
        self.fecha_var = tk.StringVar()
        self.hora_var = tk.StringVar()

        # Llamar al método que dibuja la interfaz
        self.crear_interfaz()

    def crear_interfaz(self):
        # Título principal dentro de la app
        titulo = tk.Label(self.root, text="⚽ Reservas Court's Bquilla ⚽", font=("Arial", 16, "bold"))
        titulo.pack(pady=15)

        # Contenedor (Frame) para organizar el formulario
        frame_form = tk.Frame(self.root)
        frame_form.pack(pady=10)

        # Fila 0: Nombre del Cliente
        tk.Label(frame_form, text="Nombre del Cliente:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(frame_form, textvariable=self.nombre_var, width=25).grid(row=0, column=1, padx=10, pady=10)

        # Fila 1: Selección de Cancha (Menú desplegable)
        tk.Label(frame_form, text="Cancha:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        opciones_canchas = ["Cancha Norte (Fútbol 5)", "Cancha Sur (Fútbol 5)", "Cancha Central (Fútbol 7)"]
        tk.OptionMenu(frame_form, self.cancha_var, *opciones_canchas).grid(row=1, column=1, padx=10, pady=10, sticky="we")

        # Fila 2: Fecha de reserva
        tk.Label(frame_form, text="Fecha (DD/MM/AAAA):", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(frame_form, textvariable=self.fecha_var, width=25).grid(row=2, column=1, padx=10, pady=10)

        # Fila 3: Hora de reserva
        tk.Label(frame_form, text="Hora (Ej. 18:00):", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(frame_form, textvariable=self.hora_var, width=25).grid(row=3, column=1, padx=10, pady=10)

        # Botón para confirmar y exportar el recibo
        btn_reservar = tk.Button(self.root, text="Reservar y Exportar Recibo", bg="#2E86C1", fg="white", 
                                 font=("Arial", 11, "bold"), cursor="hand2", command=self.generar_recibo)
        btn_reservar.pack(pady=20)

    def generar_recibo(self):
        # 1. Obtener datos
        nombre = self.nombre_var.get().strip()
        cancha = self.cancha_var.get()
        fecha_str = self.fecha_var.get().strip()
        hora_str = self.hora_var.get().strip()

        # 2. Validación de campos vacíos
        if not nombre or not fecha_str or not hora_str:
            messagebox.showwarning("Atención", "Por favor, completa todos los campos.")
            return

        # 3. Validación de Formato de Fecha y Hora
        try:
            # Intenta convertir el texto a un objeto de fecha real
            fecha_valida = datetime.strptime(fecha_str, "%d/%m/%Y")
            
            # Intenta convertir el texto a un objeto de hora real
            hora_valida = datetime.strptime(hora_str, "%H:%M")
        except ValueError:
            # esta es la vaina de las excepciones osea si se ingresan fechas incorrectas o con formato incorrecto, se muestra un mensaje de error
            messagebox.showerror("Formato Incorrecto", 
                                 "La fecha o la hora no son válidas.\n\n"
                                 "Usa estos formatos:\n"
                                 "Fecha: DD/MM/AAAA (Ej: 25/05/2026)\n"
                                 "Hora: HH:MM (Ej: 19:30)")
            return

        # 4. Si todo está bien, Se procede con la exportación
        fecha_emision = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        recibo_texto = (
            "========================================\n"
            "             COURT'S BQUILLA            \n"
            "         Confirmación de Reserva        \n"
            "========================================\n\n"
            f"Fecha de emisión: {fecha_emision}\n\n"
            f"Cliente: {nombre}\n"
            f"Cancha: {cancha}\n"
            f"Fecha del partido: {fecha_str}\n"
            f"Hora del partido: {hora_str}\n\n"
            "========================================\n"
        )

        archivo = filedialog.asksaveasfile(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")],
            title="Guardar recibo",
            initialfile=f"Reserva_{nombre.replace(' ', '_')}.txt"
        )

        if archivo:
            archivo.write(recibo_texto)
            archivo.close()
            messagebox.showinfo("Éxito", "Reserva guardada correctamente.")
            self.limpiar_campos()

    def limpiar_campos(self):
        # Reiniciar los valores a su estado original incluyendo aja la cancha que esta por defecto que es la norte
        self.nombre_var.set("")
        self.fecha_var.set("")
        self.hora_var.set("")
        self.cancha_var.set("Cancha Norte (Fútbol 5)")

# Bloque main: Punto de entrada de la aplicación
if __name__ == "__main__":
    # Inicializar la ventana principal de tkinter
    ventana_principal = tk.Tk()
    
    # Instanciar nuestra clase, pasándole la ventana principal
    app = CourtsBquillaApp(ventana_principal)
    
    # no borrar esta linea porque es la que mantiene la ventana abierta, sin esta linea la ventana se abriria y cerraria inmediatamente
    ventana_principal.mainloop()