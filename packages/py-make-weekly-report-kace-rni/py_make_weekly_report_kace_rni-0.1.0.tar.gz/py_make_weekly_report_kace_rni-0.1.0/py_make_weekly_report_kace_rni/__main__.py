import logging
import os
import platform
import string
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

import pyperclip
from rich.console import Console

logging.basicConfig(format='%(message)s', level=logging.INFO)


class WeeklyReportGenerator:
    def __init__(
            self, *,
            name: str = "Anthony",
            unit: str = "SE",
    ):
        self.name = name
        self.unit = unit

        self.start_date, self.end_date = self.get_week_range()
        self.date_range = self.format_date_range(self.start_date, self.end_date)

        self.console = Console()
        self.report_content = []

    def get_week_range(self) -> tuple:
        """Get the start and end date of the current week."""
        today = datetime.now()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=4)  # Monday to Friday
        return start, end

    def get_week_number(self, date: datetime) -> int:
        """Get the week number of the year."""
        return int(date.strftime('%W')) + 1

    def generate_filename(self) -> str:
        """Generate filename in format: Week [n] [Month] [monday's date] - [friday's date].txt"""
        week_num = self.get_week_number(self.start_date)
        return f"Week {week_num} {self.start_date.strftime('%b')} {self.start_date.day} - {self.end_date.day}.txt"

    def format_date_range(self, start: datetime, end: datetime) -> str:
        """Format the date range string."""
        return f"{start.strftime('%B %d')}{self.get_ordinal(start.day)} – {end.strftime('%B %d')}{self.get_ordinal(end.day)} {end.year}"

    def get_ordinal(self, day: int) -> str:
        """Return the ordinal indicator for a day."""
        if 10 <= day % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        return suffix

    def get_input_list(self, prompt: str) -> List[str]:
        """Get multiple inputs from user until empty line is entered."""
        items = []
        print(f"\n{prompt} (press Enter twice to finish):")
        while True:
            item = input().strip()
            if not item and items:  # Empty line and we have some items
                break
            elif item:  # Non-empty line
                items.append(item)
        return items

    def clean_input(self, input: str) -> str:
        cleaned_item = input[0].upper() + input[1:]  # capitalize the first letter
        if cleaned_item[-1] not in string.punctuation: cleaned_item += '.'  # add full stop
        return cleaned_item

    def add_to_report(self, text: str, style: str = None):
        """Add text to report content list."""
        self.console.print(text, style=style)
        # Strip rich formatting for plain text version
        self.report_content.append(text)

    def save_to_file(self):
        current_year = str(datetime.now().year)
        filename = self.generate_filename()

        # Get desktop path based on the current os
        if platform.system() == "Windows":
            desktop = Path(os.path.join(os.path.expanduser("~"), "Desktop"))

        elif platform.system() == "Darwin":  # macOS
            desktop = Path(os.path.join(os.path.expanduser("~"), "Desktop"))

        else:  # Linux and other Unix-like
            desktop = Path(os.path.join(os.path.expanduser("~"), "Desktop"))
            if not desktop.exists():
                desktop = Path(os.path.join(os.path.expanduser("~"), "Desktop"))

        # Create Weekly Reports folder and year subfolder
        reports_dir = desktop / "Weekly Reports" / current_year
        reports_dir.mkdir(parents=True, exist_ok=True)

        save_path = reports_dir / filename

        with open(save_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.report_content))

        self.console.print(f"\nReport saved to: {save_path}", style="bold green")

        return save_path

    def copy_to_clipboard(self):
        """Copy report content to clipboard."""
        text_content = '\n'.join(self.report_content)
        pyperclip.copy(text_content)
        self.console.print("\nReport copied to clipboard!", style="bold green")

    def generate_report(self):
        """Generate the weekly report based on user input."""
        # Clear previous content
        self.report_content = []

        # Get basic information
        name = self.name or input("\nEnter your name: ")
        unit = self.unit or input("Enter your unit: ")
        project = input("Enter the project: ")

        # Get achievements and challenges
        achievements = self.get_input_list("Enter key achievements")
        challenges = self.get_input_list("Enter challenges and next steps")

        # Create the report
        self.add_to_report("=" * 80)
        self.add_to_report("")

        # Header
        header = f"Subject: Week Report of {self.date_range}, [{name}]"
        self.add_to_report(header, "bold blue")

        # Divider
        self.add_to_report("-" * 80)

        # Basic Info
        self.add_to_report(f"Unit: {unit}", "bold")
        self.add_to_report(f"Project: {project}", "bold")

        # Achievements
        self.add_to_report("\nKey Achievement(s):", "bold green")
        for achievement in achievements:
            self.add_to_report(f"  • {self.clean_input(achievement)}")

        # Challenges
        self.add_to_report("\nChallenges and Next Steps:", "bold yellow")
        for challenge in challenges:
            self.add_to_report(f"  • {self.clean_input(challenge)}")

        self.add_to_report("\n" + "=" * 80)

        # Save and copy
        self.save_to_file()
        self.copy_to_clipboard()


def main():
    try:
        generator = WeeklyReportGenerator()
        generator.generate_report()
    except KeyboardInterrupt:
        print("\nReport generation cancelled.")
    except:
        logging.exception(f"\nAn error occurred:")
    else:
        print("\nReport generation completed successfully!")


if __name__ == "__main__":
    main()
