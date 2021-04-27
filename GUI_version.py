# GUI version of application by Michał Matachowski version 1.0

import requests
import json
import webbrowser
from tkinter import *


class Application(Frame):
    """GUI Application with one submit button"""
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """GUI Layout"""
        # Label with instruction for user
        self.info_lbl = Label(self, text="Type the name of team which highlights you want to see: ")
        self.info_lbl.grid(row=0, column=0, columnspan=2, sticky=W)

        # Blank row for better better readability
        self.blank_row = Label(self)
        self.blank_row.grid(row=1, column=1)

        # Label with information for entery field
        self.team_lbl = Label(self, text="Team: ")
        self.team_lbl.grid(row=2, column=1, sticky=E)

        # Entry field to type football team name
        self.entry_field = Entry(self)
        self.entry_field.grid(row=2, column=2, sticky=W)

        # Submit button to confirm choice and send request to API after press
        self.submit_button = Button(self, text="Submit", bg="grey70", command=self.press_button)
        self.submit_button.grid(row=2, column=2, sticky=E)

        # Blank row for better better readability
        self.blank_row2 = Label(self)
        self.blank_row2.grid(row=3, column=0)

        # Label with information of text field
        self.info_lbl = Label(self, text="Details about found matches:")
        self.info_lbl.grid(row=4, column=0, columnspan=2, sticky=W)

        # Text field for information about matches and example of correct result
        self.info_txt = Text(self, width=100, height=8, wrap=WORD)
        self.info_txt.insert(0.0, "e.g. 2021-04-25 14:15 Villarreal - Barcelona |SPAIN: La Liga|")
        self.info_txt.grid(row=5, column=1, columnspan=2, sticky=E)

    @classmethod
    def team_found_checker(cls, list_to_check, team, title="title"):
        """Function checks if selected team appears in database. It also prevents mistyping"""
        number_of_appearances = []
        for i in range(len(list_to_check)):
            if team in list_to_check[i][title]:
                number_of_appearances.append(team)
        if len(number_of_appearances) == 0:
            return "No matches found. Check name of selected team."
        elif len(number_of_appearances) == 1:
            return f"{len(number_of_appearances)} match found\n"
        else:
            return f"{len(number_of_appearances)} matches found\n"

    def press_button(self):
        """Submit button function"""
        self.info_txt.delete(0.0, END)
        contents = self.entry_field.get()
        request = requests.get("https://www.scorebat.com/video-api/v1/")  # database request and error check
        try:
            questions = request.json()
        except json.decoder.JSONDecodeError:
            print("Invalid format")
        else:
            selected_team = contents.title()
            # code added after tests
            if "fc" or "Fc" or "FC" in selected_team:
                selected_team = selected_team[2:]
            else:
                selected_team = selected_team
            if len(selected_team) <= 3:
                self.info_txt.insert(0.0, "Invalid data. Name probably too short.")
            else:
                message = self.team_found_checker(questions, selected_team)+"\n"
                self.info_txt.insert(0.0, message)
                # main loop checks matches in db.
                # If selected team is found in match title, it will insert match details into txt field.
                for i in range(len(questions)):
                    if selected_team in questions[i]["title"]:
                        match_details = (questions[i]["date"][:10], questions[i]["date"][11:16], questions[i]["title"],
                                         "|" + questions[i]["competition"]["name"] + "|")
                        self.info_txt.insert(END, match_details)
                        self.info_txt.insert(END, "\n")
                        # automatically open page with match details and highlights video
                        webbrowser.open_new_tab(questions[i]["url"])


def main():
    """Main function, root settings"""
    root = Tk()
    root.title("Favourite team highlights")
    root.geometry("820x300")
    root.iconbitmap(r"favicon.ico")  # icon change
    app = Application(root)
    root.mainloop()


main()
