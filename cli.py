import openai
import typer
from rich import print
import json

openai.api_key = "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"

app = typer.Typer()
preset = typer.Typer()
app.add_typer(preset, name="preset")


@app.command()
def init():
    print("\nWelcome to the [bold blue]OpenAI CLI![/bold blue] Type 'exit' to quit.\n")


@app.command()
def exit():
    print('\n[bold red]Exiting...[/bold red]')
    raise typer.Exit()


@preset.command()
def add(
        name: str = typer.Argument(..., help="Name of the preset"),
        engine: str = typer.Argument('...', help='The engine to use for completion.'),
        query: str = typer.Argument('...', help='The prompt to use for completion.'),
        temp: float = typer.Argument(0.5, help="The higher the temperature, the more random the completions."),
        max_t: int = typer.Argument(2048, help="The maximum number of tokens to generate."),
        top_p: float = typer.Argument(1, help="engine considers the results of the tokens with top_p probability mass. "),
        freq_pen: float = typer.Argument(0, help="engine prefers words that were not used recently."),
        pre_pen: float = typer.Argument(0, help="engine prefers completions that have a certain subsequence present.")
        ):
    """Add a preset to the cli to be used later"""

    # assert presets are valid
    if query == "":
        print("Invalid query. Please enter a query.")
        return

    with open("banned.txt", "r") as f:
        banned = f.read().splitlines()
        for word in banned:
            if word in query:
                print(f"Error: query contains banned language. Please remove {word} from your query.")
                return

    assert engine in ["davinci", "curie", "babbage", "ada"], "Invalid engine. Must be davinci, curie, babbage, or ada."

    assert 0 <= temp <= 1, "Temperature must be between 0 and 1."
    assert 0 <= top_p <= 1, "Top_p must be between 0 and 1."
    assert 0 <= freq_pen <= 1, "Frequency penalty must be between 0 and 1."
    assert 0 <= pre_pen <= 1, "Presence penalty must be between 0 and 1."

    match engine:
        case "davinci":
            assert max_t <= 4000, "Maximum tokens must be <= 4000."
        case "curie" | "babbage" | "ada":
            assert max_t <= 2048, "Maximum tokens must be <= 2048."

    with open("presets.json", "r") as f:
        presets = json.load(f)

        if name in presets:
            print(f"Error: preset {name} already exists. Please choose a different name.")
            return

        presets[name] = {
            "engine": engine,
            "query": query,
            "temp": temp,
            "max_t": max_t,
            "top_p": top_p,
            "freq_pen": freq_pen,
            "pre_pen": pre_pen
        }

        with open("presets.json", "w") as f:
            json.dump(presets, f, indent=4)
            print(f"Added preset[blue] {name} [/blue]to presets.json")

@preset.command()
def list():
    """List all presets in presets.json"""
    with open("presets.json", "r") as f:
        presets = json.load(f)
        for preset in presets:
            # print preset attributes neatly
            print(f"[bold blue]{preset}[/bold blue]")
            for key, value in presets[preset].items():
                print(f"{key}: {value}")
            print()

@preset.command()
def delete(name: str = typer.Argument(..., help="Name of the preset to delete")):
    """Delete a preset from presets.json"""
    with open("presets.json", "r") as f:
        presets = json.load(f)
        if name in presets:
            del presets[name]
            with open("presets.json", "w") as f:
                json.dump(presets, f, indent=4)
                print(f"Deleted preset[blue] {name} [/blue]from presets.json")
        else:
            print(f"Error: preset {name} does not exist.")


@app.command()
def complete(name: str = typer.Argument(..., help="Use preset to generate text completion")):
    """Use a preset to generate text"""
    with open('presets.json', 'r') as f:
        presets = json.load(f)

    try:
        preset = presets[name]
    except KeyError:
        print(f"[bold red]Preset {name} not found.[/bold red]")
        return

    response = openai.Completion.create(
        engine=preset['engine'],
        prompt=preset['query'],
        temperature=preset['temp'],
        max_tokens=preset['max_t'],
        top_p=preset['top_p'],
        frequency_penalty=preset['freq_pen'],
        presence_penalty=preset['pre_pen']
    )

    print(response['choices'][0]['text'])



if __name__ == "__main__":
    app()
