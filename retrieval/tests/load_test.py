import sys
import time
import random  # <-- required
from pathlib import Path
import threading

import psutil
from dotenv import load_dotenv
from locust import User, task, between, events

# ---------------------------------------------------------
# Environment setup
# ---------------------------------------------------------

load_dotenv()

# tests/ → retrieval/ → (project root)
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from agents.workflow.main import app  # your RAG app


# ---------------------------------------------------------
# Test queries
# ---------------------------------------------------------

TEST_QUERIES = [
    "how to check for students tested on 10/8/2024",
    "how to check for low tdtk by Event Name as 'PSAT 8/9 Fall 2024 primary'",
]


# ---------------------------------------------------------
# Locust User
# ---------------------------------------------------------

MAX_REQUESTS_PER_USER = 100
TOTAL_USERS = 5  # for reference

class RAGUser(User):
    """
    Non-HTTP Locust user for load testing the RAG pipeline.
    """
    wait_time = between(2, 5)

    def on_start(self):
        self.request_count = 0

    @task
    def test_rag_query(self):
        if self.request_count >= MAX_REQUESTS_PER_USER:
            # Check if all users are done
            users_done = all(
                getattr(u, "request_count", 0) >= MAX_REQUESTS_PER_USER
                for u in self.environment.runner.user_classes.get(self.__class__, [])
            )
            if users_done:
                print("All users completed max requests. Stopping Locust.")
                self.environment.runner.quit()
            return

        query = random.choice(TEST_QUERIES)
        start_time = time.time()

        try:
            initial_state = {
                "question": query,
                "answer": "",
                "retrieved_documents": "",
                "iteration": 0,
                "vectorstore": None
            }

            result = app.invoke(initial_state)

            latency_ms = (time.time() - start_time) * 1000
            memory_mb = psutil.Process().memory_info().rss / 1024 ** 2

            if not result or not result.get("answer"):
                raise ValueError("Empty answer returned from RAG pipeline")

            events.request.fire(
                request_type="RAG",
                name="app.invoke",
                response_time=latency_ms,
                response_length=len(str(result)),
                exception=None
            )

            print(
                f"[SUCCESS] {latency_ms:.2f} ms | "
                f"Memory: {memory_mb:.1f} MB | "
                f"Query: {query}"
            )

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000

            events.request.fire(
                request_type="RAG",
                name="app.invoke",
                response_time=latency_ms,
                response_length=0,
                exception=e
            )

            print(
                f"[ERROR] {latency_ms:.2f} ms | "
                f"Error: {str(e)} | "
                f"Query: {query}"
            )

        finally:
            self.request_count += 1
