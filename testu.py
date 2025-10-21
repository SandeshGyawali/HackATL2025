from app.crews.product_crew import ProductCrew


def main():
    # Instantiate the crew
    crew = ProductCrew()

    # Define the user query
    query = "tell me cost breakdown for nasa lunar rover"

    # Run the analysis
    result = crew.analyze_query(query)

    # Print the result
    print("\n=== Crew Result ===")
    print(result)


if __name__ == "__main__":
    main()
