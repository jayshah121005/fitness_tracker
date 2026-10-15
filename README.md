
# Personal Fitness Tracker Dashboard

## About the Project

The Personal Fitness Tracker Dashboard is a Python-based project that helps users record their daily fitness activities and analyze their exercise progress.

Users can add activities like Running, Walking, Cycling, and Yoga. The project calculates fitness metrics and displays charts to help users understand their activity patterns.

## Features

- **Log Activities:** Add activity type, date, duration, and calories burned.
- **Input Validation:** Prevent invalid duration and calorie values.
- **Fitness Metrics:** Calculate total calories, average duration, and total exercise time.
- **Activity Frequency:** Count how often each activity is performed.
- **Filter Activities:** Filter records by activity type or date range.
- **Fitness Report:** Display a summary and recent activities.
- **Data Visualization:** Generate bar charts, line graphs, pie charts, and a correlation heatmap.
- **CSV Storage:** Save fitness records in a CSV file.

## Technologies Used

- Python
- Object-Oriented Programming (OOP)
- NumPy
- Pandas
- Matplotlib
- Seaborn
- CSV

## Project Structure

```text
fitness_dashboard/
│
├── fitness_tracker.py
├── fitness_activities.csv
└── README.md
```

## Installation

### 1. Install Python

Install Python 3.9 or newer from:

https://www.python.org/downloads/

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Personal-Fitness-Tracker.git
```

Replace `YOUR_USERNAME` with your GitHub username.

### 3. Open the Project Folder

```bash
cd Personal-Fitness-Tracker
```

### 4. Install Required Libraries

```bash
python -m pip install numpy pandas matplotlib seaborn
```

## How to Run

Run the following command in your terminal:

```bash
python fitness_tracker.py
```

The program displays a menu where you can select different options.

## Main Menu

```text
====== PERSONAL FITNESS TRACKER ======
1. Log a new activity
2. Calculate fitness metrics
3. Filter activities
4. Generate report
5. Show charts
6. View all activities
7. Exit
```

## Dataset Description

The `fitness_activities.csv` file stores the fitness activity records.

| Column | Description |
|---|---|
| Date | Date of the activity |
| Activity Type | Running, Walking, Cycling, Yoga, etc. |
| Duration (Minutes) | Time spent exercising |
| Calories Burned | Recorded calories burned |

The project includes sample data for demonstration. Users can add more records through the program.

## Data Analysis

NumPy is used for numerical calculations, including totals and averages.

Pandas is used to load, clean, filter, and group fitness records.

Matplotlib and Seaborn are used to create these visualizations:

1. **Bar Chart:** Compares total exercise time by activity.
2. **Line Graph:** Shows calories burned over time.
3. **Pie Chart:** Displays the percentage of sessions by activity type.
4. **Heatmap:** Shows the correlation between exercise duration and calories burned.

## Learning Outcomes

Through this project, I practiced:

- Python functions, loops, and conditional statements.
- Object-Oriented Programming.
- Handling user input and validation.
- Reading and writing CSV files.
- Data cleaning and analysis using Pandas.
- Numerical calculations using NumPy.
- Data visualization using Matplotlib and Seaborn.

## Conclusion

The Personal Fitness Tracker Dashboard demonstrates how Python can be used to manage and analyze fitness data. It provides a simple way to record activities, calculate useful metrics, and visualize exercise patterns.



GitHub: https://github.com/YOUR_USERNAME
