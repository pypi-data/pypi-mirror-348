# CapibaraGPT

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT%20%7C%20Commercial-blue.svg)](LICENSE)
[![PyPI Version](https://img.shields.io/pypi/v/capibara.svg)](https://pypi.org/project/capibara/)
[![Documentation Status](https://readthedocs.org/projects/capibara-model/badge/?version=latest)](https://capibara.readthedocs.io/en/latest/?badge=latest)

CapibaraGPT es un modelo de lenguaje avanzado basado en State Space Models (SSM) y tecnologías innovadoras de procesamiento de lenguaje natural.

## Características Principales

- Arquitectura basada en State Space Models (SSM)
- Soporte para TPU y GPU
- Integración con JAX y TensorFlow
- Modelos preentrenados disponibles
- API simple y fácil de usar
- Soporte para múltiples idiomas
- Optimización para inferencia y entrenamiento

## Instalación

```bash
pip install capibara
```

Para instalar con soporte de TPU:

```bash
pip install capibara[tpu]
```

Para desarrollo:

```bash
pip install -e ".[dev]"
```

## Uso Básico

```python
from capibara import CapibaraModel

# Cargar el modelo
model = CapibaraModel.from_pretrained("capibara-base")

# Generar texto
text = model.generate("Hola, ¿cómo estás?")
print(text)
```

## Documentación

La documentación completa está disponible en [Read the Docs](https://capibara.readthedocs.io/en/latest/).

## Requisitos del Sistema

- Python 3.9 o superior
- CUDA 11.8+ (para soporte GPU)
- TPU v3+ (para soporte TPU)
- 16GB+ RAM
- 20GB+ espacio en disco

## Contribuir

Las contribuciones son bienvenidas. Por favor, consulta nuestras [guías de contribución](CONTRIBUTING.md) para más detalles.

## Licencia

Este proyecto está bajo una licencia dual:

1. **Licencia MIT para uso académico y científico**
   - Libre para uso en investigación
   - Libre para uso en instituciones educativas
   - Libre para proyectos sin ánimo de lucro
   - Libre para desarrollo de código abierto

2. **Licencia Comercial para uso empresarial**
   - Requiere licencia comercial para uso en empresas
   - Requiere licencia comercial para servicios comerciales
   - Requiere licencia comercial para proyectos gubernamentales

Para más detalles sobre los términos de la licencia, consulta:
- [LICENSE](LICENSE) (Español)
- [LICENSE.en](LICENSE.en) (English)

Para obtener una licencia comercial, contacta a:
- Email: licence@capibaragpt.com
- Website: https://www.anachroni.co/licence/

## Cita

Si usas CapibaraGPT en tu investigación, por favor cita nuestro trabajo:

```bibtex
@software{capibara2025,
  author = {Anachroni s.coop},
  title = {CapibaraGPT: Modelo de lenguaje avanzado basado en SSM},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/anachroni-io/capibara-model}}
}
```

## Contacto

Para preguntas y soporte, por favor abre un issue en nuestro [GitHub](https://github.com/anachroni-io/capibara-model/issues).

## Agradecimientos

Agradecemos a todos los contribuidores y a la comunidad de código abierto por su apoyo y contribuciones.
