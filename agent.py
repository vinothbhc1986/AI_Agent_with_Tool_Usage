import random
from typing import Any, Dict, List

import requests


class SimpleAgent:
    """Simple beginner-friendly AI agent with a couple of useful tools."""

    def __init__(self):
        self.advice_pool = [
            "Take one small step at a time. Progress is built from steady efforts.",
            "Rest is part of productivity. Give yourself permission to pause and reset.",
            "Focus on what you can control today, and let the rest wait for tomorrow.",
            "Small wins build momentum. Finish the next useful task instead of worrying about everything.",
        ]

    def get_advice(self) -> Dict[str, Any]:
        """Return a helpful piece of advice, using a public API when available."""
        try:
            response = requests.get("https://api.adviceslip.com/advice", timeout=10)
            response.raise_for_status()
            payload = response.json()
            advice = payload.get("slip", {}).get("advice")
            if advice:
                return {"advice": advice, "source": "adviceslip.com"}
        except Exception:
            pass

        advice = random.choice(self.advice_pool)
        return {"advice": advice, "source": "fallback"}

    def search_books(self, query: str, max_results: int = 3) -> Dict[str, Any]:
        """Search books using the Google Books API with a fallback list for offline use."""
        normalized = (query or "").strip()
        if not normalized:
            normalized = "programming"

        try:
            response = requests.get(
                "https://www.googleapis.com/books/v1/volumes",
                params={"q": normalized, "maxResults": max_results},
                timeout=10,
            )
            response.raise_for_status()
            payload = response.json()
            items = payload.get("items", [])
            books = []
            for item in items[:max_results]:
                info = item.get("volumeInfo", {})
                books.append(
                    {
                        "title": info.get("title", "Unknown title"),
                        "authors": info.get("authors", ["Unknown author"]),
                        "preview_link": info.get("previewLink"),
                    }
                )
            if books:
                return {"query": normalized, "books": books, "source": "google-books"}
        except Exception:
            pass

        fallback_books = {
            "machine learning": [
                {"title": "Hands-On Machine Learning", "authors": ["Aurélien Géron"], "preview_link": None},
                {"title": "Deep Learning", "authors": ["Ian Goodfellow", "Yoshua Bengio", "Aaron Courville"], "preview_link": None},
                {"title": "The Hundred-Page Machine Learning Book", "authors": ["Andriy Burkov"], "preview_link": None},
            ],
            "programming": [
                {"title": "Clean Code", "authors": ["Robert C. Martin"], "preview_link": None},
                {"title": "The Pragmatic Programmer", "authors": ["Andrew Hunt", "David Thomas"], "preview_link": None},
                {"title": "Python Crash Course", "authors": ["Eric Matthes"], "preview_link": None},
            ],
        }

        books = fallback_books.get(normalized.lower(), fallback_books["programming"])[:max_results]
        return {"query": normalized, "books": books, "source": "fallback"}

    def call_agent(self, message: str) -> Dict[str, Any]:
        """Handle a user message by choosing the best available tool."""
        user_message = (message or "").strip()
        if not user_message:
            return {
                "answer": "Please tell me what you need help with.",
                "used_tool": None,
                "tool_result": None,
            }

        lower_message = user_message.lower()
        book_keywords = [
            "book",
            "books",
            "author",
            "novel",
            "read",
            "recommend",
            "fiction",
            "nonfiction",
            "machine learning",
            "python",
            "programming",
        ]

        if any(keyword in lower_message for keyword in book_keywords):
            query = user_message
            if "about" in lower_message:
                query = lower_message.split("about", 1)[1].strip()
            elif any(prefix in lower_message for prefix in ["find books", "search for books", "recommend books"]):
                query = lower_message.replace("find books", "").replace("search for books", "").replace("recommend books", "").strip()
            if not query or query.lower() in {"books", "book"}:
                query = "programming"

            result = self.search_books(query)
            books = result.get("books", [])
            if not books:
                answer = "I couldn't find any books matching that request right now. Try a broader topic such as 'machine learning' or 'programming'."
            else:
                book_lines = [
                    f"- {book['title']} by {', '.join(book['authors'])}"
                    for book in books
                ]
                answer = (
                    f"Here are some books related to '{result['query']}':\n"
                    + "\n".join(book_lines)
                )
            return {"answer": answer, "used_tool": "search_books", "tool_result": result}

        advice = self.get_advice()
        answer = f"Here is some advice: {advice['advice']}"
        return {"answer": answer, "used_tool": "get_advice", "tool_result": advice}
