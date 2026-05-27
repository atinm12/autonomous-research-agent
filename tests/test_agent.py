from agent.core import ResearchAgent


agent = ResearchAgent()

query = "Give me a company profile for Microsoft"

result = agent.run(query)

print("\nFINAL RESULT:")
print(result)