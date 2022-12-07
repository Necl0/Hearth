import typer
import json
import datetime
import webbrowser
import random
import string
import os
import csv
import requests
import psutil
import platform
import chrome_bookmarks
import shutil
from datetime import datetime
from rich import print
from rich.table import Table

app = typer.Typer()

bm = typer.Typer(help="Bookmark manager")
jl = typer.Typer(help="Journal manager")
todo = typer.Typer(help="Todo manager")
notes = typer.Typer(help="Notes manager")

app.add_typer(bm, name="bm")
app.add_typer(jl, name="jl")
app.add_typer(todo, name="todo")
app.add_typer(notes, name="notes")


### Root commands ###
@app.command("home")
def init():
    """Initialize CLI"""
    os.system("cls" if os.name == "nt" else "clear")

    print(f"""\nWelcome to [bold red underline]Hearth[/bold red underline], a CLI tool that allows you to manage your bookmarks, journal,
todo list, and give you the feel of a home Notion page, but in the terminal!\n

    Commands:
    [bold blue]home[/bold blue] - Home page
    [bold blue]exit[/bold blue] - Exit Hearth
    [bold blue]bm[/bold blue] - Bookmark manager
    [bold blue]jl[/bold blue] - Journal manager
    [bold blue]todo[/bold blue] - Todo list manager
    [bold blue]notes[/bold blue] - Notes manager
    [bold blue]quote[/bold blue] - Get a random motivational quote
    [bold blue]weather[/bold blue] - Get the weather for your location
    [bold blue]sysinfo[/bold blue] - Get system information
    
    \n""")


@app.command("exit")
def exit():
    """Exit CLI"""
    os.system("cls" if os.name == "nt" else "clear")

    print('\n[bold red]Exiting...[/bold red]')
    raise typer.Exit()


@app.command("quote")
def quote():
    """Get an inspirational quote"""
    os.system("cls" if os.name == "nt" else "clear")

    response = requests.get("https://zenquotes.io/api/random")
    json_data = response.json()
    print(f"\n[i]{json_data[0]['q']}[/i] - [b]{json_data[0]['a']}[/b]\n")


@app.command("weather")
def weather():
    """Get current weather"""
    os.system("cls" if os.name == "nt" else "clear")

    response = requests.get(
        "http://api.weatherapi.com/v1/forecast.json?key=bb697f97081f43a3bf642927220612&q=Rockville&days=1&aqi=no&alerts=no")

    json_data = response.json()
    print(f"""\nCurrent weather in [b]{json_data['location']['name']}, {json_data['location']['region']}[/b]:\n
    [b]Temperature:[/b] {json_data['current']['temp_f']}°F
    [b]Feels like:[/b] {json_data['current']['feelslike_f']}°F
    [b]Condition:[/b] {json_data['current']['condition']['text']}
    [b]Wind:[/b] {json_data['current']['wind_mph']} mph {json_data['current']['wind_dir']}
    [b]Humidity:[/b] {json_data['current']['humidity']}%\n""")


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


@app.command("sysinfo")
def System_information():
    print("\n", "=" * 40, "System Information", "=" * 40)
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Version: {uname.version}")

    # print CPU information
    print("=" * 40, "CPU Info", "=" * 40)
    # number of cores
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Total cores:", psutil.cpu_count(logical=True))

    print(f"Total CPU Usage: {psutil.cpu_percent()}%")

    # Memory Information
    print("=" * 40, "Memory Information", "=" * 40)
    # get the memory details
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")

    # Disk Information
    print("=" * 40, "Disk Information", "=" * 40)
    print("Partitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Device: {partition.device} ===")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        print(f"  Total Size: {get_size(partition_usage.total)}")
        print(f"  Used: {get_size(partition_usage.used)}")
        print(f"  Free: {get_size(partition_usage.free)}")
        print(f"  Percentage: {partition_usage.percent}%")


### Bookmark Manager ###
@bm.command("add")
def add(
        name: str = typer.Argument(..., help="Name of the bookmark"),
        url: str = typer.Argument(..., help="bookmark URL"),
        tag: str = typer.Argument(..., help="Tag for the bookmark")
):
    """Add a bookmark to the cli to be used later"""
    os.system("cls" if os.name == "nt" else "clear")

    if name == "":
        print("Invalid name. Please enter a name.")
        return

    with open("banned.txt", "r") as f:
        banned = f.read().splitlines()
        for word in banned:
            if word in name:
                print(
                    f"\n[red]Error [/red]: name contains banned language. Please remove[red] {word}[/red] from the name.\n")
                return

    with open("bookmarks.json", "r") as f:
        bms = json.load(f)

        if name in bms:
            print(f"\n[red] Error [/red]: bookmark {name} already exists. Please choose a different name.\n")
            return

        bms[name] = {
            "id": "".join(random.choices(string.ascii_lowercase + string.digits, k=10)),
            "name": name,
            "url": url,
            "tag": tag,
            "last modified": datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        }

        with open("bookmarks.json", "w") as c:
            json.dump(bms, c, indent=4)
            print(f"\nAdded bookmark[blue] {name} [/blue]\n")


@bm.command("list")
def list():
    """List all bookmarks in table view"""
    os.system("cls" if os.name == "nt" else "clear")

    # create rich table for all bookmarks
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", width=10)
    table.add_column("Name", width=12)
    table.add_column("URL", width=30)
    table.add_column("Tag", width=12)
    table.add_column("Last Modified", width=20)

    with open("bookmarks.json", "r") as f:
        bms = json.load(f)

        for bm in bms:
            table.add_row(
                bms[bm]["id"],
                bms[bm]["name"],
                bms[bm]["url"],
                bms[bm]["tag"],
                bms[bm]["last modified"]
            )

    print(table)


@bm.command("delete")
def delete(name: str = typer.Argument(..., help="Name of the bookmark to delete")):
    """Delete a bookmark from bookmarks.json"""
    os.system("cls" if os.name == "nt" else "clear")

    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        if name in bms:
            del bms[name]
            with open("bookmarks.json", "w") as c:
                json.dump(bms, c, indent=4)
                print(f"\nDeleted bookmark[blue] {name} [/blue]\n")
        else:
            print(f" \n[red]Error[/red]: bookmark {name} does not exist.\n")


@bm.command("view")
def view(name: str = typer.Argument(..., help="Name of the bm to open")):
    """Open a bookmark in the browser"""

    os.system("cls" if os.name == "nt" else "clear")

    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        if name in bms:
            webbrowser.open(bms[name]["url"])
        else:
            print(f" \n[red]Error[/red]: bookmark {name} does not exist.\n")


@bm.command("search")
def search(query: str = typer.Argument(..., help="Query to search for")):
    """Search for a bookmark"""

    os.system("cls" if os.name == "nt" else "clear")

    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        for bm in bms:
            if query in bm:
                print(f"\nFound bookmark [bold blue]{bm}[/bold blue]")
                for key, value in bms[bm].items():
                    print(f"{key}: {value}")

                print()
                return

    print(f"\n No bookmark found for query [bold blue]{query} [/bold blue]\n")


@bm.command("update")
def update(name: str = typer.Argument(..., help="Name of the bm to update")):
    """Update a bookmark"""

    os.system("cls" if os.name == "nt" else "clear")

    # update a bm
    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        if name in bms:
            print(f"Updating bookmark [blue] {name} [/blue]")
            url = typer.prompt("Enter new URL")
            tag = typer.prompt("Enter new tag")
            bms[name]["url"] = url
            bms[name]["tag"] = tag
            with open("bookmarks.json", "w") as c:
                json.dump(bms, c, indent=4)
                print(f"\nUpdated bookmark [blue] {name} [/blue]\n")
        else:
            print(f" \n[red]Error[/red]: bookmark {name} does not exist.\n")


@bm.command("clear")
def clear():
    """Clear all bookmarks"""

    os.system("cls" if os.name == "nt" else "clear")

    # check if you want to proceed
    print("""\nAre you sure you want to clear all bookmarks? [bold red]This cannot be undone.[/bold red]
    Type [bold blue]yes[/bold blue] to proceed or [bold blue]no[/bold blue] to cancel.\n""")

    if input("    >>> ").lower().strip() == "yes":
        with open("bookmarks.json", "w") as f:
            json.dump({}, f, indent=4)
            print("Cleared bookmarks")


@bm.command("export-csv")
def export_csv():
    """Export bookmarks to a CSV file"""
    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        with open("bookmarks.csv", "w", newline="") as c:
            writer = csv.writer(c)
            writer.writerow(["ID", "Name", "URL", "Tag", "Last Modified"])
            for bm in bms.values():
                writer.writerow([bm["id"], bm["name"], bm["url"], bm["tag"], bm["last modified"]])

        print("\nExported bookmarks to bookmarks.csv\n")


@bm.command("import-csv")
def import_csv():
    """Import bookmarks from a CSV file"""
    with open("bookmarks.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        bms = {}
        for row in reader:
            bms[row[1]] = {
                "id": row[0],
                "name": row[1],
                "url": row[2],
                "tag": row[3],
                "last modified": row[4]
            }

        with open("bookmarks.json", "w") as c:
            json.dump(bms, c, indent=4)
            print("\nImported bookmarks from [yellow]bookmarks.csv[/yellow]\n")


@bm.command("import-json")
def import_json():
    """Import bookmarks from a JSON file"""
    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        with open("bookmarks.json", "w") as c:
            json.dump(bms, c, indent=4)

        print("\nImported bookmarks from [yellow]bookmarks.json[/yellow]\n")


@bm.command("import-google")
def import_google():
    """Import bookmarks from Google Chrome"""

    count = 0

    for url in chrome_bookmarks.urls:
        count += 1
        # add bookmark to bookmarks.json along with unique id
        with open("bookmarks.json", "r") as f:
            bms = json.load(f)
            bms[url.name] = {
                "id": "".join(random.choices(string.ascii_lowercase + string.digits, k=10)),
                "name": url.name,
                "url": url.url,
                "tag": "*imported*",
                "last modified": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }

            with open("bookmarks.json", "w") as c:
                json.dump(bms, c, indent=4)

    print(f"\nImported {count} bookmarks from [yellow]Google Chrome[/yellow]\n")


### Journal Manager ###
@jl.command("add")
def add():
    """Add a journal entry"""
    os.system("cls" if os.name == "nt" else "clear")

    date = datetime.datetime.now().strftime("%m/%d/%Y")
    time = datetime.datetime.now().strftime("%I:%M %p")

    title = typer.prompt("Enter the title of the entry")
    entry = typer.prompt("Enter the entry\n")

    # add the entry to the journal
    with open("journal.json", "r") as f:
        journal = json.load(f)
        journal[date] = {
            "time": time,
            "title": title,
            "entry": entry
        }

        with open("journal.json", "w") as c:
            json.dump(journal, c, indent=4)

    print(f"Added entry [blue bold]{title}[/blue bold] to journal")


@jl.command("view")
def view(date: str = typer.Argument(..., help="Date of the entry to view")):
    """View a journal entry"""
    os.system("cls" if os.name == "nt" else "clear")

    with open("journal.json", "r") as f:
        journal = json.load(f)
        if date in journal:
            print(f" \n[blue]{journal[date]['title']}[/blue] - {date} {journal[date]['time']}\n")
            print(journal[date]["entry"], "\n")
        else:
            print(f" \n[red]Error[/red]: entry for {date} does not exist.\n")


@jl.command("search")
def search(query: str = typer.Argument(..., help="Query to search for")):
    """Search for a journal entry by title"""
    os.system("cls" if os.name == "nt" else "clear")

    with open("journal.json", "r") as f:
        journal = json.load(f)
        for entry in journal:
            if query in journal[entry]["title"]:
                print(f"\nFound entry [blue]{journal[entry]['title']}[/blue] - {entry} {journal[entry]['time']}\n")
                print(journal[entry]["entry"], "\n")
                return
            else:
                print(f"\n No entry found for query [bold blue]{query} [/bold blue]\n")


@jl.command("delete")
def delete(title: str = typer.Argument(..., help="title of the entry to delete")):
    """Delete a journal entry by title"""
    # delete an entry
    os.system("cls" if os.name == "nt" else "clear")

    with open("journal.json", "r") as f:
        journal = json.load(f)

        for entry in journal:
            if title == journal[entry]["title"]:
                print(f"Are you sure you want to delete [bold blue]{title}[/bold blue]? This cannot be undone.")

                if input(
                        "Type [bold blue]yes[/bold blue] to proceed or [bold blue]no[/bold blue] to cancel.\n\n>>> ").lower().strip() == "yes":
                    del journal[entry]
                    with open("journal.json", "w") as c:
                        json.dump(journal, c, indent=4)
                        print(f"Deleted entry [blue]{title}[/blue] from journal.\n")
                        return

        print(f"\n[red]Error[/red]: entry {title} does not exist.\n")


@jl.command("list")
def table_view():
    """View journal entries in a table"""
    os.system("cls" if os.name == "nt" else "clear")

    with open("journal.json", "r") as f:
        journal = json.load(f)
        table = Table()

        table.add_column("Date", justify="center", style="cyan")
        table.add_column("Time", justify="center", style="cyan")
        table.add_column("Title", justify="center", style="cyan")
        table.add_column("Entry", justify="center", style="cyan")

        for entry in journal:
            table.add_row(entry, journal[entry]["time"], journal[entry]["title"], journal[entry]["entry"])

        print(table)


### TODO Manager ###
@todo.command("add")
def add():
    """Add a todo"""
    os.system("cls" if os.name == "nt" else "clear")

    title = typer.prompt("Enter the title of the todo")
    description = typer.prompt("Enter the description of the todo")

    # add the todo to the list
    with open("todo.json", "r") as f:
        todo = json.load(f)
        todo[title] = {
            "title": title,
            "description": description,
            "completed": "false"
        }

        with open("todo.json", "w") as c:
            json.dump(todo, c, indent=4)

    print(f"Added todo [blue bold]{title}[/blue bold] to todo list")


@todo.command("complete")
def complete(title: str = typer.Argument(..., help="Title of the todo to complete")):
    """Complete a todo"""
    os.system("cls" if os.name == "nt" else "clear")

    with open("todo.json", "r") as f:
        todo = json.load(f)

        for item in todo:
            if title == todo[item]["title"]:
                todo[item]["completed"] = "true"
                with open("todo.json", "w") as c:
                    json.dump(todo, c, indent=4)
                    print(f"Completed todo [blue]{title}[/blue].\n")
                    return

        print(f"\n[red]Error[/red]: todo {title} does not exist.\n")


@todo.command("delete")
def delete(title: str = typer.Argument(..., help="Title of the todo to delete")):
    """Delete a todo"""
    os.system("cls" if os.name == "nt" else "clear")

    with open("todo.json", "r") as f:
        todo = json.load(f)

        for item in todo:
            if title == todo[item]["title"]:
                del todo[item]
                with open("todo.json", "w") as c:
                    json.dump(todo, c, indent=4)
                    print(f"Deleted todo [blue]{title}[/blue].\n")
                    return

        print(f"\n[red]Error[/red]: todo {title} does not exist.\n")


@todo.command("list")
def table_view():
    """View todo list in a table"""
    os.system("cls" if os.name == "nt" else "clear")

    with open("todo.json", "r") as f:
        todo = json.load(f)
        table = Table()

        table.add_column("Title", justify="center", style="cyan")
        table.add_column("Description", justify="center", style="cyan")
        table.add_column("Completed", justify="center", style="cyan")

        for item in todo:
            table.add_row(todo[item]["title"], todo[item]["description"], todo[item]["completed"])

        print(table)


### Notes Manager ###
@notes.command("add")
def create_page(directory):
    """Create a new note page"""
    os.system("cls" if os.name == "nt" else "clear")

    title = typer.prompt("Enter the title of the page")

    # create the page
    with open(f"{directory}/{title}.txt", "w") as f:
        f.write("")

    print(f"Created page [blue bold]{title}[/blue bold] in {directory}.\n")


@notes.command("edit")
def edit_page(title: str = typer.Argument(..., help="Title of the note page to edit")):
    """Edit a note page"""
    os.system("cls" if os.name == "nt" else "clear")

    # edit page after searching all directories to find it
    for directory in os.listdir():
        if os.path.isdir(directory):
            for file in os.listdir(directory):
                if file == f"{title}.txt":
                    os.system(f"notepad {directory}/{file}")
                    return


@notes.command("view")
def view_page(title: str = typer.Argument(..., help="Title of the note page to view")):
    """View a note page"""
    os.system("cls" if os.name == "nt" else "clear")

    # search all directories for the page
    for file in os.listdir():
        if os.path.isdir(file):
            for page in os.listdir(file):
                if page == f"{title}.txt":
                    # open the page
                    with open(f"{file}/{page}", "r") as f:
                        print("[bold red]File contents [/bold red]:\n")
                        print(f.read() + "\n")
                    return


@notes.command("search")
def search_pages(query: str = typer.Argument(..., help="Query to search for")):
    """Search for a note page"""
    os.system("cls" if os.name == "nt" else "clear")

    # search all directories for the page
    for file in os.listdir():
        if os.path.isdir(file):
            for page in os.listdir(file):
                if page == f"{query}.txt":
                    print(f"Found page [blue bold]{page}[/blue bold] in directory [yellow]{file}[/yellow].\n")
                    return


@notes.command("mkdir")
def create_dir(name: str = typer.Argument(..., help="Name of the directory to create")):
    """Create a new directory"""
    os.system("cls" if os.name == "nt" else "clear")

    if not os.path.exists(name):
        os.mkdir(name)
        print(f"Created directory [blue]{name}[/blue].\n")
    else:
        print(f"\n[red]Error[/red]: directory {name} already exists.\n")


@notes.command("rmdir")
def delete_dir(name: str = typer.Argument(..., help="Name of the directory to delete")):
    """Delete a directory"""
    os.system("cls" if os.name == "nt" else "clear")

    # search through all directories to find the one to delete
    for directory in os.listdir():
        if os.path.isdir(directory):
            if directory == name:
                os.rmdir(directory)
                print(f"Deleted directory [blue]{name}[/blue].\n")


@notes.command("mv")
def move_file(file: str = typer.Argument(..., help="Name of the file to move"),
              dest: str = typer.Argument(..., help="Name of the destination directory")):
    """Move a file to a different directory"""
    os.system("cls" if os.name == "nt" else "clear")

    # search through all directories for file
    for directory in os.listdir():
        if os.path.isdir(directory):
            for page in os.listdir(directory):
                if page == f"{file}.txt":
                    os.rename(f"{directory}/{page}", f"{dest}/{page}")
                    print(f"Moved page [blue bold]{page}[/blue bold] to directory [yellow]{dest}[/yellow].\n")
                    return


@notes.command("rm")
def remove_file(title: str = typer.Argument(..., help="Name of the file to remove")):
    """Remove a file"""
    os.system("cls" if os.name == "nt" else "clear")

    # search all directories for file to remove
    for directory in os.listdir():
        if os.path.isdir(directory):
            for file in os.listdir(directory):
                if file == f"{title}.txt":
                    os.remove(f"{directory}/{file}")
                    print(f"Removed notes file [blue]{title}.txt[/blue].\n")
                    return


@notes.command("rename")
def rename_file(file: str = typer.Argument(..., help="Name of the file to rename")):
    """Rename a file"""
    os.system("cls" if os.name == "nt" else "clear")

    # search all directories for file and rename it
    for directory in os.listdir():
        if os.path.isdir(directory):
            for page in os.listdir(directory):
                if page == f"{file}.txt":
                    new_name = typer.prompt("Enter the new name for the file")
                    os.rename(f"{directory}/{page}", f"{directory}/{new_name}.txt")
                    print(f"Renamed file [blue]{page}[/blue] to [blue]{new_name}.txt[/blue].\n")
                    return


@notes.command("tree")
def print_tree():
    """Print the directory tree"""
    os.system("cls" if os.name == "nt" else "clear")

    # print all directories and if they contain note files, print them in tree like fashion, indent=4
    for directory in os.listdir():
        if os.path.isdir(directory):
            # if file isnt venv, pycache, or idea

            if directory not in ("venv", ".idea", "__pycache__"):
                print(f"[blue bold]{directory}[/blue bold]")
                for file in os.listdir(directory):
                    if file.endswith(".txt"):
                        print(f"--- [blue]{file}[/blue]")


if __name__ == "__main__":
    app()
