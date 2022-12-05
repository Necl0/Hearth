import openai
import typer
from rich import print
from typing import Optional

openai.api_key = "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"

app = typer.Typer()


def main(
         engine: str = typer.Argument('...', help='The engine to use for completion.'),
         query: str = typer.Argument('...', help='The prompt to use for completion.'),
         temp: float = typer.Argument(0.5, help="The higher the temperature, the more random the completions. Try 0.9 for more adventurous completions."),
         max_t: int = typer.Argument(2048, help="The maximum number of tokens to generate. The default is 2048 for curie, babbage, and ada. 4000 for davinci."),
         top_p: float = typer.Argument(1, help="engine considers the results of the tokens with top_p probability mass. "),
         freq_pen: float = typer.Argument(0, help="engine prefers words that were not used recently."),
         pre_pen: float = typer.Argument(0, help="engine prefers completions that have a certain subsequence present."),
        ) -> None:

    """Use OpenAI's engines to generate text.

    Args:
    - engine (str): The engine to use. Can be davinci, curie, babbage, or ada.
    - query (str): The prompt to use.
    - temp (float): The temperature to use.
    - max_t (int): The maximum number of tokens to generate.
    - top_p (float): The top_p to use.
    - freq_pen (float): The frequency penalty to use.
    - pre_pen (float): The presence penalty to use.

    """

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

    response = openai.Completion.create(
        engine=engine,
        prompt=query,
        temperature=temp,
        max_tokens=max_t,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pre_pen,
        stop=["\n", " Human:", " AI:"]
    )

    if query.lower().strip() == 'exit':
        print('\n[bold red]Exiting...[/bold red]')
        exit()

    print(response["choices"][0]["text"])


if __name__ == "__main__":
    print(r"""Welcome to the OpenAI CLI! Type 'exit' to quit.\n
     [oo]
    /|##|\
     d  b""")
    typer.run(main)
