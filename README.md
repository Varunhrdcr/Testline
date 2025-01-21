# Quiz Performance Analysis

This project analyzes quiz performance data to generate insights and recommendations for students. The analysis focuses on identifying weak areas, improvement trends, and performance gaps based on topics, difficulty levels, and response accuracy.

## Features
- Fetches quiz data from API endpoints.
- Analyzes historical quiz data to identify performance metrics.
- Generates personalized insights based on the analysis.
- Creates actionable recommendations for students to improve their performance.

## Requirements

- Python 3.x
- `requests` library for making API requests.
- `pandas` library for data manipulation and analysis.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your-Varunhrdcr/testline.git
    cd testline.git
    ```

2. Install the required libraries:

    ```sh
    pip install requests pandas
    ```

## Usage

1. Ensure you have the API endpoints for current and historical quiz data. Update the `current_quiz_endpoint` and `historical_quiz_endpoint` variables in the code with your API endpoints.

2. Run the script:

    ```sh
    python analyze_quiz_performance.py
    ```

3. The script will fetch the data, analyze it, and print the insights and recommendations.

## Output

The script will output the following information:

- **Historical Data**: The raw historical quiz data fetched from the API.
- **Topic Performance**: A DataFrame showing the mean accuracy and difficulty for each topic.
- **Insights**: Personalized insights highlighting weak areas and improvement trends.
- **Recommendations**: Actionable recommendations for topics that need improvement.

Example output:

Historical Data:
{'id': 336566, 'quiz_id': 43, 'user_id': '7ZXdz3zHuNcdg9agb5YpaOGLQqw2', 'submitted_at': '2025-01-17T15:51:29.859+05:30', ...}
...

Historical DataFrame created successfully.
Head of Historical DataFrame:
correct_responses  total_questions  ...  submission_date  difficulty
0                  8               10  ...  2025-01-17T15:51:29.859+05:30  Medium
...

Topic Performance:
topic  accuracy  difficulty
0  Biology      0.85       2.5
1  Chemistry   0.70       3.0
...

Insights:

Weak Topic: Chemistry - Focus on improving this topic as accuracy is below 50%.
Improvement: Your accuracy in Biology has improved by 15.00%.
Decline: Your accuracy in Chemistry has decreased by 10.00%.
Recommendations:

Topic: Chemistry - Practice more questions in Chemistry at a medium difficulty level to improve accuracy.
