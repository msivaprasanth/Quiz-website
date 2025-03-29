from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import mysql.connector
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = 'Luffy'

# Ensure the static directory exists
if not os.path.exists('static'):
    os.makedirs('static')

# Connect to the MySQL database
mydb = mysql.connector.connect(host="localhost", user="root", password="admin", db="quiz_app")
cursor = mydb.cursor()

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

# Start Quiz Route
@app.route('/start_quiz', methods=['POST', 'GET'])
def start_quiz():
    cursor.execute("SELECT * FROM Questions ORDER BY RAND() LIMIT 15")
    questions = cursor.fetchall()

    # Store questions in session
    session['questions'] = questions
    session['current_index'] = 0
    session['user_answers'] = []
    session.modified = True  # Ensures that the session is saved

    return render_template('quiz.html', question=questions[0], index=0)

# Next Question AJAX Route
@app.route('/next_question', methods=['POST'])
def next_question():
    data = request.json
    selected_option = data['selected_option']
    current_index = session.get('current_index', 0)

    # Save the answer
    session['user_answers'].append(selected_option)
    session['current_index'] = current_index + 1
    session.modified = True

    # Check if there are more questions
    if current_index + 1 < len(session['questions']):
        question = session['questions'][current_index + 1]
        return jsonify(finished=False, question=question)
    else:
        return jsonify(finished=True)

# Submit Route
@app.route('/submit_quiz', methods=['POST', 'GET'])
def submit_quiz():
    user_answers = session.get('user_answers', [])
    questions = session.get('questions', [])

    # Calculate score
    score = sum(1 for i, q in enumerate(questions) if str(user_answers[i]).strip() == str(q[6]).strip())

    # Generate Performance Graph
    labels = [f"Q{i + 1}" for i in range(len(questions))]
    correct_answers = [1 if str(user_answers[i]).strip() == str(questions[i][6]).strip() else 0 for i in range(len(questions))]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, correct_answers, color='skyblue')
    plt.axhline(y=0.5, color='r', linestyle='--', label='Passing Mark')
    plt.title('Quiz Performance')
    plt.xlabel('Questions')
    plt.ylabel('Correctness (1 = Correct, 0 = Incorrect)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    # Save the graph as an image
    performance_graph_path = os.path.join('static', 'performance.png')
    plt.savefig(performance_graph_path)
    plt.close()  # Close the figure

    return redirect(url_for('result', score=score))

# Result Route
@app.route('/result', methods=['POST', 'GET'])
def result():
    score = request.args.get('score', 0)
    return render_template('result.html', score=score)

if __name__ == '__main__':
    app.run(debug=True)
