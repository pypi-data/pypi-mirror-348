# 🎩 Smooth Criminal

**A Python performance acceleration toolkit with the soul of Michael Jackson.**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🚀 ¿Qué es esto?

**Smooth Criminal** es una librería de Python para acelerar funciones y scripts automáticamente usando:
- 🧠 [Numba](https://numba.pydata.org/)
- ⚡ Asyncio y threading
- 🧪 Benchmarks y profiling
- 🎶 Estilo, carisma y mensajes inspirados en MJ

---

## 💡 Características principales

| Decorador / Función     | Descripción                                           |
|-------------------------|--------------------------------------------------------|
| `@smooth`               | Aceleración con Numba (modo sigiloso y rápido)        |
| `@moonwalk`             | Convierte funciones en corutinas `async` sin esfuerzo |
| `@thriller`             | Benchmark antes y después (con ritmo)                 |
| `@jam(workers=n)`       | Paralelismo automático con ThreadPoolExecutor         |
| `@black_or_white(mode)` | Optimiza tipos numéricos (`float32` vs `float64`)     |
| `@bad`                  | Modo de optimización agresiva (`fastmath`)            |
| `@beat_it`              | Fallback automático si algo falla                     |
| `dangerous(func)`       | Mezcla poderosa de decoradores (`@bad + @thriller`)   |
| `profile_it(func)`      | Estadísticas detalladas de rendimiento                |
| `analyze_ast(func)`     | Análisis estático para detectar código optimizable    |

---

## ⚙️ Instalación

```bash
pip install smooth-criminal
```

O si estás desarrollando localmente:

```bash
pip install -e .
```

## 💃 Ejemplo rápido

```python
from smooth_criminal import smooth, thriller

@thriller
@smooth
def square(n):
    return [i * i for i in range(n)]

print(square(10))

```

## 🧪 CLI interactiva

```bash
smooth-criminal analyze my_script.py
```
Esto analizará tu código buscando funciones lentas, bucles, range(), y más.

## 📚 Documentación

Próximamente en ReadTheDocs…

## 📝 Licencia

MIT © Adolfo González

## 🎤 Créditos

- Michael Jackson por la inspiración musical 🕺

- Numba, NumPy, asyncio por la base técnica


