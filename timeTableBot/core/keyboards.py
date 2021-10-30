from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from core.models import Faculty, Student_group
from asgiref.sync import sync_to_async


@sync_to_async
def get_inline_kb_faculty():
    inline_kb_faculty = InlineKeyboardMarkup(row_width=2)
    faculty_list = list(Faculty.objects.values_list('name', flat=True))
    inline_kb_faculty.add(*[types.KeyboardButton(group, callback_data=f'faculty_{group}') for group in faculty_list])

    return inline_kb_faculty

@sync_to_async
def get_inline_kb_course():
    inline_kb_course = InlineKeyboardMarkup(row_width=3)
    courses = ['1-й Курс', '2-й Курс', '3-й Курс', '4-й Курс', '5-й Курс', '6-й Курс']
    inline_kb_course.add(*[types.KeyboardButton(course, callback_data=f'course_{course[0]}') for course in courses])

    return inline_kb_course


@sync_to_async
def get_inline_kb_direction(faculty_name, course):
    inline_kb_direction = InlineKeyboardMarkup(row_width=3)

    directions = Student_group.objects.filter(faculty__name=faculty_name, course=course).values_list('direction', flat=True)
    directions = list(set(directions))
    inline_kb_direction.add(*[types.KeyboardButton(direction, callback_data=f'direction_{direction}') for direction in directions])

    return inline_kb_direction


@sync_to_async
def get_inline_kb_group(faculty_name, course, direction):
    inline_kb_direction = InlineKeyboardMarkup(row_width=3)

    groups = Student_group.objects.filter(faculty__name=faculty_name, course=course, direction=direction).values_list('name', flat=True)
    inline_kb_direction.add(*[types.KeyboardButton(group, callback_data=f'group_{group}') for group in groups])

    return inline_kb_direction