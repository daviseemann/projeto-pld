import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime

from app.database import SessionLocal
from app.models import PLDData


def create_dashboard():
    # Função para buscar dados do banco e atualizar o gráfico
    def update_chart():
        submarket = submarket_var.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

        with SessionLocal() as session:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            results = (
                session.query(PLDData)
                .filter(
                    PLDData.submarket == submarket,
                    PLDData.timestamp >= start,
                    PLDData.timestamp <= end,
                )
                .all()
            )

            dates = [result.timestamp for result in results]
            prices = [result.price for result in results]

            ax.clear()
            ax.plot(dates, prices, marker="o")
            ax.set_title(f"PLD - {submarket}")
            ax.set_xlabel("Data")
            ax.set_ylabel("Preço (R$)")
            fig.autofmt_xdate()
            canvas.draw()

    # Criação da janela principal
    root = tk.Tk()
    root.title("Dashboard PLD")

    # Widgets para seleção de submercado e intervalo de datas
    submarket_var = tk.StringVar(value="SE")
    submarket_label = ttk.Label(root, text="Submercado:")
    submarket_label.grid(column=0, row=0, padx=5, pady=5)
    submarket_combo = ttk.Combobox(root, textvariable=submarket_var)
    submarket_combo["values"] = ("SE", "S", "NE", "N")
    submarket_combo.grid(column=1, row=0, padx=5, pady=5)

    start_date_label = ttk.Label(root, text="Data Início (YYYY-MM-DD):")
    start_date_label.grid(column=0, row=1, padx=5, pady=5)
    start_date_entry = ttk.Entry(root)
    start_date_entry.grid(column=1, row=1, padx=5, pady=5)

    end_date_label = ttk.Label(root, text="Data Fim (YYYY-MM-DD):")
    end_date_label.grid(column=0, row=2, padx=5, pady=5)
    end_date_entry = ttk.Entry(root)
    end_date_entry.grid(column=1, row=2, padx=5, pady=5)

    update_button = ttk.Button(root, text="Atualizar Gráfico", command=update_chart)
    update_button.grid(column=0, row=3, columnspan=2, pady=10)

    # Criação do gráfico
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(column=0, row=4, columnspan=2)

    # Inicializa a interface
    root.mainloop()


# Corrigir a verificação do nome do módulo principal
if __name__ == "__main__":
    create_dashboard()
