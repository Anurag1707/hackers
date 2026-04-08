#!/bin/bash

# Start FastAPI in background
uvicorn inference:app --host 0.0.0.0 --port 8000 &

# Start Streamlit on main port (7860)
streamlit run app.py --server.port 7860 --server.address 0.0.0.0