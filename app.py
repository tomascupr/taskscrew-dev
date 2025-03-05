from flask import Flask, jsonify
from crewai import Agent, Task, Crew

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "CrewAI with Brand Book PDF deployed."})

@app.route('/run-crew')
def run_crew():
    # Load brand book PDF once and share with all agents via crew knowledge
    brand_book_knowledge = PDFLoader(pdf_path="brand_book.pdf")

    brand_manager = Agent(
        role="Brand Manager",
        goal="Ensure brand consistency according to the brand book PDF.",
        backstory="Expert brand manager deeply familiar with brand guidelines provided in PDF.",
        verbose=True
    )

    copywriter = Agent(
        role="Copywriter",
        goal="Write compelling and engaging social media posts about great food.",
        backstory="Creative and experienced digital copywriter.",
        verbose=True
    )

    mom = Agent(
        role="Mom Expert",
        goal="Ensure content deeply resonates with moms.",
        backstory="Experienced mother understanding the nuances of engaging the mom audience.",
        verbose=True
    )

    brand_task = Task(
        description="Extract key messaging, brand voice, and style guidelines from the brand book PDF.",
        expected_output="Concise guidelines extracted from the brand book.",
        agent=brand_manager
    )

    copywriting_task = Task(
        description="Create a social media post promoting great food following brand guidelines provided by the Brand Manager.",
        expected_output="An engaging, concise, and brand-consistent social media post.",
        agent=copywriter,
        context=[brand_task]
    )

    mom_task = Task(
        description="Review and optimize the social media post to resonate strongly with moms.",
        expected_output="Final optimized social media post appealing to moms.",
        agent=mom,
        context=[copywriting_task]
    )

    crew = Crew(
        agents=[brand_manager, copywriter, mom],
        tasks=[brand_task, copywriting_task, mom_task],
        verbose=True
    )

    result = crew.kickoff()

    return jsonify({"result": str(result)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)