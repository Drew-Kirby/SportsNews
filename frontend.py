import backend
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Universal Sports Dashboard")
root.geometry("600x650")

def update_name(event):
    selected_sport = sport_dropdown.get().lower()

    allowed_leagues = backend.valid_leagues.get(selected_sport, [])

    league_dropdown.config(values=allowed_leagues)

    league_dropdown.set('')

def on_button_click():
    

    sport = sport_dropdown.get().lower()
    league = league_dropdown.get()
    resource = resource_dropdown.get().lower()

    if not league:
        display_box.delete("1.0", tk.END)
        display_box.insert(tk.END, "Please select a league.")
        return
    
    api_string = backend.resource_names.get(resource)
    target_url = backend.build_url(sport, league, api_string)

    display_box.delete("1.0", tk.END)

    if resource == "news":
        headlines = backend.news(target_url)
        for headline in headlines:
            display_box.insert(tk.END, f"- {headline}\n\n")
    elif resource == "scores":
        matchups = backend.scores(target_url)
        for matchup in matchups:
            display_box.insert(tk.END, f"- {matchup}\n\n")
    elif resource == "rankings":
        rankings = backend.rankings(target_url)
        for ranking in rankings:
            display_box.insert(tk.END, f"- {ranking}\n\n")
    elif resource == "standings":
        standings = backend.standings(target_url)
        for standing in standings:
            display_box.insert(tk.END, f"- {standing}\n\n")

sport_dropdown = ttk.Combobox(root, values=["Basketball", "Football", "Baseball", "Hockey", "Soccer", "Golf", "Racing"], state="readonly")
sport_dropdown.grid(row=0, column=0, padx=10, pady=10)

sport_dropdown.bind("<<ComboboxSelected>>", update_name)

league_dropdown = ttk.Combobox(root, state="readonly")
league_dropdown.grid(row=0, column=1, padx=10, pady=10)

resource_dropdown = ttk.Combobox(root, values=["News", "Scores", "Standings", "Rankings"], state="readonly")
resource_dropdown.grid(row=0, column=2, padx=10, pady=10)
resource_dropdown.set('News')

display_box = tk.Text(root, wrap="word", width=55, height=15)
display_box.grid(row=1, column=0, padx=10, pady=10)

fetch_button = ttk.Button(root, text="Get Resource", command=on_button_click)
fetch_button.grid(row=2, column=0, padx=10, pady=5)

root.mainloop()