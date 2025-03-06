from flask import Flask, jsonify
from crewai import Agent, Task, Crew

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "CrewAI deployed successfully."})

@app.route('/run-crew')
def run_crew():
    brand_manager = Agent(
        role="Brand Manager",
        goal="Provide clear brand guidelines based on predefined standards.",
        backstory="Expert in brand management.",
        verbose=True
    )

    copywriter = Agent(
        role="Copywriter",
        goal="Craft engaging social media posts.",
        backstory="Experienced creative copywriter.",
        verbose=True
    )

    mom = Agent(
        role="Mom Expert",
        goal="Ensure the message resonates deeply with moms.",
        backstory="Insightful mom familiar with audience expectations.",
        verbose=True
    )

    brand_task = Task(
        description="Summarize brand guidelines clearly.",
        expected_output="Brand voice and style guidelines.",
        agent=brand_manager
    )

    copywriting_task = Task(
        description="Write engaging social media post.",
        expected_output="Social media post text.",
        agent=copywriter,
        context=[brand_task]
    )

    mom_task = Task(
        description="Optimize social media post to resonate with moms.",
        expected_output="Optimized social media post.",
        agent=mom,
        context=[copywriting_task]
    )

    crew = Crew(
        agents=[brand_manager, copywriter, mom],
        tasks=[brand_task, copywriting_task, mom_task],
        memory=True,  # enables conversation memory
        verbose=True
    )

    result = crew.kickoff()

    # Access internal conversation history explicitly
    conversation_logs = crew.memory.export_memory()

    return jsonify({
        "result": str(result),
        "conversation_logs": conversation_logs
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)