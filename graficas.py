import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def format_func(value, tick_number):
    if value >= 1e9:
        return f"{value/1e9:.2f}B"
    if value >= 1e6:
        return f"{value/1e6:.2f}M"
    return f"{value/1e3:.2f}K"


def graficar(df):

    # 8-12. Visualizaciones
    plt.style.use("seaborn")

    # Primera página de gráficos
    plt.figure(figsize=(15, 10))

    # Gráfico 1: Apps por categoría
    # ---------------------------------------
    # Obtener top 10 categorías por número de apps
    category_counts = df["Category"].value_counts().head(10)

    plt.subplot2grid((2, 2), (0, 0))
    category_counts.plot(kind="bar")
    plt.xticks(rotation=45, ha="right")
    plt.title("Top 10 Categorías por Número de Apps")
    plt.ylabel("Número de Apps")
    plt.xlabel("Categoría")
    # ---------------------------------------

    # Gráfico 2: Top 10 categorías por descargas
    # ---------------------------------------
    # Obtener top 10 categorías por número de descargas
    downloads_by_category = (
        df.groupby("Category")["Installs"].sum().sort_values(ascending=False)
    ).head(10)

    plt.subplot2grid((2, 2), (0, 1))
    downloads_by_category.plot(kind="bar")
    plt.title("Top 10 Categorías por Número Total de Descargas")
    plt.xlabel("Categoría")
    plt.ylabel("Número de Descargas")
    plt.xticks(rotation=45, ha="right")
    # Mejorar el formato del eje y
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    # ---------------------------------------

    # Gráfico 3: Top 10 apps más descargadas
    # ---------------------------------------
    # Obtener top 10 apps más descargadas
    top_10_apps = df.nlargest(10, "Installs")[
        ["App", "Category", "Installs", "Rating", "Reviews"]
    ]
    print("Top 10 apps más descargadas")
    print(top_10_apps)

    plt.subplot2grid((2, 2), (1, 0), colspan=2)
    bars = plt.bar(top_10_apps["App"], top_10_apps["Installs"])
    # Colorear las barras por categoría
    categories = top_10_apps["Category"].unique()
    color_map = dict(zip(categories, plt.cm.Set3(np.linspace(0, 1, len(categories)))))
    for bar, category, rating, reviews in zip(
        bars, top_10_apps["Category"], top_10_apps["Rating"], top_10_apps["Reviews"]
    ):
        bar.set_color(color_map[category])
        # Agregar el rating sobre cada barra
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            bar.get_y() + height / 2.0,
            f"Rating:\n{rating:.1f}\n\nReviews:\n{reviews:,}",
            ha="center",
            va="bottom",
        )

    plt.title("Top de Aplicaciones más Descargadas")
    plt.xlabel("Aplicación")
    plt.ylabel("Número de Descargas")
    plt.xticks(rotation=45, ha="right")
    # Mejorar el formato del eje y
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(format_func))
    # Agregar leyenda de categorías
    legend_elements = [
        plt.Rectangle((0, 0), 1, 1, color=color_map[cat]) for cat in categories
    ]
    plt.legend(
        legend_elements,
        categories,
        title="Categorías",
        loc="lower right",
        bbox_to_anchor=(1.15, 1),
    )
    # ---------------------------------------

    plt.tight_layout()
    plt.show()

    # Tercera página de gráficos
    # ---------------------------------------
    plt.figure(figsize=(15, 10))

    # Gráfico 1: Distribución de Apps Gratuitas vs de Pago
    plt.subplot2grid((2, 2), (0, 0))
    # Obtener el conteo por tipo
    type_counts = df["Type"].value_counts()

    # Crear gráfico de pie
    colors = ["#2ecc71", "#e74c3c"]  # Verde para Free, Rojo para Paid
    total_apps = len(df)
    plt.pie(
        type_counts.values,
        labels=type_counts.index,
        colors=colors,
        autopct=lambda pct: f"{pct:.1f}%\n({int(pct/100.*total_apps):,})",
        startangle=90,
        wedgeprops=dict(width=0.7),
    )  # Esto lo convierte en un donut chart

    # Personalizar gráfico
    plt.title("Distribución de Apps Gratuitas vs de Pago", pad=20)

    # Asegurar que el círculo se vea como un círculo
    plt.axis("equal")

    # Gráfico 2: Distribución de Apps por Content Rating
    plt.subplot2grid((2, 2), (0, 1))
    # Obtener el conteo por Content Rating
    content_counts = df["Content Rating"].value_counts()
    # Crear gráfico de barras
    bars = plt.bar(content_counts.index, content_counts.values)

    # Definir colores para cada categoría
    colors = {
        "Everyone": "#2ecc71",  # Verde
        "Teen": "#3498db",  # Azul
        "Everyone 10+": "#f1c40f",  # Amarillo
        "Mature 17+": "#e74c3c",  # Rojo
        "Adults only 18+": "#c0392b",  # Rojo oscuro
        "Unrated": "#95a5a6",  # Gris
    }

    # Aplicar colores a las barras
    for bar, content in zip(bars, content_counts.index):
        bar.set_color(colors.get(content, "#95a5a6"))

    # Agregar etiquetas con valores y porcentajes
    total_apps = len(df)
    for bar in bars:
        height = bar.get_height()
        percentage = (height / total_apps) * 100
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{int(height):,}\n({percentage:.1f}%)",
            ha="center",
            va="bottom",
        )

    # Personalizar gráfico
    plt.title("Distribución de Apps por Clasificación de Contenido", pad=20)
    plt.xlabel("Clasificación de Contenido")
    plt.ylabel("Número de Apps")
    # Agregar grid para mejor lectura
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Rotar etiquetas si es necesario
    plt.xticks(rotation=15)

    # Gráfico 3: Correlación
    # 1. Preparar datos numéricos para correlación
    numeric_df = df[["Rating", "Reviews", "Installs", "Price"]]

    # 2. Calcular matriz de correlación
    correlation_matrix = numeric_df.corr()

    # 3. Visualizar matriz de correlación
    plt.subplot2grid((2, 2), (1, 0))
    sns.heatmap(
        correlation_matrix,
        annot=True,  # Mostrar valores
        cmap="coolwarm",  # Esquema de colores
        center=0,  # Centro del colormap
        fmt=".2f",  # Formato de números
        square=True,
    )  # Hacer celdas cuadradas

    plt.title("Matriz de Correlaciones")

    plt.tight_layout()
    plt.show()
