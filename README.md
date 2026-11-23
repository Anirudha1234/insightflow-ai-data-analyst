# InsightFlow — AI Data Analyst Agent

**Ask questions about your business data in natural language and get SQL-powered answers, business insights, calculations, and interactive charts.**

InsightFlow is an AI-powered data analyst application that converts natural-language questions into SQL queries, executes them against a PostgreSQL database, analyzes the results, and generates business insights using Google Gemini and LangGraph.

## Features

- **Natural Language to SQL:** Ask business questions in plain English.
- **AI-Powered Insights:** Generate business summaries and actionable findings using Google Gemini.
- **SQL Validation:** Validate generated SQL before execution, with restrictions on query types, tables, and dangerous operations.
- **Read-Only Database Access:** Execute analytical queries through a restricted PostgreSQL database role.
- **Python Data Analysis:** Generate descriptive statistics and analyze query results using Pandas and NumPy.
- **Business Calculations:** Calculate metrics such as average order value, revenue growth, percentages, and profit metrics when the required data is available.
- **Interactive Visualizations:** Generate Plotly charts and display them inside the React dashboard.
- **LangGraph Workflow:** Coordinate SQL generation, execution, analysis, calculations, chart generation, and answer generation.
- **FastAPI Backend:** Expose the analysis workflow through REST APIs.
- **React Dashboard:** Interactive interface with Markdown-rendered insights, query results, and formatted SQL.

## Architecture

```text
              React + Vite
                   |
                   | Axios
                   v
               FastAPI
                   |
                   v
             LangGraph Agent
                   |
       +-----------+------------+
       |           |            |
       v           v            v
   Gemini       PostgreSQL    Python Tools
       |           |            |
  SQL Generation  SQL       Analysis
  Answer Generation Validation Calculations
                  Execution   Charts
                   |
                   v
             Analysis Results
                   |
                   v
             React Dashboard
```

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, Vite, Axios |
| UI and Visualization | Recharts, Plotly, Lucide React |
| AI / LLM | Google Gemini |
| Agent Framework | LangGraph, LangChain |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| Data Analysis | Pandas, NumPy |
| SQL Validation | SQLGlot |
| Database Connectivity | SQLAlchemy, Psycopg |
| Deployment | Docker |

## Project Structure

```text
insightflow-ai-data-analyst/
│
├── app/
│   ├── agents/
│   │   ├── analysis_nodes.py
│   │   ├── calculator_nodes.py
│   │   ├── chart_nodes.py
│   │   ├── error_handler.py
│   │   ├── graph.py
│   │   ├── nodes.py
│   │   └── state.py
│   │
│   ├── api/
│   │   └── schemas.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── schema_context.py
│   │
│   ├── services/
│   │   ├── gemini_client.py
│   │   └── sql_generator.py
│   │
│   ├── tools/
│   │   ├── calculator.py
│   │   ├── chart_generator.py
│   │   ├── python_analyzer.py
│   │   ├── sql_executor.py
│   │   └── sql_validator.py
│   │
│   └── main.py
│
├── database/
│   ├── schema.sql
│   └── seed_data.sql
│
├── data/
│   └── Generated chart files
│
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── .env
│   └── package.json
│
├── test_agent.py
├── test_analysis_node.py
├── test_calculator.py
├── test_calculator_node.py
├── test_chart_decision.py
├── test_chart_generator.py
├── test_chart_node.py
├── test_gemini.py
├── test_integrated_analysis.py
├── test_python_analyzer.py
├── test_sql_executor.py
├── test_sql_generator.py
├── test_sql_validator.py
│
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
└── .dockerignore
```

## Database

InsightFlow uses PostgreSQL with the following tables:

- `customers`
- `products`
- `orders`
- `order_items`
- `payments`
- `returns`
- `inventory`

The project includes SQL scripts for creating the database schema and populating synthetic business data.

## Getting Started

### Prerequisites

- Python
- Node.js and npm
- PostgreSQL
- Google Gemini API key
- Docker (for containerized backend execution)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/insightflow-ai-data-analyst.git

cd insightflow-ai-data-analyst
```

### 2. Set up PostgreSQL

Create a PostgreSQL database named:

```sql
CREATE DATABASE insightflow_db;
```

Run the schema and seed scripts:

```bash
psql -U postgres -d insightflow_db -f database/schema.sql

psql -U postgres -d insightflow_db -f database/seed_data.sql
```

Configure the database credentials in your environment file.

### 3. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Configure:

- Gemini API key and model.
- PostgreSQL host, port, database name, username, and password.
- Read-only PostgreSQL username and password.

Never commit `.env` or expose API credentials.

### 4. Install backend dependencies

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```cmd
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 5. Start the backend

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

### 6. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
```

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

Start the development server:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## Docker Backend

Build the Docker image from the project root:

```bash
docker build -t insightflow-ai-analyst .
```

Run the container:

```bash
docker run -d \
  --name insightflow-api \
  -p 8000:8000 \
  --env-file .env \
  -e DB_HOST=host.docker.internal \
  insightflow-ai-analyst
```

Check container logs:

```bash
docker logs insightflow-api
```

The database must be reachable from the Docker container.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API health |
| POST | `/analyze` | Analyze business data |
| GET | `/charts/{filename}` | Retrieve a generated chart |

### Example API Request

`POST /analyze`

```json
{
  "question": "Show the top 5 products by delivered revenue in 2025"
}
```

The response includes:

- Original question
- AI-generated business insights
- Generated SQL query
- Query results
- Calculations
- Chart information
- Execution status and errors, when applicable

## Example Questions

Try asking InsightFlow:

1. Show the top 5 products by delivered revenue in 2025.
2. Show monthly delivered revenue for 2025 as a line chart.
3. Compare delivered revenue across years.
4. Which product category contributes the most revenue?
5. Calculate the average order value.
6. Show the distribution of orders by status.

## Security Considerations

- SQL queries are validated before execution.
- Only permitted SELECT queries and database tables are allowed.
- A restricted PostgreSQL role is used for analytical queries.
- Database statement timeouts and result-row limits are configured.
- Environment files containing credentials must not be committed.

These controls reduce risk but should not be considered a substitute for a full production security review.

## Current Limitations

- The project uses synthetic business data.
- Currency is not defined in the sample database schema, so monetary values are displayed without assuming a currency.
- Revenue calculations depend on the available order and order-item data.
- Profit metrics require actual cost information.
- The application currently supports the configured database schema and analytical workflow.

## Future Improvements

- Deploy the frontend and backend to cloud hosting.
- Integrate hosted PostgreSQL.
- Add user authentication and role-based access.
- Add downloadable reports.
- Improve chart and dashboard customization.
- Add automated evaluation of generated SQL and AI insights.

## License

This project is available under the MIT License.
