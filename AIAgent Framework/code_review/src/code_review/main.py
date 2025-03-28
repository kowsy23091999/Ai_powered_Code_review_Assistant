from code_review.crew import CodeReview

if __name__ == "__main__":
    print("🚀 Starting Code Review Crew...")

    # Create Crew instance
    crew = CodeReview().crew()

    # Example code snippet to analyze
    code_snippet = """
    def add_numbers(a, b):
        return a + b
    print(add_numbers(5))
    """

    # ✅ Pass the code snippet as input
    results = crew.kickoff(inputs={"code_snippet": code_snippet})

    print("\n🔹 Code Review Results:")
    print(results)
