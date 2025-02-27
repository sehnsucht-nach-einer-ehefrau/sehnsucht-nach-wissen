import time
from datetime import datetime
import os
import platform
from lazyinput import lazy
from notifypy import Notify
from groq import Groq

client = Groq(
    api_key="YOUR GROQ API KEY HERE",
)


class ActivityItem:
    def __init__(self, content, count, category):
        self.content = content
        self.count = count
        self.category = category

    def count_inc(self):
        self.count += 1

    def check_exists(self, input_list):
        for i in input_list:
            if self.content == i.content:
                return True

        return False

    def exists_index(self, input_list):
        for i in range(len(input_list)):
            if self.content == input_list[i].content:
                return i

        return 0


def main():
    options_list = ["track", "examine", "quit"]
    options = lazy(options_list)
    if "track" in options:
        notif = input("\nnotifications or audio?\n")
        if notif == "notifications":
            track(True)
        else:
            track(False)
    elif "examine" in options:
        date = input("\nexamine what date?\n")
        examine(date)


def check_os():
    os_name = platform.system()
    if os_name == "Darwin":
        return "macOS"
    elif os_name == "Linux":
        return "Linux"
    else:
        return "Other"


def track(notif):
    f = open(f"{datetime.today().strftime('%m-%d-%Y')}.txt", "w")
    print("Get to Work.")
    notification = Notify()
    notification.title = "Record Data."
    notification.message = "It's been 15 minutes. What have you been doing?"
    os_name = check_os()
    file = "./chirp.mp3"
    while True:
        time.sleep(900)

        if notif:
            notification.send()
        else:
            if os_name == "macOS":
                os.system("afplay " + file)
            elif os_name == "Linux":
                os.system("mpg123 " + file)

        activity = input("What have you been doing for the past 15 minutes?\n")
        if activity == "exit":
            break
        print("Get back to Work.")
        f.write(activity)

    f.close()


def examine(date):
    f = open(f"{date}.txt", "r")
    print("\n")
    os.system("clear")
    print(f"Report for {date} ====================\n")
    print(analyze(f))
    print("\nEnd of Report =========================\n")


def analyze(file):
    line_list = file.readlines()

    complete_string = f"match the following list into vague categories like 'Entertainment', 'Studying', etc. Don't introduce yourself, don't saying anything other than what I told you to do. Put items that aren't activities or tasks into a 'Misc' category. Based on the number of tasks within each category, calculate by percentage how much time was spent in a category. If there are duplicates, only put one instance of the item. If no tasks fall under a category, don't put the category. Follow this format: [CATEGORY](in square brackets) - x%\n- task\n- task\n- etc\n. list: {line_list}"

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": complete_string}],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    main()
