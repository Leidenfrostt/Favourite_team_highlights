# Terminal version of application by Michał Matachowski version 1.0

import requests
import json
import webbrowser


def team_found_checker(list_to_check, team, title="title"):
    """Function checks if selected team appears in database. It also prevents mistyping"""
    number_of_appearances = []
    for i in range(len(list_to_check)):
        if team in list_to_check[i][title]:
            number_of_appearances.append(team)
    if len(number_of_appearances) == 0:
        return "\nNo matches found. Check name of selected team."
    elif len(number_of_appearances) == 1:
        return f"\n{len(number_of_appearances)} match found\n"
    else:
        return f"\n{len(number_of_appearances)} matches found\n"


def main():
    """Function ask user about team to search in database. Give information about number of found matches, dates,
    rival teams and competition. Automatically opens match details an highlights in new tabs.
    """
    request = requests.get("https://www.scorebat.com/video-api/v1/")
    try:
        questions = request.json()
    except json.decoder.JSONDecodeError:
        print("Invalid format")
    else:
        selected_team = input("Type the name of team which highlights you want to see: ").title()
        # added after tests
        if "fc" or "Fc" or "FC" in selected_team:
            selected_team = selected_team[2:]
        else:
            selected_team = selected_team
        print(team_found_checker(questions, selected_team))
        for i in range(len(questions)):
            if selected_team in questions[i]["title"]:
                print(questions[i]["date"][:10], questions[i]["date"][11:16],
                      questions[i]["title"], "|"+questions[i]["competition"]["name"]+"|")
                webbrowser.open_new_tab(questions[i]["url"])
            else:
                pass


main()
