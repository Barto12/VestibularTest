import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# Función para realizar la prueba de equilibrio de Romberg
def romberg_test():
    msg = "Ponte de pie con los pies juntos y los brazos a los lados. Cierra los ojos y mantén esta posición por 30 segundos."
    result = messagebox.askokcancel("Prueba de Romberg", msg)
    if not result:
        return 'cancelado'

    # Esperar 30 segundos antes de preguntar
    root.after(30000, lambda: messagebox.showinfo("Prueba de Romberg", "Tiempo completado"))
    balanceo = messagebox.askyesno("Prueba de Romberg", "¿Te balanceaste o caíste?")
    return 'positivo' if balanceo else 'negativo'


# Función para realizar la prueba de Unterberger
def unterberger_test():
    msg = "Marcha en el mismo lugar con los ojos cerrados por 50 pasos."
    result = messagebox.askokcancel("Prueba de Unterberger", msg)
    if not result:
        return 'cancelado'

    # Esperar 20 segundos antes de preguntar
    root.after(20000, lambda: messagebox.showinfo("Prueba de Unterberger", "Tiempo completado"))
    desviación = messagebox.askyesno("Prueba de Unterberger", "¿Te desviaste significativamente al marchar?")
    return 'positivo' if desviación else 'negativo'


# Función para realizar la prueba de Fukuda
def fukuda_test():
    msg = "Marcha en el mismo lugar con los ojos cerrados por 1 minuto."
    result = messagebox.askokcancel("Prueba de Fukuda", msg)
    if not result:
        return 'cancelado'

    # Esperar 60 segundos antes de preguntar
    root.after(60000, lambda: messagebox.showinfo("Prueba de Fukuda", "Tiempo completado"))
    desviación = messagebox.askyesno("Prueba de Fukuda", "¿Te desviaste significativamente al marchar?")
    return 'positivo' if desviación else 'negativo'


# Función para registrar los síntomas del usuario
def record_symptoms():
    symptoms = []
    symptoms.append("mareo" if messagebox.askyesno("Síntomas", "¿Experimentas mareo?") else "no_mareo")
    symptoms.append("vértigo" if messagebox.askyesno("Síntomas", "¿Experimentas vértigo?") else "no_vértigo")
    symptoms.append("náuseas" if messagebox.askyesno("Síntomas", "¿Experimentas náuseas?") else "no_náuseas")
    symptoms.append(
        "pérdida_auditiva" if messagebox.askyesno("Síntomas", "¿Tienes pérdida auditiva?") else "no_pérdida_auditiva")
    return ', '.join(symptoms)


# Función para determinar cuál oído está afectado
def determine_ear_affected(romberg, unterberger, fukuda):
    if romberg == 'positivo' or unterberger == 'positivo' or fukuda == 'positivo':
        if messagebox.askyesno("Determinación", "¿Te desviaste principalmente hacia la derecha?"):
            return "derecho"
        elif messagebox.askyesno("Determinación", "¿Te desviaste principalmente hacia la izquierda?"):
            return "izquierdo"
        else:
            return "indeterminado"
    return "ninguno"


# Función para guardar los resultados en un archivo CSV
def save_results(user_id, romberg_result, unterberger_result, fukuda_result, symptoms, ear_affected):
    data = {
        "user_id": user_id,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "romberg_result": romberg_result,
        "unterberger_result": unterberger_result,
        "fukuda_result": fukuda_result,
        "symptoms": symptoms,
        "ear_affected": ear_affected
    }
    df = pd.DataFrame([data])
    df.to_csv('vestibular_results.csv', mode='a', index=False,
              header=not pd.io.common.file_exists('vestibular_results.csv'))


# Función para mostrar los resultados históricos en un gráfico
def show_results():
    try:
        df = pd.read_csv('vestibular_results.csv')
    except FileNotFoundError:
        messagebox.showinfo("Resultados", "No hay resultados disponibles")
        return

    dates = pd.to_datetime(df['date'])
    romberg_results = df['romberg_result'].apply(lambda x: 1 if x == 'positivo' else 0)
    unterberger_results = df['unterberger_result'].apply(lambda x: 1 if x == 'positivo' else 0)
    fukuda_results = df['fukuda_result'].apply(lambda x: 1 if x == 'positivo' else 0)
    ear_affected = df['ear_affected']

    fig, ax = plt.subplots()
    ax.plot(dates, romberg_results, label='Romberg', marker='o')
    ax.plot(dates, unterberger_results, label='Unterberger', marker='o')
    ax.plot(dates, fukuda_results, label='Fukuda', marker='o')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Resultado (1 = Positivo, 0 = Negativo)')
    ax.set_title('Resultados de Pruebas Vestibulares')
    ax.legend()

    for i, ear in enumerate(ear_affected):
        ax.annotate(ear, (dates[i], romberg_results[i]), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.show()


# Función para la ventana principal
def main_window():
    global root
    root = tk.Tk()
    root.title("Evaluación Vestibular")

    user_id = 1  # Este es un ejemplo, en un escenario real, esto podría provenir de un sistema de autenticación.

    frame = tk.Frame(root)
    frame.pack(pady=20)

    romberg_button = tk.Button(frame, text="Prueba de Romberg",
                               command=lambda: save_results(user_id, romberg_test(), '', '', '', ''))
    romberg_button.grid(row=0, column=0, padx=10, pady=10)

    unterberger_button = tk.Button(frame, text="Prueba de Unterberger",
                                   command=lambda: save_results(user_id, '', unterberger_test(), '', '', ''))
    unterberger_button.grid(row=0, column=1, padx=10, pady=10)

    fukuda_button = tk.Button(frame, text="Prueba de Fukuda",
                              command=lambda: save_results(user_id, '', '', fukuda_test(), '', ''))
    fukuda_button.grid(row=1, column=0, padx=10, pady=10)

    symptoms_button = tk.Button(frame, text="Registrar Síntomas",
                                command=lambda: save_results(user_id, '', '', '', record_symptoms(), ''))
    symptoms_button.grid(row=1, column=1, padx=10, pady=10)

    determine_ear_button = tk.Button(frame, text="Determinar Oído Afectado",
                                     command=lambda: save_results(user_id, '', '', '', '',
                                                                  determine_ear_affected(romberg_test(),
                                                                                         unterberger_test(),
                                                                                         fukuda_test())))
    determine_ear_button.grid(row=2, column=0, padx=10, pady=10)

    show_results_button = tk.Button(frame, text="Mostrar Resultados", command=show_results)
    show_results_button.grid(row=2, column=1, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main_window()
