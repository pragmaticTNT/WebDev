import urllib.request
import json

ENCODING = "utf-8"          ## JSON requires string not bytes
FILE_NAME = "textbook.txt"  ## Results saved here

## SFU Course Outline API here:
## http://www.sfu.ca/outlines/help/api.html
BASE = "http://www.sfu.ca/bin/wcm/course-outlines?"

NUM_CUTOFF = 500            ## Only want UG courses

NUM_KEY = "value"           ## To get valid course numbers
SECTION_KEY = "value"       ## To get valid section numbers
TEXTBOOK_KEY = "requiredText"   ## JSON entry type 1
NAME_KEY = "details"
ALT_TB_KEY = "info"         ## JSON entry type 2
ALT_NAME_KEY = "title"

def is_int( string ):
    try:
        int(string)
        return True
    except ValueError:
        return False


year = input("--> Year: ")
term = input("--  Term (summer, fall, spring): ")
dept = input("--  Department (abbr): ")
print('\n')
url = BASE + year + '/' + term + '/' + dept

print("--> Getting all courses...")
raw_courses = urllib.request.urlopen(url)
str_courses = raw_courses.readall().decode(ENCODING)
courses = json.loads(str_courses)
courses_num = [course[NUM_KEY] for course in courses]

## print("--  All Courses:", courses_num)
print("--  Printing to " + FILE_NAME + "...")

results_file = open(FILE_NAME, 'w')
for course_num in courses_num:
    ## print("--  Course num:", course_num, is_int(course_num))
    if (not is_int(course_num)) or int(course_num) < NUM_CUTOFF:
        section_url = url + '/' + course_num
        raw_section = urllib.request.urlopen(section_url)
        str_section = raw_section.readall().decode(ENCODING)
        sections = json.loads(str_section)
        if len(sections) > 0 and SECTION_KEY in sections[0]:
            section = sections[0][SECTION_KEY]
            course_url = section_url + '/' + section
            ## print("--  Course url:", course_url)
            raw_course = urllib.request.urlopen(course_url)
            str_course = raw_course.readall().decode(ENCODING)
            course = json.loads(str_course)
            text = ""
            if TEXTBOOK_KEY in course:
                text = course[TEXTBOOK_KEY][0][NAME_KEY]
            elif ALT_TB_KEY in course:
                text = course[ALT_TB_KEY][ALT_NAME_KEY]
            result = course_num + ', ' + text + '\n'
            results_file.write(result)
results_file.close()

print("--  Textbook retrieval complete!")
