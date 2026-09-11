from agent import analyze_post


text = """
OpenAI announced a new AI model that can perform advanced
reasoning and assist researchers with scientific tasks.
"""


result = analyze_post(text)

print("\nAI ANALYSIS")
print("=" * 50)
print(result)