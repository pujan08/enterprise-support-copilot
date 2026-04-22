# Enterprise Support Resolution Copilot

An AI-powered support copilot built to handle common SaaS support questions using retrieval, orchestration, evaluation, and cloud deployment.

This project was created as a hands-on learning build to explore how modern AI application components fit together in a realistic workflow. It combines FastAPI, Azure AI Search, LangGraph, LangSmith, Azure AI Foundry, Docker, Azure Container Registry, Azure Container Apps, and a lightweight frontend into one end-to-end system.

## Architecture Diagram

![Enterprise Support Copilot Architecture](screenshots/architecture-diagram.png)

The copilot is designed to answer support questions related to:

- login and account access
- billing and subscriptions
- invitations and permissions
- notifications and email delivery
- performance and slow loading

It does not rely on generic chatbot behavior alone. Instead, it uses a retrieval-based support flow backed by a structured knowledge base, answer-generation rules, graph-based orchestration, evaluation pipelines, and deployed infrastructure.

---

## Live Demo

**Frontend:**  
Add your public frontend URL here

**Backend API:**  
Add your deployed backend URL here

Example deployed endpoints used in this project:

- `/health`
- `/ask`
- `/debug/search`
- `/debug/search-query`

---

## Project Goal

The purpose of this project was to build and deploy a practical AI support system from scratch while learning the full stack of an AI application lifecycle:

- backend API design
- search-based retrieval
- answer shaping
- evaluation workflows
- orchestration with LangGraph
- tracing and dataset evaluation with LangSmith
- agent-service experimentation with Azure AI Foundry
- containerization and Azure deployment
- simple frontend integration

This was not built as a toy chatbot. The aim was to understand how to create a more controlled support assistant that gives grounded answers based on a knowledge base rather than relying entirely on general model responses.

---

## Key Features

### Retrieval-based support answering
The system retrieves relevant support content from Azure AI Search and uses that content to generate support responses. This makes the answers more grounded and consistent than generic model-only outputs.

### Support theme coverage
The current knowledge base is organized around five practical support themes:

- Login and account access
- Billing and subscription
- Invitations and permissions
- Notifications and email delivery
- Performance and slow loading

### Mixed document-style handling
The knowledge base includes both:

- support article style documents
- FAQ-style documents

This made the project more realistic and helped expose retrieval and answer-quality issues that would not appear in a perfectly clean dataset.

### Answer shaping
The system does more than return raw search snippets. It formats answers into a support-friendly shape with:

- a short issue summary
- next steps
- confidence
- source information

### LangGraph orchestration
The backend flow is orchestrated through LangGraph rather than one large function. The graph currently includes:

- search step
- relevance filtering
- conditional routing
- ambiguity-aware post-processing
- no-context fallback
- final response assembly

### Local evaluation pipeline
The project includes a local evaluation runner that checks retrieval and answer quality against a manually curated question set.

### LangSmith integration
The system uses LangSmith for:

- tracing
- dataset-backed evaluation
- custom evaluators
- experiment-style review of system behavior

### Azure AI Foundry foundation
The project includes an Azure AI Foundry setup and a Foundry-side bridge into the real support API, showing how an agent layer can sit in front of an actual product workflow rather than replacing it with generic model output.

### Deployed backend and frontend
The backend is deployed using:

- Docker
- Azure Container Registry
- Azure Container Apps

The frontend is hosted publicly as a static website.

---

## Tech Stack

### Backend
- Python
- FastAPI

### Retrieval and Search
- Azure AI Search

### Orchestration
- LangGraph

### Evaluation and Tracing
- LangSmith

### Agent Layer
- Azure AI Foundry

### Deployment
- Docker
- Azure Container Registry
- Azure Container Apps
- Azure Storage Static Website hosting

### Frontend
- HTML
- CSS
- JavaScript

---

## System Architecture

At a high level, the system works like this:

1. A user submits a support question through the frontend.
2. The frontend sends the question to the FastAPI backend.
3. The backend sends the question into a LangGraph workflow.
4. The graph performs search and relevance filtering against Azure AI Search.
5. If relevant support content exists, the graph builds a support answer.
6. If the retrieval is ambiguous, the answer is post-processed accordingly.
7. If there is no relevant support content, the system returns a no-context response.
8. The final response is returned with:
   - answer
   - next steps
   - confidence
   - primary source
9. LangSmith captures traces and supports evaluation analysis.

---

## Architecture Flow

### User Layer
- User enters a support question

### Frontend Layer
- Static frontend page
- Hosted publicly
- Sends requests to the deployed backend

### Backend Layer
- FastAPI app
- `/ask` endpoint
- `/health` endpoint
- debug endpoints

### Orchestration Layer
- LangGraph workflow
- search node
- filter node
- routing node
- answer node
- ambiguity annotation node
- no-context node
- final response node

### Retrieval Layer
- Azure AI Search
- support documents
- FAQ documents

### Evaluation Layer
- local manual eval runner
- LangSmith dataset + evaluator flow

### Agent / Integration Layer
- Azure AI Foundry
- Foundry-side bridge calling the real `/ask` API

### Deployment Layer
- Docker image
- Azure Container Registry
- Azure Container Apps
- static frontend hosting

---

## Repository Structure

```text
enterprise-support-copilot/
  app/
    __init__.py
    api.py
    answering.py
    config.py
    graph.py
    models.py
    search.py
    services.py
    test_graph.py

  data/
    login-account-access-support.txt
    billing-support.txt
    invitations-permissions-support.txt
    notifications-email-delivery-support.txt
    performance-slow-loading-support.txt
    billing-faq.txt
    login-faq.txt
    invitations-permissions-faq.txt
    notifications-email-faq.txt
    performance-faq.txt

  docs/
    ingestion_plan.md

  eval/
    __init__.py
    manual_questions.json
    load_manual_questions.py
    run_manual_eval.py
    create_langsmith_dataset.py
    prepare_langsmith_dataset.py
    run_langsmith_eval.py
    langsmith_target.py
    langsmith_evaluators.py
    manual_eval_results_latest.json
    manual_eval_results_<timestamp>.json

  foundry/
    __init__.py
    create_agent.py
    run_support_agent.py
    support_bridge.py
    test_agent_response.py
    test_foundry_agent_via_bridge.py
    test_foundry_bridge.py
    test_foundry_connection.py
    test_local_support_api.py

  frontend/
    index.html

  ingestion/

  .env
  .env.example
  .gitignore
  Dockerfile
  requirements.txt
  README.md
