#accounts views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils import timezone
import logging
from ldap3 import Server, Connection
from .models import LogEntry, LoginEntry
from .ldap_config import LDAP_SERVER_URL, GROUP_BASE, USER_BASE, BIND_DN, BIND_PASSWORD

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)

def execute_confluent_command(command):
    server = Server(LDAP_SERVER_URL, get_info=ALL)
    conn = Connection(server, user=BIND_DN, password=BIND_PASSWORD, auto_bind=True)
    approved = command.lower() == "test"
    if approved:
        conn.search(USER_BASE, "(objectClass=inetOrgPerson)", attributes=['uid'])
        result = f"Command '{command}' executed via LDAP at {timezone.now().strftime('%Y-%m-%d %H:%M:%S %Z')}"
    else:
        result = f"Command '{command}' rejected at {timezone.now().strftime('%Y-%m-%d %H:%M:%S %Z')}"
    conn.unbind()
    return approved, result

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        logger.info(f"Attempting to authenticate user: {username} at {timezone.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
        user = authenticate(request, username=username, password=password)
        ip_address = request.META.get('REMOTE_ADDR')
        if user is not None:
            login(request, user)
            logger.info(f"User {username} logged in successfully at {timezone.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
            LoginEntry.objects.create(user=user, success=True, ip_address=ip_address)
            return JsonResponse({"success": True, "message": "Login successful"})
        else:
            logger.warning(f"Authentication failed for {username} at {timezone.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
            LoginEntry.objects.create(user=None, success=False, ip_address=ip_address, message=f"Invalid credentials for {username}")
            return JsonResponse({"success": False, "message": "Invalid credentials"})
    return render(request, "login.html")

def submit_request(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        command = request.POST.get("command", "")
        approved, message = execute_confluent_command(command)
        LogEntry.objects.create(command=command, approved=approved, message=message)
        logger.info(f"Command: {command}, Approved: {approved}, Message: {message}, Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
        return JsonResponse({"approved": approved, "message": message})
    return render(request, "submit.html")

def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    topics = ["1", "2", "3", "4"]
    return render(request, "home.html", {"topics": topics})

def topic_detail(request, topic_name):
    if not request.user.is_authenticated:
        return redirect("login")
    logger.info(f"Rendering topic_detail with topic_name: {topic_name}")
    topics = ["1", "2", "3", "4"]  # Match the home view topics
    return render(request, "topic_detail.html", {"topic_name": topic_name, "topics": topics})

def create_topic(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        topic_name = request.POST.get("topic_name").strip()
        partitions = request.POST.get("partitions")
        if topic_name and partitions:
            logger.info(f"Creating topic '{topic_name}' with {partitions} partitions")
            return redirect("topic_detail", topic_name=topic_name)
        else:
            return render(request, "home.html", {"topics": ["1", "2", "3", "4"], "error": "Please fill all fields."})
    return render(request, "home.html", {"topics": ["1", "2", "3", "4"]})