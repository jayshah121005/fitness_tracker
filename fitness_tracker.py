"""
Personal Fitness Tracker Dashboard
A beginner-friendly project using Python, OOP, NumPy, Pandas,
Matplotlib and Seaborn.
"""

import os
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


DATA_FILE = "fitness_activities.csv"


class FitnessTracker:
    """Stores fitness activities and provides simple analysis tools."""

    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.columns = ["Date", "Activity Type", "Duration (Minutes)", "Calories Burned"]
        self.activities = self.load_data()

    def load_data(self):
        """Load the CSV file, or create an empty dataset if it does not exist."""
        if not os.path.exists(self.filename):
            empty_data = pd.DataFrame(columns=self.columns)
            empty_data.to_csv(self.filename, index=False)
            return empty_data

        try:
            data = pd.read_csv(self.filename)
            # Check that the file contains all required columns.
            for column in self.columns:
                if column not in data.columns:
                    data[column] = np.nan

            data = data[self.columns]
            data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
            data["Activity Type"] = data["Activity Type"].astype("string").str.strip()
            data["Duration (Minutes)"] = pd.to_numeric(
                data["Duration (Minutes)"], errors="coerce"
            )
            data["Calories Burned"] = pd.to_numeric(
                data["Calories Burned"], errors="coerce"
            )

            # Remove rows that do not have usable values.
            data = data.dropna(subset=self.columns)
            data = data[
                (data["Activity Type"] != "")
                & (data["Duration (Minutes)"] > 0)
                & (data["Calories Burned"] > 0)
            ]
            data["Date"] = data["Date"].dt.strftime("%Y-%m-%d")
            return data.reset_index(drop=True)

        except (pd.errors.EmptyDataError, pd.errors.ParserError, OSError):
            print("Could not read the CSV file. Starting with an empty dataset.")
            return pd.DataFrame(columns=self.columns)

    def save_data(self):
        """Save the current activities to the CSV file."""
        self.activities.to_csv(self.filename, index=False)

    def log_activity(self, activity_type, duration, calories, date=None):
        """Validate and add a new activity."""
        activity_type = activity_type.strip().title()

        if not activity_type:
            print("Activity type cannot be empty.")
            return False

        try:
            duration = float(duration)
            calories = float(calories)
        except (ValueError, TypeError):
            print("Duration and calories must be numbers.")
            return False

        if duration <= 0 or calories <= 0:
            print("Duration and calories must be greater than zero.")
            return False

        if date is None or date.strip() == "":
            date = datetime.today().strftime("%Y-%m-%d")

        try:
            date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Date must use YYYY-MM-DD format, for example 2026-10-15.")
            return False

        new_activity = {
            "Date": date,
            "Activity Type": activity_type,
            "Duration (Minutes)": duration,
            "Calories Burned": calories,
        }

        self.activities = pd.concat(
            [self.activities, pd.DataFrame([new_activity])], ignore_index=True
        )
        self.save_data()
        print("Activity saved successfully!")
        return True

    def calculate_metrics(self):
        """Calculate total, average and frequency metrics."""
        if self.activities.empty:
            print("No activities available yet. Add an activity first.")
            return None

        durations = self.activities["Duration (Minutes)"].to_numpy(dtype=float)
        calories = self.activities["Calories Burned"].to_numpy(dtype=float)

        metrics = {
            "activity_count": len(self.activities),
            "total_calories": float(np.sum(calories)),
            "average_duration": float(np.mean(durations)),
            "average_calories": float(np.mean(calories)),
            "total_duration": float(np.sum(durations)),
        }

        print("\n--- Fitness Summary ---")
        print("Number of activities:", metrics["activity_count"])
        print("Total calories burned:", round(metrics["total_calories"], 2))
        print("Total exercise time (minutes):", round(metrics["total_duration"], 2))
        print("Average activity duration (minutes):", round(metrics["average_duration"], 2))
        print("Average calories per activity:", round(metrics["average_calories"], 2))

        print("\nActivity frequency:")
        print(self.activities["Activity Type"].value_counts().to_string())

        # Grouping data with Pandas.
        print("\nSummary by activity:")
        summary = self.activities.groupby("Activity Type").agg(
            Sessions=("Activity Type", "count"),
            Total_Minutes=("Duration (Minutes)", "sum"),
            Total_Calories=("Calories Burned", "sum"),
        )
        print(summary.round(2).to_string())
        return metrics

    def filter_activities(self, condition=None):
        """Filter activities by type or date range."""
        if self.activities.empty:
            print("No activities to filter.")
            return self.activities.copy()

        print("\nFilter activities:")
        print("1. By activity type")
        print("2. By date range")
        print("3. Show all activities")
        choice = input("Choose an option: ").strip()

        data = self.activities.copy()
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

        if choice == "1":
            activity = input("Enter activity type (e.g., Running): ").strip().title()
            result = data[data["Activity Type"].str.title() == activity]
        elif choice == "2":
            start_date = input("Start date (YYYY-MM-DD): ").strip()
            end_date = input("End date (YYYY-MM-DD): ").strip()
            try:
                start = pd.to_datetime(start_date, format="%Y-%m-%d")
                end = pd.to_datetime(end_date, format="%Y-%m-%d")
                if start > end:
                    print("Start date cannot be after end date.")
                    return self.activities.iloc[0:0].copy()
                result = data[(data["Date"] >= start) & (data["Date"] <= end)]
            except ValueError:
                print("Invalid date. Please use YYYY-MM-DD.")
                return self.activities.iloc[0:0].copy()
        elif choice == "3":
            result = data
        else:
            print("Invalid filter option.")
            return self.activities.iloc[0:0].copy()

        if result.empty:
            print("No activities matched your filter.")
        else:
            print("\nFiltered activities:")
            print(result.assign(Date=result["Date"].dt.strftime("%Y-%m-%d")).to_string(index=False))
        return result

    def generate_report(self):
        """Print a simple report and offer to create visualizations."""
        if self.activities.empty:
            print("No data available. Add activities or check your CSV file.")
            return

        print("\n========== FITNESS REPORT ==========")
        self.calculate_metrics()
        print("\nRecent activities:")
        recent = self.activities.copy()
        recent["Date"] = pd.to_datetime(recent["Date"], errors="coerce")
        recent = recent.sort_values("Date", ascending=False).head(5)
        recent["Date"] = recent["Date"].dt.strftime("%Y-%m-%d")
        print(recent.to_string(index=False))
        print("====================================")

    def show_charts(self):
        """Create a bar chart, line graph, pie chart and heatmap."""
        if self.activities.empty:
            print("No data available to plot.")
            return

        data = self.activities.copy()
        data["Duration (Minutes)"] = pd.to_numeric(data["Duration (Minutes)"])
        data["Calories Burned"] = pd.to_numeric(data["Calories Burned"])
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

        sns.set_theme(style="whitegrid")

        # 1. Bar chart: total time by activity.
        activity_minutes = data.groupby("Activity Type")["Duration (Minutes)"].sum()
        plt.figure(figsize=(8, 5))
        activity_minutes.plot(kind="bar")
        plt.title("Total Exercise Time by Activity")
        plt.xlabel("Activity Type")
        plt.ylabel("Minutes")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.show()

        # 2. Line graph: calories burned over time.
        daily_calories = data.groupby("Date")["Calories Burned"].sum().sort_index()
        plt.figure(figsize=(8, 5))
        plt.plot(daily_calories.index, daily_calories.values, marker="o")
        plt.title("Calories Burned Over Time")
        plt.xlabel("Date")
        plt.ylabel("Calories")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.show()

        # 3. Pie chart: share of exercise sessions by activity.
        activity_counts = data["Activity Type"].value_counts()
        plt.figure(figsize=(7, 7))
        plt.pie(
            activity_counts.values,
            labels=activity_counts.index,
            autopct="%1.1f%%",
            startangle=90,
        )
        plt.title("Percentage of Activities")
        plt.tight_layout()
        plt.show()

        # 4. Heatmap: relationship between duration and calories.
        plt.figure(figsize=(6, 4))
        correlation = data[["Duration (Minutes)", "Calories Burned"]].corr()
        sns.heatmap(correlation, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
        plt.title("Duration and Calories Correlation")
        plt.tight_layout()
        plt.show()


def get_positive_number(message):
    """Keep asking until the user enters a positive number."""
    while True:
        try:
            value = float(input(message))
            if value > 0:
                return value
            print("Please enter a number greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a number, such as 30.")


def main():
    tracker = FitnessTracker()

    while True:
        print("\n====== PERSONAL FITNESS TRACKER ======")
        print("1. Log a new activity")
        print("2. Calculate fitness metrics")
        print("3. Filter activities")
        print("4. Generate report")
        print("5. Show charts")
        print("6. View all activities")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            activity = input("Activity type (Running, Yoga, Cycling, etc.): ").strip()
            duration = get_positive_number("Duration in minutes: ")
            calories = get_positive_number("Calories burned: ")
            date = input("Date (YYYY-MM-DD), or press Enter for today: ").strip()
            tracker.log_activity(activity, duration, calories, date)

        elif choice == "2":
            tracker.calculate_metrics()

        elif choice == "3":
            tracker.filter_activities()

        elif choice == "4":
            tracker.generate_report()

        elif choice == "5":
            tracker.show_charts()

        elif choice == "6":
            if tracker.activities.empty:
                print("No activities recorded yet.")
            else:
                print(tracker.activities.to_string(index=False))

        elif choice == "7":
            print("Thank you for using the Personal Fitness Tracker!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
