import os
from dotenv import load_dotenv
from ollama import Client
from pydantic import BaseModel
from tkinter import filedialog

load_dotenv()

Image_input = None

def get_image():
    global Image_input
    Image_input = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
    )

SECRET_KEY = os.getenv("PROBLEM_SOLVER_KEY")

client = Client(
    host= "https://ollama.com",
    headers={"Authorization": f"Bearer {SECRET_KEY}"},
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

while True:
    CONTEXT = input("Enter your problem (or q to exit): ")
    if CONTEXT == 'q':
        break
    get_image()
    path = Image_input

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

#Why is the circuit not working?