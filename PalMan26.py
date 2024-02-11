import json
import tkinter as tk
from tkinter import ttk

checkbox_values = {}  # Dictionary to store checkbox values for each name


def create_characteristics_frame(name):
    characteristics_frame = tk.Frame(database_tab)
    tk.Label(characteristics_frame, text=name).pack(anchor='w')

    characteristics = [
        "Passive", "none", "Abnormal", "Aggressive", "Artisan",
        "Burly Body", "Blood of the Dragon", "Botanical Barrier", "Brave",
        "Capacitor", "Celestial Emperor", "Cheery", "Coldblooded",
        "Conceited", "Dainty Eater", "Diet Lover", "Divine Dragon",
        "Dragonkiller", "Earth Emperor", "Earthquake Resistant",
        "Ferocious", "Flame Emperor", "Fragrant Foliage", "Hard Skin",
        "Heated Body", "Hooligan", "Hydromaniac", "Ice Emperor",
        "Insulated Body", "Legend", "Logging Foreman", "Lord of Darkness",
        "Lord of Lightning", "Lord of the Sea", "Lucky", "Masochist",
        "Mine Foreman", "Motivational Leader", "Musclehead", "Nimble",
        "Positive Thinker", "Power of Gaia", "Pyromaniac", "Runner", "Sadist",
        "Serious", "Spirit Emperor", "Suntan Lover", "Swift",
        "Stronghold Strategist", "Vanguard", "Veil of Darkness", "Waterproof",
        "Workaholic", "Work Slave", "Zen Mind"
    ]

    # Store checkbox values for each name and characteristic
    checkbox_values[name] = {char: [tk.IntVar() for _ in range(4)] for char in characteristics}

    for characteristic in characteristics:
        characteristic_frame = tk.Frame(characteristics_frame)
        tk.Label(characteristic_frame, text=characteristic, width=10, anchor='w').pack(side='left')

        if characteristic == "Passive":
            tk.Label(characteristic_frame, text="  Clean        Mixed").pack(side='left')
        else:
            for checkbox in checkbox_values[name][characteristic]:
                tk.Checkbutton(characteristic_frame, variable=checkbox).pack(side='left')

        characteristic_frame.pack(anchor='w', fill='x')

    return characteristics_frame


def update_characteristics(name):
    for widget in selected_characteristics.winfo_children():
        widget.destroy()

    for widget in database_tab.winfo_children():
        if widget.winfo_children()[0].cget("text") == name:
            characteristics_frame = widget

    if name != "Select Pal" and characteristics_frame:
        pals_var.set(name)  # Set the dropdown menu's value to the selected pal's name
        selected_pal_label.config(text=name)  # Update the selected Pal's name in the label

        canvas_container = tk.Frame(selected_characteristics)
        canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=0, padx=0, pady=0)

        canvas = tk.Canvas(canvas_container, height=800, width=250)
        scrollbar = tk.Scrollbar(canvas_container, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='left', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        checkbox_colors = ["#66B3FF", "#FFCCCC", "#66B3FF", "#FFCCCC"]
        for characteristic in characteristics_frame.winfo_children():
            if characteristic.winfo_children():
                characteristic_name = characteristic.winfo_children()[0].cget("text")
                characteristic_clone = tk.Frame(scrollable_frame)
                characteristic_clone.pack(fill='x')

                tk.Label(characteristic_clone, text=characteristic_name, width=17, anchor='w').pack(side='left')

                if characteristic_name == "Passive":
                    tk.Label(characteristic_clone, text="  Clean        Mixed").pack(side='left')
                else:
                    index = 0
                    for checkbox in checkbox_values[name][characteristic_name]:
                        tk.Checkbutton(characteristic_clone, variable=checkbox,
                                       bg=checkbox_colors[index % 2]).pack(side='left')
                        index += 1


def populate_dropdown():
    for name in names:
        pals_dropdown['menu'].add_command(label=name, command=lambda n=name: update_characteristics(n))

    # Remove "SelectxPal" from the dropdown menu
    pals_dropdown['menu'].delete("SelectxPal")


def save_data():
    data = {}
    for name in names:
        char_data = {}
        for characteristic in checkbox_values[name]:
            char_data[characteristic] = [var.get() for var in checkbox_values[name][characteristic]]
        data[name] = char_data

    with open("pals.json", "w") as file:
        json.dump(data, file)


def load_data():
    with open("pals.json", "r") as file:
        data = json.load(file)
        for name in data:
            for characteristic in data[name]:
                for index, value in enumerate(data[name][characteristic]):
                    checkbox_values[name][characteristic][index].set(value)


def clear_data():
    for name in checkbox_values:
        for characteristic in checkbox_values[name]:
            for checkbox in checkbox_values[name][characteristic]:
                checkbox.set(0)


def fill_data():
    for name in checkbox_values:
        for characteristic in checkbox_values[name]:
            for checkbox in checkbox_values[name][characteristic]:
                checkbox.set(1)


def create_skills_frame():
    skills_frame = tk.Frame(skills_tab)

    characteristics = [
        "none", "Abnormal", "Aggressive", "Artisan",
        "Burly Body", "Blood of the Dragon", "Botanical Barrier", "Brave",
        "Capacitor", "Celestial Emperor", "Cheery", "Coldblooded",
        "Conceited", "Dainty Eater", "Diet Lover", "Divine Dragon",
        "Dragonkiller", "Earth Emperor", "Earthquake Resistant",
        "Ferocious", "Flame Emperor", "Fragrant Foliage", "Hard Skin",
        "Heated Body", "Hooligan", "Hydromaniac", "Ice Emperor",
        "Insulated Body", "Legend", "Logging Foreman", "Lord of Darkness",
        "Lord of Lightning", "Lord of the Sea", "Lucky", "Masochist",
        "Mine Foreman", "Motivational Leader", "Musclehead", "Nimble",
        "Positive Thinker", "Power of Gaia", "Pyromaniac", "Runner", "Sadist",
        "Serious", "Spirit Emperor", "Suntan Lover", "Swift",
        "Stronghold Strategist", "Vanguard", "Veil of Darkness", "Waterproof",
        "Workaholic", "Work Slave", "Zen Mind"
    ]

    default_text = "Passive skill"

    # Create droplist to select characteristic
    characteristic_frame = tk.Frame(skills_frame)
    characteristic_frame.grid(row=0, column=0, padx=0, pady=0)

    characteristic_var = tk.StringVar(value=characteristics[0])
    characteristic_combobox = ttk.Combobox(characteristic_frame, values=characteristics,
                                           textvariable=characteristic_var, state="readonly",
                                           height=10, width=20)
    characteristic_combobox.pack(side='left', fill='both', expand=1)

    # Display default text initially
    characteristic_combobox.set(default_text)

    # Create listboxes to display Pals based on the selected characteristic and checkboxes
    listbox_frames = []
    for i in range(4):
        listbox_frame = tk.Frame(skills_frame)
        listbox_frame.grid(row=1, column=i, padx=3, pady=10, sticky="nsew")

        header_text = ["Clean M", "Clean F", "Mixed M", "Mixed F"][i]
        header_label = tk.Label(listbox_frame, text=header_text)
        header_label.pack()

        pals_listbox = tk.Listbox(listbox_frame, height=31, width=22)
        pals_listbox.pack(side='left', fill='both', expand=False)
        listbox_frames.append({'frame': listbox_frame, 'listbox': pals_listbox})

    def update_skills():
        for listbox_frame in listbox_frames:
            listbox_frame['listbox'].delete(0, tk.END)

        selected_characteristic = characteristic_var.get()

        for name in names:
            if any([var.get() for var in checkbox_values[name][selected_characteristic]]):
                for i, checkbox_value in enumerate(checkbox_values[name][selected_characteristic]):
                    if checkbox_value.get() and i < 4:
                        listbox_frames[i]['listbox'].insert(tk.END, name)

    # Update Pals displayed when characteristic changes
    characteristic_var.trace_add('write', lambda *args: update_skills())

    skills_frame.pack()

    return skills_frame


def clear_data():
    for name in checkbox_values:
        for characteristic in checkbox_values[name]:
            for checkbox in checkbox_values[name][characteristic]:
                checkbox.set(0)


def fill_data():
    for name in checkbox_values:
        for characteristic in checkbox_values[name]:
            for checkbox in checkbox_values[name][characteristic]:
                checkbox.set(1)


def create_additional_canvas():
    additional_canvas = tk.Canvas(pals_tab, height=200, width=500)
    additional_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Create 20x10 grid for buttons
    button_width = 17
    button_height = 1

    for i in range(20):
        for j in range(8):
            name_index = i * 8 + j
            if name_index < len(names):
                name = names[name_index]

                button = tk.Button(additional_canvas, text=name, width=button_width, height=button_height)
                button.grid(row=i, column=j, padx=1, pady=1)
                button.bind("<Button-1>", lambda event, name=name: update_characteristics(name))

    additional_canvas.update()


# Create the root window
root = tk.Tk()
root.title("Palworld Manager")
root.maxsize(1350, 600)
root.minsize(1350, 600)
root.geometry("1350x600")

# Create the tabs
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

skills_tab = tk.Frame(notebook)
notebook.add(skills_tab, text="Skills")

pals_tab = tk.Frame(notebook)
notebook.add(pals_tab, text="Pals")

database_tab = tk.Frame(notebook)
# show Database tab - commented out
#notebook.add(database_tab, text="Database")

# Add the Clear and Fill buttons to the database tab
button_frame = tk.Frame(database_tab)
button_frame.pack(side='top', fill='x', padx=10, pady=10)

clear_button = tk.Button(button_frame, text="Clear", command=clear_data)
clear_button.pack(side='left', padx=10, pady=10)

fill_button = tk.Button(button_frame, text="Fill", command=fill_data)
fill_button.pack(side='left', padx=10, pady=10)

# Create the checkboxes and labels
names = ["Anubis", "Arsox", "Astegon", "Azurobe", "Beakon", "Beegarde", "Blazamut", "Blazehowl", "Blazehowl Noct",
         "Boltmane",
         "Bristla", "Broncherry", "Broncherry Aqua", "Bushi", "Caprity", "Cattiva", "Cawgnito", "Celaray", "Chikipi",
         "Chillet",
         "Cinnamoth", "Colossal Whale", "Colossal Wyrm", "Cremis", "Cryolinx", "Daedream", "Dazzi", "Depresso",
         "Digtoise",
         "Dinossom", "Dinossom Lux", "Direhowl", "Dragostrophe", "Dragostrophe's Cousin", "Dumud", "Eikthyrdeer",
         "Eikthyrdeer Terra",
         "Elizabee", "Elphidran", "Elphidran Aqua", "Faleris", "Felbat", "Fenglope", "Flambelle", "Flopie", "Foxcicle",
         "Foxparks",
         "Frostallion", "Frostallion Noct", "Fuack", "Fuddler", "Galeclaw", "Gobfin", "Gobfin Ignis", "Gorirat",
         "Grintale",
         "Grizzbolt", "Gumoss", "Hangyu", "Hangyu Cryst", "Helzephyr", "Hoocrates", "Incineram", "Incineram Noct",
         "Jetragon",
         "Jolthog", "Jolthog Cryst", "Jormuntide", "Jormuntide Ignis", "Katress", "Kelpsea", "Kelpsea Ignis",
         "Killamari", "Kingpaca",
         "Kingpaca Cryst", "Kitsun", "Lamball", "Leezpunk", "Leezpunk Ignis", "Lifmunk", "Loupmoon", "Lovander",
         "Lunaris", "Lyleen",
         "Lyleen Noct", "Mammorest", "Mammorest Cryst", "Maraith", "Mau", "Mau Cryst", "Melpaca", "Menasting",
         "Mossanda",
         "Mossanda Lux", "Mozzarina", "Necromus", "Nitewing", "Nox", "Orserk", "Paladius", "Pengullet", "Penking",
         "Petallia",
         "Pyrin", "Pyrin Noct", "Quivern", "Ragnahawk", "Rayhound", "Reindrix", "Relaxaurus", "Relaxaurus Lux",
         "Reptyro",
         "Reptyro Cryst", "Ribbuny", "Robinquill", "Robinquill Terra", "Rooby", "Rushoar", "Shadowbeak", "Sibelyx",
         "Sparkit",
         "Surfent", "Surfent Terra", "Suzaku", "Suzaku Aqua", "Swee", "Sweepa", "Tanzee", "Teafant", "Tocotoco",
         "Tombat",
         "Univolt", "Vaelet", "Vanwyrm", "Vanwyrm Cryst", "Verdash", "Vixy", "Warsect", "Wixen", "Woolipop", "Wumpo",
         "Wumpo Botan"]

for name in names:
    create_characteristics_frame(name).pack(anchor='w', fill='x', padx=10, pady=10)

# Create the dropdown and buttons for the Pals tab
dropdown_button_frame = tk.Frame(pals_tab)
dropdown_button_frame.pack(fill='x', padx=10, pady=10)

pals_var = tk.StringVar()
pals_var.set("Select Pal")
pals_dropdown = tk.OptionMenu(dropdown_button_frame, pals_var, "SelectxPal")
pals_dropdown.pack(side='left', padx=10, pady=10)

selected_pal_label = tk.Label(dropdown_button_frame, text="", font=("Arial", 14), fg="blue")
selected_pal_label.pack(side='left', padx=10, pady=10)

button_frame = tk.Frame(dropdown_button_frame)
button_frame.pack(side='right')

save_button = tk.Button(button_frame, text="SAVE", command=save_data)
save_button.pack(side='left', padx=10, pady=10)

load_button = tk.Button(button_frame, text="LOAD", command=load_data)
load_button.pack(side='left', padx=10, pady=10)

selected_characteristics = tk.Frame(pals_tab)
selected_characteristics.pack(side='left', fill='both', expand=1, padx=10, pady=10)

populate_dropdown()
load_data()


def on_closing():
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

# Hide the dropdown on the Pals tab
pals_dropdown.pack_forget()

# Create the additional canvas in the "Pals" tab
create_additional_canvas()

# Create the skills frame
skills_frame = create_skills_frame()
skills_frame.pack(anchor='w', fill='x', padx=10, pady=10)

# Add the tabs to the root window
notebook.pack(expand=1, fill='both')

# Start the main event loop
root.mainloop()
