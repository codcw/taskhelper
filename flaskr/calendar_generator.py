import calendar
from datetime import datetime

def generateMonth(tasks, month):
    cal = calendar.Calendar()
    current = datetime.now()
    current_year = current.year
    current_month = month

    def generatePopover(query_object):
        object_date = query_object.first().start
        object_date = object_date.strftime("%B %d, %A")
        tasks_html = "<ol class =\'list-group list-group-numbered list-group-flush\'>"
        for entry in query_object:
            tasks_html +=   "<li class=\'list-group-item\'>" \
                            f"{entry.name}</li>"
        tasks_html += "</ol>"
        popover =   "style=\"background-color: LightPink;\" "\
                    "tabindex=\"0\" "\
                    "data-bs-toggle = \"popover\" "\
                    "data-bs-trigger = \"focus\" " \
                    "data-bs-html = \"true\" " \
                    "data-bs-animation = \"false\" " \
                    f"data-bs-title = \"{object_date}\" "\
                    f"data-bs-content = \"{tasks_html}\""
        return popover

    with open('templates\\generated_calendar.html', "a") as file:
        file.write( "<div class=\"col\">" \
                    f"<h3>{calendar.month_name[current_month]}</h3>" )
        file.write("""
                    <table class=\"table table-bordered table-sm text-center\" style=\"width:100%\">
                    <thead>
                    <tr>
                   """)

        for day in calendar.day_abbr:
            file.write(f"<th scope=\"col\" style=\"width:{100/7}%\">{day}</th>\n")
        file.write( """
                    </tr>
                    </thead>
                    <tbody>
                    """)

        for date in cal.itermonthdates(current_year, current_month):
            if date.weekday() == 0:
                file.write("\n<tr>")
            if date in tasks.keys():
                file.write(f"<td {generatePopover(tasks[date])}>{date.day}</td>")
            else:
                file.write(f"<td>{date.day}</td>")
            if date.weekday() == 6:
                file.write("</tr>\n")

        file.write( """
                    </tbody>
                    </table>
                    </div>
                    """)

def generateYearTable(func, tasks):
    with open('templates\\generated_calendar.html', 'w') as file:
        file.write(f"<h1>{datetime.now().year}</h1>" \
                   "<div class=\"row row-cols-3\">" )
    for i in range(1, 13):
        func(tasks, i)
    with open('templates\\generated_calendar.html', "a") as file:
        file.write("</div>")