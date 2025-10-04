from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from QandA.models import *
from django.db import connection
import datetime


username_global = None
userid_global = None
# Create your views here.


def home(request):
    if ('login_status' not in request.COOKIES):
        return redirect('/login')
    global userid_global
    userid_global = request.COOKIES['userid']
    global username_global
    username_global = request.COOKIES['username']
    print("inside home", userid_global)
    if (request.method == 'POST'):
        tags = request.POST.get('tag')
        tags = tags.split()
        print(tags)
        template = loader.get_template('posts.html')
        content = []
        for tag in tags:
            with connection.cursor() as cursor:
                # cursor.execute(f"select title,body from posts where tags")
                # select post_id,count(post_id) from votes group by post_id limit 10000;
                cursor.execute(f'''
                select posts.id as id, posts.title as title,posts.body as body,posts.tags as tags,v.count as count, posts.owner_display_name as oname, posts.creation_date cdate, posts.last_edit_date as ldate, posts.last_editor_display_name as lname
                from posts,v 
                where posts.id=v.post_id and posts.tags ~* '.*{tag}.*' and post_type_id=1;
                ''')
                ques = cursor.fetchall()

                for (id, title, que, tags, count, oname, cdate, ldate, lname) in ques:
                    if (oname != None and cdate != None and ldate != None):
                        c = '<h3>'+title+'</h3>'+'<br>'+f'<div id="upvotes">(upvotes:{count})</div>'+f'(Post by <b>{oname}</b>)'+f'(Posted on <b>{cdate}</b>)'+f'(Last edited on <b>{ldate}</b>)'+'<br>'+'<u><b>Question:</b></u>' + \
                            f'<b>{que}</b><br>'+f'<a href="/question/{id}" class="link-primary"><button type="submit" class="btn btn-primary btn-lg" style="padding-left: 2.5rem; padding-right: 2.5rem;" name="">View Answers</button></a><hr>'
                    else:
                        c = '<h3>'+title+'</h3>'+'<br>'+f'<div id="upvotes">(upvotes:{count})</div>'+'<br>'+'<u><b>Question:</b></u>'+f'<b>{que}</b><br>' + \
                            f'<a href="/question/{id}" class="link-primary"><button type="submit" class="btn btn-primary btn-lg" style="padding-left: 2.5rem; padding-right: 2.5rem;" name="">View Answers</button></a><hr>'

                    content.append(c)

            if ('sortbyupvote' in request.POST):
                print("sorting by upvotes")
                content.sort(key=lambda x: x[3], reverse=True)
            if ('sortbyuptime' in request.POST):
                print("sorting by time")
                content.sort(key=lambda x: x[5], reverse=True)

            return HttpResponse(template.render({'content': content}, request))

    content = []
    with connection.cursor() as cursor:
        cursor.execute(f'''
                select posts.id as id, posts.title as title,posts.body as body,posts.tags as tags,v.count as count, posts.owner_display_name as oname, posts.creation_date cdate, posts.last_edit_date as ldate, posts.last_editor_display_name as lname
                from posts,v 
                where posts.id=v.post_id and posts.owner_user_id={userid_global} and posts.post_type_id=1;
                ''')
        ques = cursor.fetchall()

        for (id, title, que, tags, count, oname, cdate, ldate, lname) in ques:
            if (oname != None and cdate != None and ldate != None):
                c = '<h3>'+title+'</h3>'+'<br>'+f'<div id="upvotes">(upvotes:{count})</div>'+f'(Posted on <b>{cdate}</b>)'+f'(Last edited on <b>{ldate}</b>)'+'<br>'+'<u><b>Question:</b></u>'+f'<b>{que}</b><br>'+f'<a href="/question/{id}" class="link-primary"><button type="submit" class="btn btn-primary btn-lg" style="padding-left: 2.5rem; padding-right: 2.5rem;" name="">View Answers</button></a>' + \
                    f'<a href="/edit/{id}" class="link-primary"><button type="submit" class="btn btn-primary btn-lg" style="padding-left: 2.5rem; padding-right: 2.5rem;" name="">Edit</button></a>' + \
                    f'<a href="/delete/{id}"><button type="submit" class="btn btn-danger btn-lg" style="padding-left: 2.5rem; padding-right: 2.5rem;" name="post">Delete</button></a>"'+'<hr>'

            else:
                c = '<h3>'+title+'</h3>'+'<br>'+f'<div id="upvotes">(upvotes:{count})</div>'+'<br>'+'<u><b>Question:</b></u>'+f'<b>{que}</b><br>'+f'<a href="/question/{id}" class="link-primary"><button type="submit" class="btn btn-primary btn-lg" style="padding-left: 2.5rem; padding-right: 2.5rem;" name="">View Answers</button></a>' + \
                    f'<a href="/edit/{id}" class="link-primary"><button type="submit" class="btn btn-primary btn-lg" style="padding-left: 2.5rem; padding-right: 2.5rem;" name="">Edit</button></a>' + \
                    f'<a href="/delete/{id}"><button type="submit" class="btn btn-danger btn-lg" style="padding-left: 2.5rem; padding-right: 2.5rem;" name="post">Delete</button></a>"'+'<hr>'

            content.append(c)

        cursor.execute(f'''
                select posts.id as id, posts.title as title,posts.body as body,posts.tags as tags,v.count as count, posts.owner_display_name as oname, posts.creation_date cdate, posts.last_edit_date as ldate, posts.last_editor_display_name as lname
                from posts,v 
                where posts.id=v.post_id and posts.owner_user_id={userid_global} and posts.post_type_id=2;
                ''')
        posts = cursor.fetchall()

        template = loader.get_template('home.html')

        for (id, title, body, tags, count, oname, cdate, ldate, lname) in posts:
            if (title == None):
                if (lname != None):
                    c = f'<div id="upvotes">(upvotes:{count})</div>'+f'(Posted on <b>{cdate}</b>)'+f'(Last edited by <b>{lname}</b>)'+'<br>'+f'<div>{str(body)}</div>'+f'<a href="/edit/{id}" class="link-primary"><button type="submit" class="btn btn-primary btn-lg" style="padding-left: 2.5rem; padding-right: 2.5rem;" name="">Edit</button></a>' + \
                        f'<a href="/delete/{id}"><button type="submit" class="btn btn-danger btn-lg" style="padding-left: 2.5rem; padding-right: 2.5rem;" name="post">Delete</button></a>"'+'<hr>'
                else:
                    c = f'<div id="upvotes">(upvotes:{count})</div>'+f'(Posted on <b>{cdate}</b>)'+'<br>'+f'<div>{str(body)}</div>'+f'<a href="/edit/{id}" class="link-primary"><button type="submit" class="btn btn-primary btn-lg" style="padding-left: 2.5rem; padding-right: 2.5rem;" name="">Edit</button></a>' + \
                        f'<a href="/delete/{id}"><button type="submit" class="btn btn-danger btn-lg" style="padding-left: 2.5rem; padding-right: 2.5rem;" name="post">Delete</button></a>"'+'<hr>'
            else:
                if (lname != None):
                    c = '<b>'+str(title)+'</b>'+'<br>'+f'<div id="upvotes">(upvotes:{count})</div>'+f'(Posted on <b>{cdate}</b>)'+f'(Last edited by <b>{lname}</b>)'+'<br>'+f'<div>{str(body)}</div><br>' + \
                        f'<a href="/edit/{id}" class="link-primary"><button type="submit" class="btn btn-primary btn-lg" style="padding-left: 2.5rem; padding-right: 2.5rem;" name="">Edit</button></a>' + \
                        f'<a href="/delete/{id}"><button type="submit" class="btn btn-danger btn-lg" style="padding-left: 2.5rem; padding-right: 2.5rem;" name="post">Delete</button></a>"'+'<hr>'
                else:
                    c = '<b>'+str(title)+'</b>'+'<br>'+f'<div id="upvotes">(upvotes:{count})</div>'+f'(Posted on <b>{cdate}</b>)'+'<br>'+f'<div>{str(body)}</div><br>'+f'<a href="/edit/{id}" class="link-primary"><button type="submit" class="btn btn-primary btn-lg" style="padding-left: 2.5rem; padding-right: 2.5rem;" name="">Edit</button></a>' + \
                        f'<a href="/delete/{id}"><button type="submit" class="btn btn-danger btn-lg" style="padding-left: 2.5rem; padding-right: 2.5rem;" name="post">Delete</button></a>"'+'<hr>'
            content.append(c)
        tags = Tags.objects.all()
        return HttpResponse(template.render({'content': content, 'tags': tags, 'username': username_global, 'userid': userid_global}, request))
    # return render(request,'home.html',{'tags':tags,'posts':posts})


def edit(request, id):
    if ('login_status' not in request.COOKIES):
        return redirect('/login')
    global userid_global
    userid_global = request.COOKIES['userid']
    global username_global
    username_global = request.COOKIES['username']
    if (request.method == 'POST'):
        title = request.POST.get('title')
        body = request.POST.get('body')
        tags = request.POST.get('tags')
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f'''Update posts set title='{title}',body='{body}',tags='{tags}' where id={id};''')
        except:
            None
        return redirect('/home')
    with connection.cursor() as cursor:
        cursor.execute(f'''Select title,body,tags from posts where id={id};''')
        post = cursor.fetchone()
        print(post)
        template = loader.get_template('edit.html')
        return HttpResponse(template.render({'title': post[0], 'body': post[1], 'tags': post[2], 'id': id}, request))


def delete(request, id):
    if ('login_status' not in request.COOKIES):
        return redirect('/login')
    global userid_global
    userid_global = request.COOKIES['userid']
    global username_global
    username_global = request.COOKIES['username']

    with connection.cursor() as cursor:
        cursor.execute(f''' Delete from posts where id={id}''')
    return redirect('/home')


def question(request, id):
    if ('login_status' not in request.COOKIES):
        return redirect('/login')
    global userid_global
    userid_global = request.COOKIES['userid']
    global username_global
    username_global = request.COOKIES['username']
    print(id)
    question = None
    with connection.cursor() as cursor:
        cursor.execute(f'''
                select posts.id as id, posts.title as title,posts.body as body,posts.tags as tags,v.count as count, posts.owner_display_name as oname, posts.creation_date cdate, posts.last_edit_date as ldate, posts.last_editor_display_name as lname
                from posts,v 
                where posts.id=v.post_id and posts.id={id} and posts.post_type_id=1;
                ''')
        print('Question done')
        que = cursor.fetchone()
        (id, title, body, tags, count, oname, cdate, ldate, lname) = que
        if (oname != None and cdate != None and ldate != None):
            question = '<h3>'+title+'</h3>'+f'<div id="upvotes">(upvotes:{count})</div>'+f'(Post by <b>{oname}</b>)' + \
                f'(Posted on <b>{cdate}</b>)'+f'(Last edited on <b>{ldate}</b>)' + \
                '<br>'+'<u><b>Question:</b></u>'+f'<b>{body}</b><br>'
        else:
            question = '<h3>'+title+'</h3>' + \
                f'<div id="upvotes">(upvotes:{count})</div>'+'<br>' + \
                '<u><b>Question:</b></u>'+f'<b>{body}</b><br>'

        content = []
        cursor.execute(f''' 
                        select posts.body, v.count, posts.owner_display_name, posts.creation_date, posts.last_edit_date from posts,v
                        where posts.id=v.post_id and posts.parent_id='{id}' and posts.post_type_id=2;
                        ''')
        ans = cursor.fetchall()
        i = 1
        for (body, up, aname, adate, ldate2) in ans:
            print(i)
            if (aname != None and adate != None and ldate2 != None):
                c = f'<u><b>Answer-{i}:</b></u>' + f' (upvotes:{up})' + f'(Answered by <b>{aname}</b> on <b>{adate}</b>)' + \
                    f'(Last edited on <b>{ldate2}</b>)<br>'+body+'<br>'
            else:
                c = f'<u><b>Answer-{i}:</b></u>' + \
                    f' (upvotes:{up})' + '<br>'+body+'<br>'
            i += 1
            content.append(c)

    template = loader.get_template('question.html')

    return HttpResponse(template.render({'content': content, 'question': question, 'id': id}, request))


def answer(request, id):
    if ('login_status' not in request.COOKIES):
        return redirect('/login')
    global userid_global
    userid_global = request.COOKIES['userid']
    global username_global
    username_global = request.COOKIES['username']
    if (request.method == 'POST'):
        body = request.POST.get('answer')
        with connection.cursor() as cursor:
            cursor.execute(f'''
                select id, title,tags,owner_user_id, owner_display_name
                from posts
                where posts.id={id} and posts.post_type_id=1;
                ''')
            que = cursor.fetchone()
            (id, title, tags, oid, oname) = que
            cursor.execute(f'''INSERT into 
            posts(owner_user_id,last_editor_user_id,post_type_id,accepted_answer_id,score,parent_id,view_count,answer_count,comment_count,owner_display_name,last_editor_display_name,title,tags,content_license,body,favorite_count,creation_date,community_owned_date,closed_date,last_edit_date,last_activity_date) 
            Values ({userid_global},{userid_global},2,0,0,{id},0,0,0,'{username_global}','{username_global}','','{tags}','CC BY-SA 3.0','{body}',0,%s,%s,%s,%s,%s)''', (datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()))
            try:
                cursor.execute(
                    f'''Select id from posts where body='{body}' and owner_user_id={userid_global} and parent_id={id} ''')
                aid = cursor.fetchone()
                cursor.execute(
                    f'''Insert into v(post_id,count) values({aid[0]},0)''')
            except:
                print("Upvotes not updated")
        return redirect(f'/question/{id}')

    template = loader.get_template('answer.html')
    return HttpResponse(template.render({'id': id}, request))


def Login(request):
    if ('login_status' in request.COOKIES):
        return redirect('/home')
    if (request.method == 'POST'):
        username = request.POST.get('username')
        userid = request.POST.get('userid')
        password = request.POST.get('password')
        with connection.cursor() as cursor:
            cursor.execute(
                f"Select password from users where id={userid} and display_name='{username}';")
            tuple = cursor.fetchone()
            print(tuple)
            global is_anoynomous
            if (tuple == None):
                return HttpResponse("invalid username and userid")
            if (password in tuple):
                global is_anoynomous
                is_anoynomous = False
                global userid_global
                global username_global
                userid_global = userid
                username_global = username
                print(userid_global)
                response = redirect('/home')
                response.set_cookie('username', username)
                response.set_cookie('userid', userid)
                response.set_cookie('login_status', True)
                return response
            else:
                return HttpResponse("Invalid Password")

    return render(request, 'login.html')


def create_post(request):
    if ('login_status' not in request.COOKIES):
        return redirect('/login')
    global userid_global
    userid_global = request.COOKIES['userid']
    global username_global
    username_global = request.COOKIES['username']
    if (request.method == 'POST'):
        title = request.POST.get('title')
        que = request.POST.get('Question')
        t1 = request.POST.get('tag1')
        t2 = request.POST.get('tag2')
        t3 = request.POST.get('tag3')
        with connection.cursor() as cursor:
            cursor.execute(f'''INSERT into 
            posts(owner_user_id,last_editor_user_id,post_type_id,accepted_answer_id,score,parent_id,view_count,answer_count,comment_count,owner_display_name,last_editor_display_name,title,tags,content_license,body,favorite_count,creation_date,community_owned_date,closed_date,last_edit_date,last_activity_date) 
            Values ({userid_global},{userid_global},1,0,0,%s,0,0,0,'{username_global}','{username_global}','{title}','<{t1}><{t2}><{t3}>','CC BY-SA 3.0','<p>{que}</p>',0,%s,%s,%s,%s,%s)''', (None, datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()))
            try:
                cursor.execute(
                    f'''Select id from posts where body='<p>{que}</p>' and owner_user_id={userid_global} ''')
                aid = cursor.fetchone()
                cursor.execute(
                    f'''Insert into v(post_id,count) values({aid[0]},0)''')
            except:
                print("Upvotes not found")
        return redirect('/home')
    # return render(request,'create_post.html')
    tags = Tags.objects.all()
    return render(request, 'create_post.html', {'tags': tags})


def create_new_accout(request):
    if (request.method == 'POST'):
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        username = request.POST.get('username')
        location = request.POST.get('location')
        profile_image_url = request.POST.get('profile_image_url')
        website_url = request.POST.get('website_url')
        about_me = request.POST.get('about_me')

        if (password == repassword):
            with connection.cursor() as cursor:
                cursor.execute(f'''INSERT into 
                users(account_id,reputation,views,down_votes,up_votes,display_name,location,profile_image_url,website_url,about_me,creation_date,last_access_date,password)
                values(0,0,0,0,0,'{username}','{location}','{profile_image_url}','{website_url}','{about_me}',%s,%s,'{password}')
                ''', (datetime.datetime.now(), datetime.datetime.now()))
                cursor.execute(f'''select max(id) from users;''')
                userid = cursor.fetchone()[0]
                response = redirect('/home')
                response.set_cookie('username', username)
                response.set_cookie('userid', userid)
                response.set_cookie('login_status', True)
                return response
        else:
            return HttpResponse("Passwords are not maatching correctly!!! Try again")

    return render(request, 'create_new_account.html')


def Logout(request):
    response = HttpResponseRedirect(reverse('login'))
    response.delete_cookie('username')
    response.delete_cookie('userid')
    response.delete_cookie('login_status')
    global userid_global
    global username_global
    username_global = None
    userid_global = None
    return response
