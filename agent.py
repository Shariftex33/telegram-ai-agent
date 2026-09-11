import ollama
from ddgs import DDGS


MODEL = "qwen2.5:3b"


# --------------------------------
# Web Search Tool
# --------------------------------
def web_search(query, max_results=5):

    try:
        results = DDGS().text(
            query,
            max_results=max_results
        )

        if not results:
            return "No web search results found."

        search_text = ""

        for result in results:
            title = result.get("title", "")
            body = result.get("body", "")
            url = result.get("href", "")

            search_text += f"""
Title: {title}
Information: {body}
URL: {url}

"""

        return search_text

    except Exception as e:
        return f"Web search error: {e}"


# --------------------------------
# Main AI Agent
# --------------------------------
def analyze_post(text):

    print("\n")
    print("=" * 60)
    print("AI AGENT")
    print("=" * 60)

    print(f"Model: {MODEL}")
    print(f"User message: {text}")

    # --------------------------------
    # Ask Qwen whether web search
    # is necessary
    # --------------------------------

    print("\nThinking...")
    print("Checking whether a tool is needed...")

    decision_prompt = f"""
You are a helpful AI assistant.

Decide whether the user's question requires current information
from the internet.

Answer ONLY:
YES
or
NO

Use YES for things such as:
- current news
- today's information
- latest information
- current prices
- current political information
- current weather
- recent events
- information that may have changed recently

Use NO for:
- general knowledge
- explanations
- programming questions
- mathematics
- casual conversation
- writing requests

User message:
{text}
"""

    decision_response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": decision_prompt
            }
        ]
    )

    decision = decision_response["message"]["content"].strip().upper()

    # --------------------------------
    # Tool Selection
    # --------------------------------

    if "YES" in decision:

        print("\nTOOL DECISION: WEB SEARCH")
        print("-" * 60)

        print("Searching the web...")

        search_results = web_search(text)

        print("Web search completed.")

        # Count approximate number of results
        result_count = search_results.count("Title:")

        print(f"Results found: {result_count}")

        print("\nWEB SEARCH RESULTS")
        print("-" * 60)
        print(search_results)

        # --------------------------------
        # Give search results to Qwen
        # --------------------------------

        print("\nSending search results to Qwen...")
        print("Generating final answer...")

        prompt = f"""
You are a helpful AI assistant.

Answer the user's question naturally and clearly.

Use the web search results below to answer the question.
Prefer information from the search results when answering
questions about current events.

Do not use a fixed format such as SUMMARY, TOPIC,
IMPORTANT, or RELEVANCE.

If useful, mention the source URLs at the end.

User question:
{text}

Web search results:
{search_results}
"""

    else:

        print("\nTOOL DECISION: NO TOOL")
        print("-" * 60)

        print("Web search is not needed.")
        print("Generating final answer with Qwen...")

        # --------------------------------
        # Normal Qwen answer
        # --------------------------------

        prompt = f"""
You are a helpful AI assistant.

Answer the user's message naturally and directly.

Do not use a fixed format.
Do not automatically summarize or analyze the message.

If the user asks a question, answer it.
If the user asks for an explanation, explain it clearly.
If the user asks for code, provide simple code.
If the user asks for advice, give useful advice.

User message:
{text}
"""

    # --------------------------------
    # Final Qwen Response
    # --------------------------------

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"]

    # --------------------------------
    # Runtime Result
    # --------------------------------

    print("\n")
    print("=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)
    print(answer)
    print("=" * 60)

    return answer