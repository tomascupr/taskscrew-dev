from flask import Flask, jsonify
from crewai import Agent, Task, Crew
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "CrewAI is deployed successfully."})

@app.route('/run-crew')
def run_crew():
    agent = Agent(
        role="Researcher",
        goal="Summarize AI startup trends",
        backstory="Expert AI researcher with extensive knowledge of current market trends.",
        verbose=True
    )

    task = Task(
        description="List the top AI trends for 2025",
        expected_output="A concise summary of the top 5 AI startup trends anticipated for the year 2025.",
        agent=agent
    )

    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = crew.kickoff()

    # FIX: Convert CrewOutput to a JSON-friendly format explicitly
    return jsonify({"result": str(result)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)