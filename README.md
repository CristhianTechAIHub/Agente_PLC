# 🏭 Industrial RAG Agent para documentos

Un agente conversacional de Inteligencia Artificial diseñado para extraer, analizar y responder preguntas técnicas precisas basadas en documentación industrial compleja (manuales de Siemens S7-1500 TM NPU).

## 💡 El Problema
En la automatización industrial, los ingenieros pierden horas valiosas buscando parámetros específicos de configuración, voltajes o procedimientos de seguridad dentro de manuales PDF de cientos de páginas. 

## 🚀 La Solución
Este proyecto implementa una arquitectura **RAG (Retrieval-Augmented Generation)** local. Permite a los usuarios hacer preguntas en lenguaje natural y obtener respuestas técnicas inmediatas, citando exactamente el **documento y el número de página** de donde se extrajo la información para garantizar la trazabilidad y evitar alucinaciones.

## ⚙️ Arquitectura Técnica
El sistema está construido con un enfoque modular y escalable:
* **Orquestación:** LangGraph y LangChain para la gestión del estado y las herramientas del agente.
* **Motor de Razonamiento (LLM):** Claude 3.5 Haiku (vía API de Anthropic) configurado con `ToolStrategy` para salidas estructuradas estrictas.
* **Vectorización Local:** Modelos de HuggingFace (`all-MiniLM-L6-v2`) ejecutados en CPU para garantizar la privacidad de los documentos industriales.
* **Base de Datos Vectorial:** FAISS (Facebook AI Similarity Search) en memoria para recuperaciones de latencia ultrabaja.

## 🛠️ Instalación y Uso

1. Clona este repositorio:
   ```bash
   git clone [https://github.com/TU_USUARIO/Industrial-Agent-AI.git](https://github.com/TU_USUARIO/Agente_PLC.git)
