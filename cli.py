import typer
from rich import print
import json
import datetime
import webbrowser

app = typer.Typer()
bm = typer.Typer()
app.add_typer(bm, name="bm")


@app.command()
def init():
    print("\nWelcome to [bold blue]Nota[/bold blue], the CLI bm tool! Type 'exit' to quit.\n")


@app.command()
def exit():
    print('\n[bold red]Exiting...[/bold red]')
    raise typer.Exit()


@bm.command()
def add(
        name: str = typer.Argument(..., help="Name of the bookmark"),
        url: str = typer.Argument(..., help="bookmark URL"),
        tag: str = typer.Argument(..., help="Tag for the bookmark")
        ):
    """Add a bookmark to the cli to be used later"""

    if name == "":
        print("Invalid name. Please enter a name.")
        return

    with open("banned.txt", "r") as f:
        banned = f.read().splitlines()
        for word in banned:
            if word in name:
                print(f"Error: query contains banned language. Please remove {word} from your query.")
                return

    with open("bookmarks.json", "r") as f:
        bms = json.load(f)

        if name in bms:
            print(f"Error: bookmark {name} already exists. Please choose a different name.")
            return

        bms[name] = {
            "name": name,
            "url": url,
            "tag": tag,
            "last modified": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

        with open("bookmarks.json", "w") as f:
            json.dump(bms, f, indent=4)
            print(f"Added bookmark [blue] {name} [/blue]to bookmarks.json")


@bm.command()
def list():
    """List all bms"""
    with open("bookmarks.json", "r") as f:
        bms = json.load(f)

        print("\n[bold red]Bookmarks[/bold red]\n")

        for bm in bms:
            print(f"[bold blue]{bm}[/bold blue]")
            for key, value in bms[bm].items():
                print(f"{key}: {value}")
            print()

@bm.command()
def delete(name: str = typer.Argument(..., help="Name of the bm to delete")):
    """Delete a bm from bookmarks.json"""
    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        if name in bms:
            del bms[name]
            with open("bookmarks.json", "w") as f:
                json.dump(bms, f, indent=4)
                print(f"Deleted bm[blue] {name} [/blue]from bookmarks.json")
        else:
            print(f"Error: bookmark {name} does not exist.")

@bm.command()
def view(name: str = typer.Argument(..., help="Name of the bm to open")):
    """Open a bookmark in the browser"""
    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        if name in bms:
            webbrowser.open(bms[name]["url"])
        else:
            print(f"Error: bookmark {name} does not exist.")


@bm.command()
def search(query: str = typer.Argument(..., help="Query to search for")):
    """Search for a bookmark"""

    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        for bm in bms:
            if query in bm:
                print(f"\nFound bookmark [bold blue]{bm}[/bold blue]")
                for key, value in bms[bm].items():
                    print(f"{key}: {value}")

                print()
                return

    print(f"\nNo bookmark found for query [bold blue]{query} [/bold blue]\n")

@bm.command()
def update(name: str = typer.Argument(..., help="Name of the bm to update")):
    """Update a bookmark"""

    # update a bm
    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        if name in bms:
            print(f"Updating bookmark [blue] {name} [/blue]")
            url = input("Enter new URL: ")
            tag = input("Enter new tag: ")
            bms[name]["url"] = url
            bms[name]["tag"] = tag
            with open("bookmarks.json", "w") as f:
                json.dump(bms, f, indent=4)
                print(f"Updated bookmark [blue] {name} [/blue]to bookmarks.json")
        else:
            print(f"Error: bookmark {name} does not exist.")

@bm.command()
def clear():
    """Clear all bookmarks"""

    # check if you want to proceed
    print("Are you sure you want to clear all bookmarks? [bold red]This cannot be undone.[/bold red]")
    print("Type [bold blue]yes[/bold blue] to proceed.")

    if input().lower().strip() == "yes":
        with open("bookmarks.json", "w") as f:
            json.dump({}, f, indent=4)
            print("Cleared bookmarks")

@bm.command()
def count():
    """Count the number of bookmarks"""
    with open("bookmarks.json", "r") as f:
        bms = json.load(f)
        print(f"\nNumber of bookmarks: [bold yellow]{len(bms)}[/bold yellow]\n")


if __name__ == "__main__":
    app()
