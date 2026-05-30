import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

# Ruta al archivo descargado
DATA_PATH = '../data/malicious_phish.csv'

def train():
    if not os.path.exists(DATA_PATH):
        print(f"Error: No se encuentra el archivo en {DATA_PATH}")
        return

    print("Cargando dataset real (esto puede tardar un poco)...")
    df = pd.read_csv(DATA_PATH)

    # 'benign' será 0, cualquier otra cosa (phishing, malware, etc) será 1
    df['label'] = df['type'].apply(lambda x: 0 if x == 'benign' else 1)

    # Muestra de 50.000 URLs
    df_sample = df.sample(n=50000, random_state=42)

    print("Extrayendo características de las URLs...")
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3, 5))
    X = vectorizer.fit_transform(df_sample['url'])
    y = df_sample['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Entrenando el modelo PerAdBlock (Random Forest)...")
    model = RandomForestClassifier(n_estimators=100, n_jobs=-1)
    model.fit(X_train, y_train)

    # ── Métricas detalladas ───────────────────────────────────────────
    y_pred = model.predict(X_test)

    score = model.score(X_test, y_test)
    print(f"\nModelo entrenado con éxito. Precisión global: {score:.2%}")

    print("\n── Informe de clasificación ──")
    print(classification_report(y_test, y_pred, target_names=['Benigna', 'Publicitaria/Maliciosa']))

    print("── Matriz de confusión ──")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    print(f"\n  Verdaderos negativos  (benigna correcta):    {cm[0][0]}")
    print(f"  Falsos positivos      (benigna→bloqueada):   {cm[0][1]}")
    print(f"  Falsos negativos      (anuncio no detectado): {cm[1][0]}")
    print(f"  Verdaderos positivos  (anuncio detectado):   {cm[1][1]}")
    # ─────────────────────────────────────────────────────────────────

    # Guardar
    joblib.dump(model, 'modelo_peradblock.pkl')
    joblib.dump(vectorizer, 'vectorizador_peradblock.pkl')
    print("\nArchivos pkl generados en server_ia/")

if __name__ == "__main__":
    train()