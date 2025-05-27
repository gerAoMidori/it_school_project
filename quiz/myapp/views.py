from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
import random
import os


class Question:
    def __init__(self):
        self.index = 0
        self.score = 0

    def load_information(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return json.loads(content)

    def get_set_of_questions(self, path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        categories_path = os.path.join(base_dir + "\myapp" + "\categories")
        file_path = os.path.join(categories_path, path + ".json")
        questions = self.load_information(file_path)
        question_list = []
        for question in questions:
            answers = random.sample(question["false_one"], 3)
            answers.append(question["answer"])
            random.shuffle(answers)
            question_list.append([question["question"], question["answer"], answers])
        random.shuffle(question_list)
        return question_list

    def get_10_questions(self, path):
        question_list = random.sample(self.get_set_of_questions(path), 10)
        return question_list


class FileManager:
    def __init__(self, path):
        self.path = path

    def load_files_list(self):
        # Get the list of files in the directory categories as a list

        self.file_list = [f[:-5] for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        return self.file_list



class WriteData:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.path = os.path.join(base_dir + "\myapp" + "\\templates\correct.txt" )


    def write_data(self, data):
        with open(self.path, 'r', encoding='utf-8') as f:
            existing_data = f.read()
        print(existing_data)
        with open(self.path, 'w', encoding='utf-8') as f:
            if existing_data.strip() == "":
                f.write(data)
            else:
                f.write(existing_data + "\n" + data)
    def read_data(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            existing_data = f.readlines()
        return existing_data
    def clear_data(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write("")
# My views
def home(request):
    WriteData().clear_data()  # Clear the file at the start of the quiz
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    categories_path = os.path.join(base_dir + "\myapp" + "\categories")
    file_manager = FileManager(categories_path)
    quiz_option = file_manager.load_files_list()  
    return render(request, "index.html", {'quiz_option': quiz_option})


# ...existing code...

# Supprimer ces 3 lignes à la fin du fichier
# categories_path = "categories"
# file_manager = FileManager(categories_path)
# quiz_option = file_manager.load_files_list()

# @csrf_exempt  # facultatif si tu utilises {% csrf_token %}
def quiz(request):
    question_manager = Question()
    if request.method == 'POST':
        quiz_name = request.POST.get('quiz_name')
        if not quiz_name:  # Vérifie si quiz_name est vide
            return redirect('home')

        # Récupérer toutes les questions pour ce quiz
        all_questions = question_manager.get_10_questions(quiz_name)

        # Stocker les questions dans la session
        request.session['questions'] = all_questions
        request.session['quiz_name'] = quiz_name
        request.session['correct_answers'] = []  # Initialiser la liste des réponses correctes
        request.session['score'] = 0
        request.session['question_index'] = 0
        request.session['max_index'] = len(all_questions)
        correct_answers = []
        return redirect('quiz_questions')
    return redirect('home')


def quiz_questions(request):
    question_index = request.session.get('question_index')
    questions = request.session.get('questions')
    quiz_name = request.session.get('quiz_name')
    print(quiz_name)
    if questions is None:
        return redirect('home')  # Redirige si les questions n'existent pas

    if question_index is None:
        question_index = 0  # Initialise à 0 si None

    try:
        question_index = int(question_index)  # S'assure que c'est un entier
    except (ValueError, TypeError):
        return redirect('home')  # Redirige en cas d'erreur

    max_index = request.session.get('max_index')

    if question_index >= max_index:
        return redirect('score')  # Quiz terminé

    question_data = questions[question_index]
    question_text = question_data[0]
    correct_answer = question_data[1]
    answers = question_data[2]
    print("Salut, je suis dans quiz_questions")  # Pour le débogage
    return render(request, 'quiz.html', {
        'question_text': question_text,
        'answers': answers,
        'question_index': question_index,
        'quiz_name': quiz_name,
    })

@csrf_exempt  # facultatif si tu utilises {% csrf_token %}
def submit_answer(request):
    write = WriteData()
    if request.method == 'POST':
        question_index = request.session.get('question_index')
        selected_answer = request.POST.get('answer')
        questions = request.session.get('questions')

        if questions is None:
            return redirect('home')  # Redirige si les questions n'existent pas

        if question_index is None:
            return redirect('home')  # Redirige si question_index n'existe pas

        try:
            question_index = int(question_index)  # S'assure que c'est un entier
        except (ValueError, TypeError):
            return redirect('home')  # Redirige en cas d'erreur

        max_index = request.session.get('max_index')

        if question_index >= max_index:
            return redirect('score')

        selected_answer = request.POST.get('answer')
        correct_answer = questions[question_index][1]

        if selected_answer == correct_answer:
            request.session['score'] = request.session.get('score', 0) + 1
            request.session.modified = True
        else:
        # Incrémenter l'index de la question    
            WriteData().write_data(f'Question {question_index + 1}: {questions[question_index][0]} (::) La reponse était {correct_answer}')
        request.session['question_index'] = question_index + 1
        request.session.modified = True
        return redirect('quiz_questions')
    return redirect('home')


def score(request):
    score = request.session.get('score', 0)
    max_index = request.session.get('max_index', 0)
    information = WriteData().read_data
    print(max_index)  # Pour le débogage
    return render(request, 'score.html', {"score": score, "max_index": max_index, 'information': information})