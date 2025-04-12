# RAG Credit Agricole

A Retrieval-Augmented Generation (RAG) system for analyzing PDF documents using OCR and vector embeddings.

## Setup

1. Create a virtual environment and activate it:
```bash
uv venv
. venv/bin/activate
```

2. Install dependencies:
```bash
uv pip install -r requirements.txt
```

3. Create `.env` file with required API keys:
```
MISTRAL_API_KEY=your_mistral_api_key
OPENAI_API_KEY=your_openai_api_key
```
4. Load `.env` with:
```bash
. .env
```

## Commits

### Pre-commit Hooks

To ensure code quality and consistency, set up pre-commit hooks:

2. Install the hooks defined in `.pre-commit-config.yaml`:
  ```bash
  pre-commit install
  ```

3. Run the hooks manually on all files:
  ```bash
  pre-commit run --all-files
  ```

Pre-commit hooks will now automatically run on every commit to check and format your code.


## Usage

1. Start the API server:
```bash
docker build -t rag-api .
docker run --name rag-api-container -p 8000:8000 rag-api
```

2. Upload a PDF file:
```bash
curl -X POST http://localhost:8000/upload_pdf \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/pdfs/your_pdf.pdf"
```

3. Create the vector database (with optional chunking parameters):
```bash
curl -X POST http://localhost:8000/create_vector_db \
  -H "Content-Type: application/json" \
  -d '{
    "chunk_size": 1000,
    "chunk_overlap": 100
  }'
```

4. Query the API:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "In quale stagione è stata inaugurata la Coppa del Mondo di sci alpino?",
    "n_documents": 10,
    "llm_model": "gpt-4o"
  }'
```

  Alternatively, you can access the FastAPI Swagger UI for an interactive experience. Open your browser and navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to explore and test the API endpoints.

## TODO
- Better implementation of `.env` for docker deployement.
- Implement error handling for missing or invalid `.env` configurations.
- Write detailed documentation for API endpoints.
- Add logging and monitoring for the API service.
- Explore integration with cloud-based vector databases.
- Add examples of real-world use cases in the documentation.



<details>
<summary>RESULTS</summary>

> **Q: In quale stagione è stata inaugurata la Coppa del Mondo di sci alpino?**  
La Coppa del Mondo di sci alpino è stata inaugurata nella stagione 1966-1967.


> **Q: Quali sono le discipline in cui si gareggia nella Coppa del Mondo di sci alpino?**  
Le discipline in cui si gareggia nella Coppa del Mondo di sci alpino sono: discesa libera, supergigante, slalom gigante e slalom speciale. Inoltre, dal 2007 al 2020 si è gareggiato anche nella disciplina della combinata, mentre dal 2011 al 2022 si sono disputate alcune gare di slalom parallelo.


> **Come vengono assegnati i punti ai primi 30 classificati di ogni gara?**  
Ai primi 30 classificati di ogni gara di Coppa del Mondo di sci alpino vengono assegnati punti secondo il seguente schema:\n\n1. 100 punti\n2. 80 punti\n3. 60 punti\n4. 50 punti\n5. 45 punti\n6. 40 punti\n7. 36 punti\n8. 32 punti\n9. 29 punti\n10. 26 punti\n11. 24 punti\n12. 22 punti\n13. 20 punti\n14. 18 punti\n15. 16 punti\n16. 15 punti\n17. 14 punti\n18. 13 punti\n19. 12 punti\n20. 11 punti\n21. 10 punti\n22. 9 punti\n23. 8 punti\n24. 7 punti\n25. 6 punti\n26. 5 punti\n27. 4 punti\n28. 3 punti\n29. 2 punti\n30. 1 punto


> **Qual è il distacco massimo dal primo classificato oltre il quale non vengono assegnati punti ai concorrenti entro il 30º posto?**  
Il distacco massimo dal primo classificato oltre il quale non vengono assegnati punti ai concorrenti entro il 30º posto è di 8 secondi.

> **Quale nazione ha vinto il maggior numero totale di Coppe del Mondo generali (maschili e femminili)?**  
L'Austria ha vinto il maggior numero totale di Coppe del Mondo generali, considerando sia le competizioni maschili che femminili.


> **Oggi è il 2000: quando Mikaela Shiffrin farà il suo debutto in Coppa del Mondo di sci alpino?**  
Mikaela Shiffrin farà il suo debutto in Coppa del Mondo di sci alpino nel 2011.


> **Se un atleta ottiene una media di 80 punti per gara e partecipa a 30 gare in una stagione, può vincere la Coppa del Mondo generale? (Considerando che mediamente il vincitore della Coppa del Mondo totalizza circa 1500-2000 punti in una stagione).**  
Se un atleta ottiene una media di 80 punti per gara e partecipa a 30 gare in una stagione, accumulerebbe un totale di 2400 punti (80 punti/gara * 30 gare = 2400 punti). Considerando che mediamente il vincitore della Coppa del Mondo totalizza circa 1500-2000 punti in una stagione, un totale di 2400 punti sarebbe sufficiente per vincere la Coppa del Mondo generale.

> **In media in carriera, ogni quanti anni Marcel Hirsher ha vinto una coppa del mondo generale?**  
Marcel Hirscher ha vinto 8 Coppe del Mondo generali durante la sua carriera, che è durata dal 2007 al 2019, quindi per 12 anni. In media, ha vinto una Coppa del Mondo generale ogni 1.5 anni (12 anni di carriera diviso 8 vittorie).

> **Quanto tempo è trascorso in termini di anni tra le due vittorie della Coppa del Mondo Generale di Federica Brignone?**  
Federica Brignone ha vinto la Coppa del Mondo Generale nel 2020 e nel 2021. Pertanto, è trascorso 1 anno tra le due vittorie.


> **Se la prima atleta all'arrivo conclude la gara con un tempo di 59\"10, quale è il tempo massimo entro il quale un atleta che termina la gara nelle prime 30 posizioni deve arrivare per ottenere punti?**  
Un atleta che termina la gara nelle prime 30 posizioni deve arrivare entro un distacco massimo dell'8% del tempo del primo classificato. \n\nSe il primo atleta ha un tempo di 59\"10, calcoliamo l'8% di questo tempo:\n\n1. Convertiamo il tempo in secondi: 59\"10 = 59,10 secondi.\n2. Calcoliamo l'8%: 59,10 * 0,08 = 4,728 secondi.\n3. Aggiungiamo questo valore al tempo del primo atleta: 59,10 + 4,728 = 63,828 secondi.\n\nQuindi, il tempo massimo entro il quale un atleta deve arrivare per ottenere punti è di 63\"83 (arrotondando al centesimo di secondo).
</details>