import typer, json, datetime, webbrowser, random, string, os, csv, toml
from rich import print
from rich.table import Table

bm = typer.Typer()


@bm.command()
def init():
    """Initialize  CLI"""
    os.system("cls" if os.name == "nt" else "clear")

    print("\nWelcome to [bold blue]Bookmarkr[/bold blue], the CLI bookmark tool! Type 'exit' to quit.\n")


@bm.command()
def exit():
    """Exit CLI"""
    os.system("cls" if os.name == "nt" else "clear")

    print('\n[bold red]Exiting...[/bold red]')
    raise typer.Exit()


@bm.command()
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
                print(f"\n[red]Error [/red]: name contains banned language. Please remove[red] {word}[/red] from the name.\n")
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
            "last modified": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

        with open("bookmarks.json", "w") as f:
            json.dump(bms, f, indent=4)
            print(f"\nAdded bookmark[blue] {name} [/blue]\n")


@bm.command()
def list():
    """List all bookmarks in table view"""
    os.system("cls" if os.name == "nt" else "clear")

    # create rich table for all bookmarks
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID",  width=10)
    table.add_column("Name",  width=12)
    table.add_column("URL",  width=30)
    table.add_column("Tag",  width=12)
    table.add_column("Last Modified",  width=20)

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


@bm.command()
def delete(name: str = typer.Argument(..., help="Name of the bookmark to delete")):
    """Delete a bookmark from bookmarks.json"""
    os.system("cls" if os.name == "nt" else "clear")

    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        if name in bms:
            del bms[name]
            with open("bookmarks.json", "w") as f:
                json.dump(bms, f, indent=4)
                print(f"\nDeleted bookmark[blue] {name} [/blue]\n")
        else:
            print(f" \n[red]Error[/red]: bookmark {name} does not exist.\n")


@bm.command()
def view(name: str = typer.Argument(..., help="Name of the bm to open")):
    """Open a bookmark in the browser"""

    os.system("cls" if os.name == "nt" else "clear")

    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        if name in bms:
            webbrowser.open(bms[name]["url"])
        else:
            print(f" \n[red]Error[/red]: bookmark {name} does not exist.\n")


@bm.command()
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


@bm.command()
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
            with open("bookmarks.json", "w") as f:
                json.dump(bms, f, indent=4)
                print(f"\nUpdated bookmark [blue] {name} [/blue]\n")
        else:
            print(f" \n[red]Error[/red]: bookmark {name} does not exist.\n")


@bm.command()
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


@bm.command()
def export_csv():
    """Export bookmarks to a CSV file"""
    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        with open("bookmarks.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "URL", "Tag", "Last Modified"])
            for bm in bms.values():
                writer.writerow([bm["id"], bm["name"], bm["url"], bm["tag"], bm["last modified"]])

        print("\nExported bookmarks to bookmarks.csv\n")


@bm.command()
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

        with open("bookmarks.json", "w") as f:
            json.dump(bms, f, indent=4)
            print("\nImported bookmarks from [yellow]bookmarks.csv[/yellow]\n")


@bm.command()
def import_json():
    """Import bookmarks from a JSON file"""
    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        with open("bookmarks.json", "w") as f:
            json.dump(bms, f, indent=4)

        print("\nImported bookmarks from [yellow]bookmarks.json[/yellow]\n")



if __name__ == "__main__":
    bm()
