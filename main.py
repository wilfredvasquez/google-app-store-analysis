import graficas as gr
import pandas as pd

# 1. Cargar los datos y revisar estructura
print("\n=== ESTRUCTURA DE DATOS ===")
df = pd.read_csv("googleplaystore_cleaned.csv")
print("\nPrimeras 5 filas:")
print(df.head())
print("\nInformación del DataFrame:")
print(df.info())

# 2. Identificar valores nulos y duplicados
print("\n=== ANÁLISIS DE CALIDAD DE DATOS ===")
print("\nValores nulos por columna:")
print(df.isnull().sum())
print("\nDuplicados encontrados:", df.duplicated().sum())

# 3. Tipos de datos y estadísticas básicas
print("\n=== ESTADÍSTICAS DESCRIPTIVAS ===")
print(df.describe())

# 4. Métricas básicas
print("\n=== MÉTRICAS BÁSICAS ===")
# Apps por categoría
category_counts = df["Category"].value_counts()
print("\nNúmero de apps por categoría:")
print(category_counts)

# Rango de descargas
print("\nRango de descargas:")
print(f"Mínimo: {df['Installs'].min():,}")
print(f"Máximo: {df['Installs'].max():,}")

# 5. Calificación promedio por categoría
avg_rating_by_category = (
    df.groupby("Category")["Rating"]
    .agg(["mean", "count"])
    .sort_values("mean", ascending=False)
)
print("\n=== CALIFICACIÓN PROMEDIO POR CATEGORÍA ===")
print(avg_rating_by_category)

# 6. Análisis por tipo (Free vs Paid)
print("\n=== ANÁLISIS FREE VS PAID ===")
type_analysis = (
    df.groupby("Type").agg({"Rating": ["mean", "count"], "Installs": "mean"}).round(2)
)
print(type_analysis)

# 7. Relación precio-calificación
price_rating_corr = df["Price"].corr(df["Rating"])
print("\n=== CORRELACIÓN PRECIO-RATING ===")
print(f"Correlación: {price_rating_corr:.2f}")

# 8. Resumen final
print("\n=== RESUMEN DE HALLAZGOS ===")
print(f"1. Total de apps analizadas: {len(df)}")
print(f"2. Número de categorías: {len(df['Category'].unique())}")
print(
    f"3. Proporción Free/Paid: {len(df[df['Type']=='Free'])}/{len(df[df['Type']=='Paid'])}"
)
print(f"4. Rating promedio general: {df['Rating'].mean():.2f}")
print(f"5. Categoría con mejor rating: {avg_rating_by_category.index[0]}")
print(f"6. Categoría más popular (por # apps): {category_counts.index[0]}")

graficar = input("\n¿Desea generar gráficos? (s/n): ")
if graficar in ["s", "S", "y", "Y"]:
    gr.graficar(df)
