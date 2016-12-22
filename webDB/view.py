#!/usr/bin/python
#coding: utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf
from django.db import connection

def get_team_member(team_id):
    member_list = []
    with connection.cursor() as cursor:
        cursor.execute("select * from ManageModel_in_team where team_id = %d" % team_id)
        row = cursor.fetchall()
        row = list(row)
        for item in row:
            member_id = int(item[1])
            cursor.execute("select person_name from ManageModel_person where id = %d" % member_id)
            member_name = cursor.fetchone()
            member_name = member_name[0]
            member_list.append([member_id,member_name,member_id])
    return member_list

def index(request):
    return render(request,'index.html')

def people(request):
    context = {}
    context.update(csrf(request))
    people_list = []
    with connection.cursor() as cursor:
        if request.method == "GET":
            if request.GET.get('all') == '0':
                if request.GET.get('person_id') != None:
                    person_id = int(request.GET.get('person_id'))
                    cursor.execute("select * from ManageModel_person where id = %d" % person_id)
                else:
                    person_name = request.GET.get('person_name')
                    cursor.execute("select * from ManageModel_person where person_name = '%s'" % person_name)
            else:
                cursor.execute("select * from ManageModel_person")
        for item in cursor.fetchall():
            item = list(item)
            item[0] = str(item[0])
            item[1] = str(item[1])
            item[2] = item[2].isoformat()
            item.append(item[0])
            people_list.append(item)
    context['people_list'] = people_list
    return render(request,'people.html',context)

def hello(request):
    return HttpResponse("hello")

def add_people(request):
    context = {}
    if request.method == "POST":
        context.update(csrf(request))
        person_name = request.POST.get('person_name')
        birth_date = request.POST.get('birth_date')
        ## try
        with connection.cursor() as cursor:
            try:
                cursor.execute("insert into ManageModel_person(person_name,birth) values('%s','%s')" % (person_name,birth_date))
                context['info'] = "add_people_success"
            except:
                context['info'] = "add_people_fail"
    return render(request,'add_people.html',context)

def team(request):
    context = {}
    leader_list = []
    with connection.cursor() as cursor:
        if request.method == "GET":
            if request.GET.get('all') == '0':
                if request.GET.get('team_id') != None:
                    team_id = int(request.GET.get('team_id'))
                    cursor.execute("select * from ManageModel_team where id = %d" % team_id)
                else:
                    team_name = request.GET.get('team_name')
                    cursor.execute("select * from ManageModel_team where team_name = '%s'" % team_name)
            else:
                cursor.execute("select * from ManageModel_team")
        row = cursor.fetchall()
        row = list(row)
        for i in range(len(row)):
            row[i] = list(row[i])
            leader_id = int(row[i][2]);
            cursor.execute("select person_name from ManageModel_person where id = %d" % leader_id)
            item = cursor.fetchone()
            leader_name = str(item[0])
            row[i].append(leader_name)
            row[i].append(row[i][0])
        context['team_list'] = row

    return render(request,'team.html',context) 

def add_team(request):
    context = {}
    if request.method == "POST":
        context.update(csrf(request))
        team_name = request.POST.get('team_name')
        leader_id = int(request.POST.get('leader_id'))
        with connection.cursor() as cursor:
            try:
                cursor.execute("insert into ManageModel_team(team_name,leader_id) values('%s',%d)" % (team_name,leader_id))
                cursor.execute("select id from ManageModel_team order by id desc limit 1")
                row = cursor.fetchone()
                team_id = int(row[0])
                cursor.execute("insert into ManageModel_in_team(person_id,team_id) values(%d,%d)" % (leader_id,team_id))
                context['info'] = "add_team_success"
            except:
                context['info'] = "add_team_fail"
    return render(request,'add_team.html',context)

def team_member(request):
    context = {}
    if request.method == "GET":
        team_id = int(request.GET.get('team_id'))
    else:
        team_id = int(request.POST.get('team_id'))
        person_name = request.POST.get('person_name')
        try:
            person_id = int(request.POST.get('person_id'))
            context['alert'] = False
        except:
            context['alert'] = True
        with connection.cursor() as cursor:
            cursor.execute("select id from ManageModel_person where id = %d and person_name = '%s'" %(person_id,person_name))
            row = cursor.fetchall()
            for item in row:
                person_id = int(item[0])
                cursor.execute("insert into ManageModel_in_team(person_id,team_id) values(%d,%d)" % (person_id,team_id))
    context['member_list'] = get_team_member(team_id)
    context['team_id'] = team_id
    return render(request,'team_member.html',context)

def search_post(request):
    ctx ={}
    ctx.update(csrf(request))
    if request.POST:
        ctx['person_name'] = request.POST['person_name']
        ctx['birth_date'] = request.POST['person_name']
    return render(request, "post.html", ctx)

def project(request):
    ctx = {}
    project_list = []
    with connection.cursor() as cursor:
        if request.method == "GET":
            if request.GET.get('project_name') != None:
                project_name = request.GET.get('project_name')
                cursor.execute("select id,project_name from ManageModel_project where project_name = '%s'" % project_name)
            else:
                cursor.execute("select id,project_name from ManageModel_project ")
            row = cursor.fetchall()
            row = list(row)
            for i in range(len(row)):
                row[i] = list(row[i])
                row[i][0] = int(row[i][0])
                row[i].append(row[i][0])
            ctx['team_list'] = row

    return render(request,"project.html",ctx)

def add_project(request):
    context = {}
    if request.method == "POST":
        context.update(csrf(request))
        project_name = request.POST.get('project_name')
        project_detail = request.POST.get('project_detail')
        ## try
        with connection.cursor() as cursor:
            try:
                cursor.execute("insert into ManageModel_project(project_name,detail) values('%s','%s')" % (project_name,project_detail))
                context['info'] = "add_project_success"
            except:
                context['info'] = "add_project_fail"
    return render(request,'add_project.html',context)

def project_detail(request):
    context = {}
    team_list = []
    if request.method == "GET":
        project_id = int(request.GET.get('project_id'))
    else:
        project_id = int(request.POST.get('project_id'))
        team_name = request.POST.get('team_name')
        try:
            team_id = int(request.POST.get('team_id'))
            context['alert'] = False
        except:
            context['alert'] = True
        with connection.cursor() as cursor:
            cursor.execute("select id from ManageModel_team where id = %d and team_name = '%s'" %(team_id,team_name))
            item = cursor.fetchone()
            team_id = int(item[0])
            cursor.execute("insert into ManageModel_involve_project(project_id,team_id) values(%d,%d)" % (project_id,team_id))
    with connection.cursor() as cursor:
        cursor.execute("select team_id from ManageModel_involve_project where project_id = %d " % project_id)
        row = cursor.fetchall()
        row = list(row)
        for i in range(len(row)):
            row[i] = list(row[i])
            row[i][0] = int(row[i][0])
            team_id = row[i][0]
            cursor.execute("select team_name from ManageModel_team where id = %d" % team_id)
            item = cursor.fetchone()
            team_name = item[0]
            row[i].append(team_name)
            row[i].append(team_id)
        context['team_list'] = row
        #detail 
        cursor.execute("select detail from ManageModel_project where id = %d" % project_id)
        item = cursor.fetchone()
        context['detail'] = item[0]
    #context['member_list'] = get_team_member(project_id)
    context['project_id'] = project_id
    return render(request,'project_detail.html',context)

def event(request):
    context = {}
    with connection.cursor() as cursor:
        if request.method == "GET":
            if request.GET.get('event_name') != None:
                event_name = request.GET.get('event_name')
                cursor.execute("select id,event_name,time from ManageModel_event where event_name = '%s'" % event_name)
            else:    
                cursor.execute("select id,event_name,time from ManageModel_event")
            row = cursor.fetchall()
            row = list(row)
            for i in range(len(row)):
                row[i] = list(row[i])
                row[i][2] = str(row[i][2])
                row[i].append(row[i][0])
            context['event_list'] = row
    return render(request,'event.html',context)

def add_event(request):
    context = {} 
    if request.method == "POST":
        context.update(csrf(request))
        event_name = request.POST.get('event_name')
        event_time = request.POST.get('event_time')
        event_detail = request.POST.get('event_detail')
        ## try
        with connection.cursor() as cursor:
            try:
                cursor.execute("insert into ManageModel_event(event_name,time,detail) values('%s','%s','%s')" % (event_name,event_time,event_detail))
                context['info'] = "add_event_success"
            except:
                context['info'] = "add_event_fail"
    return render(request,'add_event.html',context)

def event_detail(request):
    context = {} 
    team_list = []
    if request.method == "GET":
        event_id = int(request.GET.get('event_id'))
    else:
        event_id = int(request.POST.get('event_id'))
        team_name = request.POST.get('team_name')
        try:
            team_id = int(request.POST.get('team_id'))
            context['alert'] = False
        except:
            context['alert'] = True
        with connection.cursor() as cursor:
            cursor.execute("select id from ManageModel_team where id = %d and team_name = '%s'" %(team_id,team_name))
            item = cursor.fetchone()
            team_id = int(item[0])
            cursor.execute("insert into ManageModel_happen_event(event_id,team_id) values(%d,%d)" % (event_id,team_id))
    with connection.cursor() as cursor:
        cursor.execute("select team_id from ManageModel_happen_event where event_id = %d " % event_id)
        row = cursor.fetchall()
        row = list(row)
        for i in range(len(row)):
            row[i] = list(row[i])
            row[i][0] = int(row[i][0])
            team_id = row[i][0]
            cursor.execute("select team_name from ManageModel_team where id = %d" % team_id)
            item = cursor.fetchone()
            team_name = item[0]
            row[i].append(team_name)
            row[i].append(team_id)
        context['team_list'] = row
        #detail 
        cursor.execute("select detail from ManageModel_event where id = %d" % event_id)
        item = cursor.fetchone()
        context['detail'] = item[0]
    #context['member_list'] = get_team_member(project_id)
    context['event_id'] = event_id
    return render(request,'event_detail.html',context)

def task(request):
    context = {}
    with connection.cursor() as cursor:
        search_person_name = False
        if request.method == "GET":
            if request.GET.get('task_name') != None:
                task_name = request.GET.get('task_name')
                cursor.execute("select id,task_name,deadline from ManageModel_task where task_name = '%s'" % task_name)
            elif request.GET.get('person_name') != None:
                print('fuck')
                search_person_name = True
                person_name = request.GET.get('person_name')
                cursor.execute("select task_id from ManageModel_have_task as H ,ManageModel_person as P where P.id = H.person_id and person_name = '%s'" % person_name)
                row = cursor.fetchall()
                row = list(row)
                task_list = []
                for task_id in row:
                    cursor.execute("select id,task_name,deadline from ManageModel_task where id = %d" % task_id) 
                    task = cursor.fetchone()
                    task = list(task)
                    task[2] = str(task[2])
                    task.append(task[0])
                    task_list.append(task)
                context['task_list'] = task_list
            else:    
                cursor.execute("select id,task_name,deadline from ManageModel_task")
            if search_person_name == False:
                row = cursor.fetchall()
                row = list(row)
                for i in range(len(row)):
                    row[i] = list(row[i])
                    row[i][2] = str(row[i][2])
                    row[i].append(row[i][0])
                context['task_list'] = row
    return render(request,'task.html',context)

def add_task(request):
    context = {}
    if request.method == "POST":
        context.update(csrf(request))
        task_name = request.POST.get('task_name')
        deadline = request.POST.get('deadline')
        task_detail = request.POST.get('task_detail')
        print(str(task_name))
        print(str(deadline))
        print(str(task_detail))
        ## try
        with connection.cursor() as cursor:
            try:
                cursor.execute("insert into ManageModel_task(task_name,deadline,detail) values('%s','%s','%s')" % (task_name,deadline,task_detail))
                context['info'] = "add_task_success"
            except:
                context['info'] = "add_task_fail"
    return render(request,'add_task.html',context)

def task_detail(request):
    context = {} 
    team_list = []
    if request.method == "GET":
        task_id = int(request.GET.get('task_id'))
    else:
        task_id = int(request.POST.get('task_id'))
        person_name = request.POST.get('person_name')
        try:
            person_id = int(request.POST.get('person_id'))
            context['alert'] = False
        except:
            context['alert'] = True
        with connection.cursor() as cursor:
            cursor.execute("select id from ManageModel_person where id = %d and person_name = '%s'" %(person_id,person_name))
            item = cursor.fetchone()
            person_id = int(item[0])
            cursor.execute("insert into ManageModel_have_task(person_id,task_id) values(%d,%d)" % (person_id,task_id))
    with connection.cursor() as cursor:
        cursor.execute("select person_id from ManageModel_have_task where task_id = %d " % task_id)
        row = cursor.fetchall()
        row = list(row)
        for i in range(len(row)):
            row[i] = list(row[i])
            row[i][0] = int(row[i][0])
            person_id = row[i][0]
            cursor.execute("select person_name from ManageModel_person where id = %d" % person_id)
            item = cursor.fetchone()
            person_name = item[0]
            row[i].append(person_name)
            row[i].append(person_id)
        context['person_list'] = row
        #detail 
        cursor.execute("select detail from ManageModel_task where id = %d" % task_id)
        item = cursor.fetchone()
        context['detail'] = item[0]
    #context['member_list'] = get_team_member(project_id)
    context['task_id'] = task_id
    return render(request,'task_detail.html',context)
def people_delete(request):
    context = {}
    if request.method == "POST":
        context.update(csrf(request))
        person_id = int(request.POST.get('person_id'))
        with connection.cursor() as cursor:
            cursor.execute("delete from ManageModel_in_team where person_id = %d" % person_id)
            cursor.execute("delete from ManageModel_have_task where person_id = %d" % person_id)
            cursor.execute("delete from ManageModel_person where id = %d" % person_id)
    return HttpResponseRedirect("/people/")
