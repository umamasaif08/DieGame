import random
import time

from art import text2art
from colorama import Fore, Style, init as colorama_init
from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


# Initialize Colorama so terminal color touches work on Windows too.
colorama_init(autoreset=True)
console = Console()

# The original ASCII art faces, reused for any number of dice from 1 to 6.
dice_faces = {
    1: [" ----- ", "|     |", "|  o  |", "|     |", " ----- "],
    2: [" ----- ", "| o   |", "|     |", "|   o |", " ----- "],
    3: [" ----- ", "| o   |", "|  o  |", "|   o |", " ----- "],
    4: [" ----- ", "| o o |", "|     |", "| o o |", " ----- "],
    5: [" ----- ", "| o o |", "|  o  |", "| o o |", " ----- "],
    6: [" ----- ", "| o o |", "| o o |", "| o o |", " ----- "],
}


def show_title() -> None:
    """Display the game's title and a compact welcome panel."""
    title = text2art("DICE ROLLER", font="small")
    console.print(Align.center(Text(title, style="bold bright_cyan")))
    console.print(
        Panel(
            Align.center("Roll your luck. Track your streak. Have fun!", vertical="middle"),
            border_style="bright_yellow",
            box=box.DOUBLE,
            padding=(0, 2),
        )
    )
    print(Fore.CYAN + "  Welcome to Dice Roller!" + Style.RESET_ALL)


def make_dice_display(values: list[int]) -> Group:
    """Build colored, side-by-side Rich lines for all rolled dice."""
    lines = []
    for row in range(len(dice_faces[1])):
        line = Text()
        for index, value in enumerate(values):
            if index:
                line.append("   ")
            line.append(dice_faces[value][row], style="bold bright_white")
        lines.append(line)
    return Group(*lines)


def animate_roll(number_of_dice: int) -> None:
    """Show a short rolling animation before revealing the final values."""
    frames = ([1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1])
    with Live(console=console, refresh_per_second=12, transient=True) as live:
        for step in range(8):
            preview = [frames[step % 2][(step + index) % 6] for index in range(number_of_dice)]
            live.update(
                Panel(
                    make_dice_display(preview),
                    title="[bold yellow]Rolling...[/bold yellow]",
                    border_style="yellow",
                    box=box.ROUNDED,
                )
            )
            time.sleep(0.08)


def lucky_message(total: int, number_of_dice: int) -> tuple[str, str]:
    """Return a friendly message based on the result."""
    maximum = number_of_dice * 6
    if total == maximum:
        return "JACKPOT!", "bold bright_yellow"
    if total >= number_of_dice * 4:
        return "Lucky roll!", "bold bright_green"
    if total <= number_of_dice * 2:
        return "Tough luck this time.", "bold bright_red"
    return "A solid roll!", "bold bright_cyan"


def roll_dice(number_of_dice: int) -> int:
    """Roll, display, and summarize a group of dice."""
    animate_roll(number_of_dice)
    values = [random.randint(1, 6) for _ in range(number_of_dice)]
    total = sum(values)
    message, message_style = lucky_message(total, number_of_dice)

    console.print(
        Panel(
            make_dice_display(values),
            title="[bold bright_cyan]Your Dice[/bold bright_cyan]",
            subtitle=f"[bold white]Total: {total}[/bold white]",
            border_style="bright_cyan",
            box=box.DOUBLE,
            padding=(1, 2),
        )
    )
    console.print(Align.center(Text(message, style=message_style)))
    return total


def ask_for_dice() -> int | None:
    """Read a valid dice count, returning None when the user cancels."""
    while True:
        try:
            answer = console.input("\n[bold yellow]How many dice?[/bold yellow] [dim](1-6, or q to cancel)[/dim] ")
        except (EOFError, KeyboardInterrupt):
            return None
        if answer.strip().lower() == "q":
            return None
        try:
            number_of_dice = int(answer)
        except ValueError:
            console.print("[bold red]Please enter a whole number from 1 to 6.[/bold red]")
            continue
        if 1 <= number_of_dice <= 6:
            return number_of_dice
        console.print("[bold red]Choose between 1 and 6 dice.[/bold red]")


def show_statistics(rolls: list[int]) -> None:
    """Display statistics collected during this session."""
    table = Table(title="Session Statistics", box=box.ROUNDED, border_style="bright_blue")
    table.add_column("Metric", style="bold bright_cyan")
    table.add_column("Value", justify="right", style="bold white")
    total_points = sum(rolls)
    table.add_row("Number of rolls", str(len(rolls)))
    table.add_row("Highest roll", str(max(rolls) if rolls else "-"))
    table.add_row("Lowest roll", str(min(rolls) if rolls else "-"))
    table.add_row("Total points", str(total_points))
    table.add_row("Average roll", f"{total_points / len(rolls):.2f}" if rolls else "-")
    console.print(table)


def show_menu() -> str:
    """Render the main menu and return the user's selection."""
    menu = Table(box=box.SIMPLE_HEAVY, show_header=False, border_style="bright_magenta")
    menu.add_column("Option", style="bold bright_yellow", width=8)
    menu.add_column("Action", style="white")
    menu.add_row("1", "Roll the dice")
    menu.add_row("2", "View statistics")
    menu.add_row("3", "Roll again")
    menu.add_row("4", "Exit")
    console.print(Panel(menu, title="[bold bright_magenta]Main Menu[/bold bright_magenta]", box=box.ROUNDED))
    try:
        return console.input("[bold cyan]Choose an option:[/bold cyan] ").strip()
    except (EOFError, KeyboardInterrupt):
        return "4"


def main() -> None:
    """Run the interactive dice game until the player exits."""
    rolls: list[int] = []
    show_title()
    try:
        while True:
            choice = show_menu()
            if choice in {"1", "3"}:
                number_of_dice = ask_for_dice()
                if number_of_dice is not None:
                    rolls.append(roll_dice(number_of_dice))
            elif choice == "2":
                show_statistics(rolls)
            elif choice == "4" or choice.lower() in {"q", "quit", "exit"}:
                break
            else:
                console.print("[bold red]That option is not available. Choose 1, 2, 3, or 4.[/bold red]")
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Roll cancelled.[/bold yellow]")
    console.print(Panel("Thanks for playing! See you next time.", border_style="bright_green", box=box.DOUBLE))


if __name__ == "__main__":
    main()
