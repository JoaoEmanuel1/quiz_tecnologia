#Importações e configuracoes básicas
from flask import Flask, render_template, request, redirect, url_for, session
from questions import questions
import random

app = Flask(__name__)
app.secret_key = '427623'

# renderiza a página inicial 
@app.route('/')
def home():
    return render_template('index.html')

# Inicia o quiz
@app.route('/start')
def start():

    # embaralha as perguntas quando inicia
    session['question_order'] = random.sample(range(len(questions)), len(questions))
    session['current_question'] = 0
    session['score'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():

    # verificar se o quiz terminou
    current_q = session['current_question']
    if current_q >= len(questions):
        return redirect(url_for('results'))
    
    # recebe a pergunta atual
    question_data = questions[session['question_order'][current_q]]
    
    return render_template('quiz.html', 
                         question=question_data['question'],
                         options=question_data['options'],
                         current=current_q + 1,
                         total=len(questions))

@app.route('/check', methods=['POST'])
def check():

    #recebe a resposta do usuário
    selected_option = request.form.get('option')
    current_q = session['current_question']
    question_data = questions[session['question_order'][current_q]]
    
    # verifica se a resposta está correta
    if selected_option == question_data['answer']:
        session['score'] += 1
    
    # avança para a próxima pergunta
    session['current_question'] += 1
    
    return redirect(url_for('quiz'))

@app.route('/results')
def results():
    # Recupera o resultado final e mostra na tela
    score = session['score']
    total = len(questions)
    
    session.clear()
    
    return render_template('results.html', score=score, total=total)

if __name__ == '__main__':
    app.run(debug=True)