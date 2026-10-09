# Sapori di Puglia API 🌿🍝

Un'API RESTful moderna e robusta sviluppata con **FastAPI** per la gestione di un catalogo digitale di ricette tradizionali della cucina pugliese. Il progetto implementa validazione avanzata dei dati tramite **Pydantic v2**, gestione dei parametri di percorso, query parameters strutturati e operazioni CRUD.

---

## 🚀 Caratteristiche Principali

- **FastAPI**: Framework ad alte prestazioni per la creazione di API in Python.
- **Validazione con Pydantic**: Modelli dedicati per la validazione di Request Body, Path Parameters e Query Parameters.
- **Filtri Avanzati**: Gestione dei parametri di ricerca, categorie e paginazione tramite Dependency Injection (`Depends`).
- **Documentazione Automatica**: Interfacce interattive pronte all'uso (Swagger UI e ReDoc).
- **Supporto CORS**: Middleware configurato per consentire l'integrazione con qualsiasi frontend.

---

## 🛠️ Requisiti e Installazione

Assicurati di avere Python installato sul tuo sistema (consigliato Python 3.10+) e il package manager **Poetry**.

1. **Clona il repository o posizionati nella cartella del progetto.**

2. **Installa le dipendenze con Poetry:**
   ```bash
   poetry install