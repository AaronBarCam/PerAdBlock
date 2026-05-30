# 🍐🛡️ PerAdBlock

> Bloqueador de publicidad basado en Inteligencia Artificial para navegadores Chromium.

PerAdBlock es una extensión de navegador (Manifest V3) que se conecta a un servidor local en Python para clasificar URLs en tiempo real mediante un modelo **Random Forest** entrenado con más de 650.000 URLs reales. A diferencia de los bloqueadores tradicionales, no depende de listas de filtros estáticas: detecta publicidad analizando la **estructura léxica** de cada URL.

---

## 🧠 ¿Cómo funciona?

```
Usuario navega → background.js intercepta la URL
                        ↓
             POST /predict a FastAPI (localhost:8000)
                        ↓
         TF-IDF vectoriza la URL en n-gramas de caracteres
                        ↓
         Random Forest devuelve probabilidad de ser anuncio
                        ↓
        Si confianza > 80% → bloqueo + contador +1
        content.js oculta elementos del DOM residuales
```

---

## 🗂️ Estructura del proyecto

```
PerAdBlock/
├── data/
│   └── malicious_phish.csv          # Dataset de entrenamiento (651.199 URLs)
├── extension/
│   ├── manifest.json                # Configuración de la extensión (MV3)
│   ├── background.js                # Service Worker: intercepta peticiones de red
│   ├── content.js                   # Content Script: limpia el DOM de anuncios
│   ├── rules.json                   # Regla declarativa de bloqueo
│   ├── icons/
│   │   └── icon128.png
│   └── popup/
│       ├── popup.html               # Interfaz del popup
│       └── popup.js                 # Lógica del popup (contador de bloqueos)
└── server_ia/
    ├── train_model.py               # Script de entrenamiento del modelo
    ├── main.py                      # Servidor FastAPI con endpoint /predict
    ├── modelo_peradblock.pkl        # Modelo entrenado (generado al entrenar)
    ├── vectorizador_peradblock.pkl  # Vectorizador TF-IDF (generado al entrenar)
    └── requirements.txt             # Dependencias Python
```

---

## ⚙️ Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Extensión | JavaScript ES6+, Manifest V3, Chrome API |
| Servidor | Python 3.12, FastAPI, Uvicorn |
| Modelo IA | Scikit-learn — Random Forest + TF-IDF (n-gramas de caracteres) |
| Serialización | Joblib |
| Validación API | Pydantic |
| Dataset | [Malicious URLs Dataset — Kaggle](https://www.kaggle.com/datasets/sid321ax2/malicious-urls-dataset) |

---

## 🚀 Instalación y uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/PerAdBlock.git
cd PerAdBlock
```

### 2. Instalar dependencias Python

```bash
cd server_ia
pip install -r requirements.txt
```

### 3. Entrenar el modelo *(opcional si ya tienes los .pkl)*

> Requiere tener el archivo `data/malicious_phish.csv` descargado desde [Kaggle](https://www.kaggle.com/datasets/sid321ax2/malicious-urls-dataset).

```bash
python train_model.py
```

Esto genera `modelo_peradblock.pkl` y `vectorizador_peradblock.pkl` en la carpeta `server_ia/`.

### 4. Iniciar el servidor FastAPI

```bash
uvicorn main:app --reload
```

El servidor estará disponible en `http://localhost:8000`.  
Puedes verificarlo en `http://localhost:8000/docs` (interfaz Swagger).

### 5. Cargar la extensión en el navegador

1. Abre `chrome://extensions` (o `opera://extensions`, `edge://extensions`).
2. Activa el **Modo desarrollador**.
3. Haz clic en **Cargar descomprimida** y selecciona la carpeta `extension/`.
4. El icono 🍐🛡️ aparecerá en la barra de herramientas.

> ⚠️ El servidor FastAPI debe estar activo para que el análisis de IA funcione. Si está apagado, la extensión no genera errores y la navegación continúa con normalidad.

---

## 🔌 Endpoint de la API

### `POST /predict`

**Body:**
```json
{
  "url": "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"
}
```

**Respuesta:**
```json
{
  "url": "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js",
  "is_ad": true,
  "confidence": 0.85
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `is_ad` | boolean | `true` si la URL supera el umbral del 80% de confianza |
| `confidence` | float | Probabilidad asignada por el modelo (0.0 – 1.0) |

---

## 📊 Rendimiento del modelo

Entrenado sobre una muestra de **50.000 URLs** del dataset de Kaggle (división 80/20):

| Métrica | Valor |
|---------|-------|
| Accuracy | **95.90 %** |
| Precision (media) | 0.96 |
| Recall (media) | 0.95 |
| F1-score (media) | 0.95 |
| Verdaderos negativos | 6.529 |
| Verdaderos positivos | 3.061 |
| Falsos positivos | 95 |
| Falsos negativos | 315 |

**Umbral de confianza:** 80% — reduce falsos positivos para no romper páginas legítimas.

---

## 🧪 Pruebas

Puedes probar el tiempo de respuesta de la API con:

```bash
curl -w "\nTiempo total: %{time_total}s\n" -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"url\": \"https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js\"}"
```

Resultado obtenido:

```
{"url":"...googlesyndication...","is_ad":true,"confidence":0.85}
Tiempo total: 0.283336s
```

**Benchmarks externos:**

| Herramienta de test | Resultado |
|--------------------|-----------|
| [adblock-tester.com](https://adblock-tester.com) | 51 / 100 |
| [canyoublockit.com](https://canyoublockit.com) | Detección activa |

> El resultado de 51/100 en adblock-tester es coherente con el enfoque: la IA clasifica por estructura léxica de la URL, no por nombre de dominio. No necesita que el dominio esté en ninguna lista para bloquearlo.

---

## 📋 Requisitos del sistema

- Python 3.10 o superior
- Navegador basado en Chromium (Chrome, Opera, Edge, Brave)
- ~500 MB de RAM para el modelo en memoria

---

## 📚 Referencias

- [Malicious URLs Dataset — Kaggle](https://www.kaggle.com/datasets/sid321ax2/malicious-urls-dataset)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Chrome Extensions — Manifest V3](https://developer.chrome.com/docs/extensions/mv3/intro/)
- [Scikit-learn — Random Forest](https://scikit-learn.org/stable/modules/ensemble.html)
- Breiman, L. (2001). *Random Forests*. Machine Learning, 45(1), 5–32.

---

## 👨‍💻 Autor

**Aarón Barral Camacho**  
Proyecto Final de Ciclo — CFGS Desarrollo de Aplicaciones Multiplataforma  
I.E.S. Castillo de Luna, Rota (Cádiz) · Curso 2025–2026  

---

<p align="center">Hecho con 🍐 y mucho café</p>
