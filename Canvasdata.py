import requests
from datetime import datetime, timezone

# Your Canvas API details
API_URL = "https://ulm.instructure.com/api/v1/courses"
TOKEN = "23796~Lk9cA9VNhvLQXxwtWh9LMRQhLKfJChW2BGf3hCYXeQ8FNnDa44ZMFVxEun4K4zmH"  # Replace with your actual API token

# Authentication headers
headers = {
    "Authorization": f"Bearer {TOKEN}"
}

# Fetch all courses, handling pagination
def fetch_all_courses():
    """Fetch all courses across multiple pages."""
    courses = []
    url = API_URL
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            courses.extend(response.json())
            url = response.links.get('next', {}).get('url')  # Get next page if available
        else:
            break
    return courses

# Filter courses for the current semester 
def is_current_semester(course):
    """Checks if a course belongs to the current semester (Spring 2025)."""
    term_name = course.get("term", {}).get("name", "").lower()
    course_name = course.get("name", "").lower()
    course_code = course.get("course_code", "").lower()

    # If the course explicitly mentions "Spring 2025", include it
    return "spring 2025" in term_name or "spring 2025" in course_name or "spring 2025" in course_code

# Fetch assignments for a course
def get_assignments(course_id):
    """Fetch assignments for a specific course."""
    url = f"https://ulm.instructure.com/api/v1/courses/{course_id}/assignments"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        assignments = response.json()
        upcoming = [
            f"{a['name']} - Due: {a['due_at']}" for a in assignments if a.get('due_at')
        ]
        return upcoming
    else:
        return ["Failed to fetch assignments"]

# Fetch courses
courses = fetch_all_courses()
current_semester_courses = [course for course in courses if is_current_semester(course)]

# Print the courses for the current semester
print("\n📌 Current Semester Courses:")
for course in current_semester_courses:
    print(f"- {course['name']} (ID: {course['id']})")

# Fetch and display assignments for each course
print("\n📌 Assignments:")
for course in current_semester_courses:
    print(f"\n🔹 {course['name']} (ID: {course['id']})")
    
    assignments = get_assignments(course['id'])
    
    if assignments:
        for assignment in assignments:
            print(f"   📌 {assignment}")
    else:
        print("   ✅ No upcoming assignments.")
