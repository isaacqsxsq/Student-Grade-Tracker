# Student Grade Tracker

A CLI application to track student grades for a single subject.
Supports multiple grade categories with configurable weights and two score modes.

---

## Features

- Add students with or without grades
- Grade categories with two modes: single score or multiple scores (averaged)
- Configurable category weights that must sum to 1.0
- Weighted final grade calculation per student
- Add, delete, and update categories dynamically
- Data persisted across sessions in CSV files

---

## Project Structure

```
grade_tracker/
├── Data/
│   ├── .student.csv        # stores student grades
│   └── .categories.csv     # stores category configuration
├── main.py
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.10 or higher
- tabulate

---

## Installation

1. Clone or download this repository

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the program:
```
python tracker.py
```

---

## How to Use

On launch, a menu appears:

```
1. View All Students        — shows raw scores, averages, and weighted final grade
2. Add Student              — adds a student with empty grades
3. Add Student With Grade   — adds a student and enters all grades at once
4. Update Student Grade     — update a single category for an existing student
5. Delete Student           — permanently removes a student (with confirmation)
6. Update Category          — add/delete categories or update their weights
q. Quit                     — exits the program
```

### Adding Grades

- **Single mode** categories accept one number (e.g. attendance: `95`)
- **List mode** categories accept multiple comma-separated numbers (e.g. homework: `80,90,70`)
- All scores must be integers between 0 and 100

### Updating a List Mode Category

When updating a list mode category you will be asked:
```
1. Add    — appends a new score to existing scores
2. Update — replaces all scores with new input
```

### Managing Categories

When updating categories you will be asked:
```
1. Add category     — adds a new category and reassigns all weights
2. Delete category  — removes a category and reassigns all weights
3. Update weight    — reassigns weights for all existing categories
```

> ⚠️ Weights must always sum to exactly 1.0

---

## File Format

### .categories.csv
```
name,weight,mode
homework,0.3,list
test,0.5,list
attendance,0.2,single
```

### .student.csv
```
name,homework,test,attendance
John,80,90,70,85,90,95
Jane,70,80,88
```

---

## Final Grade Calculation

The weighted final grade is calculated as:

```
final = avg(homework) × weight + avg(test) × weight + avg(attendance) × weight
```

Example with default categories:
```
homework avg = 80.0  × 0.3 = 24.0
test avg     = 87.5  × 0.5 = 43.75
attendance   = 95.0  × 0.2 = 19.0
─────────────────────────────────
final grade          = 86.75
```

> If a category has no scores entered yet, the final grade will show as N/A

---

## Notes

- Student names are stored in Title Case (e.g. `John Smith`)
- Category names are stored in lowercase
- Deleting a student or category cannot be undone
