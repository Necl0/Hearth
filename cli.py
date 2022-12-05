import openai
import typer
from rich import print
from typing import Optional

openai.api_key = "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"

app = typer.Typer()

def main(engine: str,
         query: str,
         temp: float = typer.Argument(0.5, help="The higher the temperature, the more random the completions. Try 0.9 for more adventurous completions."),
         max_t: int = typer.Argument(2048, help="The maximum number of tokens to generate. The default is 2048 for curie, babbage, and ada. 4000 for davinci."),
         top_p: float = typer.Argument(1),
         freq_pen :float = typer.Argument(0),
         pre_pen: float = typer.Argument(0)) -> None:

    """Use OpenAI's ChatGPT engine to generate text.

    Args:
    - engine (str): The engine to use. Can be davinci, curie, babbage, or ada.
    - query (str): The prompt to use.
    - temp (float): The temperature to use.
    - max_t (int): The maximum number of tokens to generate.
    - top_p (float): The top_p to use.
    - freq_pen (float): The frequency penalty to use.
    - pre_pen (float): The presence penalty to use.

    """


    assert engine in ["davinci", "curie", "babbage", "ada"], "Invalid engine. Must be davinci, curie, babbage, or ada."
    assert 0 <= temp <= 1, "Temperature must be between 0 and 1."
    assert 0 <= top_p <= 1, "Top_p must be between 0 and 1."
    assert 0 <= freq_pen <= 1, "Frequency penalty must be between 0 and 1."
    assert 0 <= pre_pen <= 1, "Presence penalty must be between 0 and 1."

    match engine:
        case "davinci":
            assert max_t <= 4000, "Maximum tokens must be less than or equal to 4000."
        case "curie":
            assert max_t <= 2048, "Maximum tokens must be less than or equal to 2048."
            engine_id = "curie-instruct-beta"
        case "babbage":
            assert max_t <= 2048, "Maximum tokens must be less than or equal to 2048."
            engine_id = "babbage"
        case "ada":
            assert max_t <= 2048, "Maximum tokens must be less than or equal to 2048."
            engine_id = "ada"


    # validate query is correct
    if query == "":
        print("Invalid query. Please enter a query.")
        return


    response = openai.Completion.create(
        engine=engine_id,
        prompt=query,
        temperature=temp,
        max_tokens=max_t,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pre_pen,
        stop=["\n", " Human:", " AI:"]
    )

    print("Query:", query)
    if (query.lower().strip() == 'exit'):
        print('\n[bold red]Exiting...[/bold red]')
        exit()

    print(response["choices"][0]["text"])



if __name__ == "__main__":
    print(r"""Welcome to the OpenAI CLI! Type 'exit' to quit.\n
     [oo]
    /|##|\
     d  b""")
    typer.run(main)