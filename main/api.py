from django.http import JsonResponse, HttpResponseNotFound
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from main.models import Bug, User
from main.serializers import UserSerializer, BugSerializer


@api_view()
def bugs(request):
    bugs = Bug.objects.all().order_by("-created")
    serializer = BugSerializer(bugs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def newbug(request):
    serializer = BugSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def bug(request, bugid):
    try:
        bug = Bug.objects.get(id=bugid)
    except Bug.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = BugSerializer(bug)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = BugSerializer(bug, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        bug.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def people(request):
    people = User.objects.all().order_by("-id")
    serializer = UserSerializer(people, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def newperson(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def person(request, personid):
    try:
        person = User.objects.get(id=personid)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserSerializer(person)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = UserSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
