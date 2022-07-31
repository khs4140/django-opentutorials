from django.http import HttpRequest, HttpResponse

# redirect : 리다이렉트!!
from django.shortcuts import redirect, render, HttpResponse, redirect


from django.views.decorators.csrf import csrf_exempt


import random

# Create your views here.

next_id = 4

topics = [
    {'id': 1, 'title': 'routing', 'body': 'Routing is ...'},
    {'id': 2, 'title': 'view', 'body': 'View is ...'},
    {'id': 3, 'title': 'model', 'body': 'Model is ...'}]


def HTMLTemplate(articleTag, id=None):
    global topics  # 전역 변수 지정

    contextUI = ''
    if id != None:
        contextUI = f'''<li>
                    <form action='/delete/' method='post'>
                        <input type='submit' value='delete'>
                        <input type='hidden' name='id' value={id}>
                    </form>
                </li>
                <li><a href="/update/{id}">UPDATE</a></li>
                '''
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f"""
    <html>
        <body>
            <h1><a href='/'>Django</a></h1>
            <ol>
                {ol}
            </ol>
            {articleTag}
            <ul>
                <li><a href='/create'>CREATE</a></li>
                {contextUI}
            </ul>
        </body>
    </html>
    """


def index(request):
    article = '''
        <h2>Welcome</h2>
        Hello, Django
    '''

    return HttpResponse(HTMLTemplate(article))

# <id> 꺽쇠로 표시!! < >


def read(request, id):  # <id> => str로 전달
    # topic = topics[int(id)-1]
    global topics

    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2><p>{topic["body"]}</p>'

    return HttpResponse(HTMLTemplate(article, id))


@csrf_exempt  # csrf 면제시키고 싶은 함수에 위에다 붙여줘
def create(request):
    global next_id
    print('request.method : ', request.method)
    if request.method == 'GET':
        article = '''
            <form action='/create/' method='post'>
                <p><input type='text' name='title' placeholder="제목을 입력하세요"></p>
                <p><textarea name='body' placeholder='저장할 텍스트를 입력하세요'></textarea></p>
                <p><input type='submit'></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article))

    elif request.method == 'POST':
        print(request.POST)  # POST 방식으로 들어온 데이터 확인
        title = request.POST['title']
        body = request.POST['body']

        newTopic = {'id': next_id, 'title': title, 'body': body}
        topics.append(newTopic)
        url = '/read/'+str(next_id)
        next_id += 1

        return redirect(url)


@csrf_exempt
def delete(request):
    global topics
    if request.method == 'POST':
        id = request.POST['id']
        print(id)
        newTopic = []

        for topic in topics:
            if topic['id'] != int(id):
                newTopic.append(topic)
        topics = newTopic
        return redirect('/')


@csrf_exempt
def update(request, id):
    global topics
    if request.method == 'GET':
        for topic in topics:
            if topic['id'] == int(id):
                selectedTopic = {
                    "title": topic['title'],
                    'body': topic['body']
                }
        article = f'''
            <form action='/update/{id}/' method='post'>
                <p><input type='text' name='title' value={selectedTopic['title']}></p>
                <p><textarea name='body' placeholder='내용 입력'>{selectedTopic['body']} </textarea></p>
                <p><input type='submit'></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article, id))

    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']

        for topic in topics:
            if topic['id'] == int(id):
                topic['title'] = title
                topic['body'] = body

        return redirect(f'/read/{id}')
