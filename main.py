from ollama import Client
from pydantic import BaseModel

client = Client(
    host= "https://ollama.com",
    headers={"Authorization": "Bearer 5506147938074c458450e9f8b1d1ee98.sqR_YTTRWMtG1pHd8VgA-hol"},
)

SYSTEM_PROMPT = """You are a good problem solver, which views the image and answers the problem based on that image. 
You can help related to electrical errors, homework and other problems.

CRITICAL REQUIREMENT: You must respond ONLY with a raw JSON object matching this schema. Do not include any conversational text, headers, or markdown wrapper tags like ```json.
{
  "problem": "string description",
  "possible_cause": "string description",
  "action": ["string action 1", "string action 2"],
  "safety": "string description"
}"""


CONTEXT = input("Enter your problem: ")
path = r"E:\Problem_solver\problem.jpg"

class ProblemSolver(BaseModel):
    problem: str
    possible_cause: str
    action: list[str]
    safety: str

response = client.chat(
    model='gemma4:31b-cloud',
    format=ProblemSolver.model_json_schema(),
    messages=[
        {
            'role' : 'system',
            'content' : SYSTEM_PROMPT,
        },
        {
            'role' : 'user',
            'content' : CONTEXT,
            'images' : [path],
        }
    ],
    options={'temperature' : 0}
)

Solved = ProblemSolver.model_validate_json(response['message']['content'])

print("\nImage Analysis Results:")
print("-" * 50)
print(f"\nProblem:\n{Solved.problem}")
print(f"\npossible_cause: {Solved.possible_cause}")
print("\nActions which can be taken:")
for obj in Solved.action:
    print(obj)
print(f"\nSafety:\n{Solved.safety}")

print("HI:)")
#Why is the circuit not working?