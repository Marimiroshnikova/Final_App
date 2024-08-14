from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Course
from .serializers import CourseSerializer



@api_view(['GET'])
def get_routes(request):
    routes = [
        "GET /api",
        "GET /api/courses",
        "GET /api/courses/:id"
    ]
    return Response(routes)

@api_view(['GET'])
def get_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_course(request, id):
    course = Course.objects.get(id=id)
    serializer = CourseSerializer(course, many=False)
    return Response(serializer.data)