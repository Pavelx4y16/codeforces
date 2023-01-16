from enum import Enum


def hide_panel():
    return {'display': 'none'}


def show_panel():
    return None


class ComponentIds(Enum):
    LAYOUT = "layout"
    TABS = "cities_tabs"
    TAB_CONTENT = "tab_content"
    ADD_STUDENT_BUTTON = "add_student"
    ADD_STUDENT_PANEL = "add_student_panel"
    REMOVE_STUDENT_BUTTON = "remove_student"
    REMOVE_STUDENT_PANEL = "remove_student_panel"
    VIEW_SCHOOL_ATTRIBUTES_BUTTON = "view_school_attributes"
    VIEW_LAST_ROUND_ATTRIBUTES_BUTTON = "view_last_round_attributes"
    UPDATE_CONTESTS_BUTTON = "update_student_contests"
    GRADES_UP_BUTTON = "grades_up"
    GRADES_DOWN_BUTTON = "grades_down"
    REMOVE_GRADUATED_BUTTON = "remove_graduated_students"
    ADMIN_PANEL = "admin-panel"
    PASSWORD_INPUT = "password_input"
    PASSWORD_BUTTON = "password_button"
    SORT_MENU = "sort_menu"
    NICK_INPUT = "nick_input"
    REMOVE_NICK_INPUT = "remove_nick_input"
    FIO_INPUT = "fio_input"
    GRADE_INPUT = "grade_input"
    SCHOOL_INPUT = "school_input"

