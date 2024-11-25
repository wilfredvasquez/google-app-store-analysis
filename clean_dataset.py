import pandas as pd

# 1. Cargar el dataset
df = pd.read_csv("googleplaystore.csv")

# 2. Seleccionar columnas relevantes
columns_to_keep = [
    "App",  # Nombre de la aplicación
    "Genres",  # Géneros de la app
    "Category",  # Categoría de la app
    "Rating",  # Calificación (1-5 estrellas)
    "Reviews",  # Número de reseñas
    "Size",  # Tamaño de la app
    "Installs",  # Número de instalaciones
    "Type",  # Tipo (Free/Paid)
    "Price",  # Precio en dólares
    "Content Rating",  # Clasificación de contenido (Everyone, Teen, etc.)
]
df = df[columns_to_keep]  # Crear nuevo DataFrame solo con estas columnas


# 3. Limpiar Rating
# Ejemplo de datos en Rating: 4.1, 4.5, NaN, 'Varies with device'
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
# - pd.to_numeric() convierte strings a números
# - errors="coerce" convierte valores no numéricos a NaN
# Resultado: 4.1, 4.5, NaN, NaN

# 4. Limpiar Installs
# Ejemplo de datos en Installs: "1,000+", "5,000,000+", "Free"
df["Installs"] = df["Installs"].str.replace("+", "").str.replace(",", "")
# - Primer replace: "1,000+" → "1,000"
# - Segundo replace: "1,000" → "1000"
df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")
# Resultado: 1000, 5000000, NaN

# 5. Limpiar Price
# Ejemplo de datos en Price: "$0.99", "0", "$2.99", "Free"
df["Price"] = df["Price"].str.replace("$", "")
# - Replace: "$0.99" → "0.99"
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
# Resultado: 0.99, 0, 2.99, NaN


# 6. Limpiar Category
def clean_category(category):
    """
    Limpia y formatea el nombre de la categoría:
    HOUSE_AND_HOME -> House and Home
    """
    # Reemplazar guiones bajos por espacios y convertir a título
    return category.replace("_", " ").title()


df["Category"] = df["Category"].apply(clean_category)

# 7. Eliminar duplicados manteniendo la versión con más instalaciones
print("\nAntes de eliminar duplicados:", len(df))
# Ordenar por instalaciones y eliminar duplicados
df = (
    df.sort_values("Installs", ascending=False)
    .reset_index(drop=True)  # Resetear índice después de ordenar
    .drop_duplicates(subset=["App"], keep="first")
)
print("Después de eliminar duplicados:", len(df))


# 8. Guardar dataset limpio
df.to_csv("googleplaystore_cleaned.csv", index=False)
# - Guarda el DataFrame en un nuevo archivo CSV
# - index=False evita guardar los números de fila
