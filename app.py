from flask import Flask, jsonify
from crewai import Agent, Task, Crew
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "CrewAI deployed successfully"})

@app.route('/run-crew')
def run_crew():
    research_agent = Agent(
        role="Researcher",
        goal="Provide AI startup trends summary",
        backstory="Skilled researcher with deep knowledge in AI market.",
        verbose=True
    )

    task = Task(
        description="List and summarize the most promising AI startups and trends for 2025.",
        agent=research_agent
    )

    crew = Crew(agents=[research_agent], tasks=[task], verbose=True)
    result = crew.kickoff()

    return jsonify({"result": result})
#test 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)