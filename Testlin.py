import requests
import pandas as pd

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

current_quiz_endpoint = "https://www.jsonkeeper.com/b/LLQT"
historical_quiz_endpoint = "https://api.jsonserve.com/rJvd7g"

current_quiz_data = fetch_data(current_quiz_endpoint)
historical_quiz_data = fetch_data(historical_quiz_endpoint)

def analyze_data(current_data, historical_data):
    if not historical_data:
        raise ValueError("Historical data is empty or invalid.")

    print("Historical Data:")
    for entry in historical_data:
        print(entry)

    normalized_data = []
    for entry in historical_data:
        if isinstance(entry, dict):
            normalized_data.append(entry)
        else:
            print(f"Skipping non-dict entry: {entry}")

    try:
        historical_df = pd.DataFrame(normalized_data)
        print("\nHistorical DataFrame created successfully.")
        print("Head of Historical DataFrame:\n", historical_df.head())
    except Exception as e:
        raise ValueError(f"Failed to create DataFrame from historical data: {e}")

    required_columns = {'correct_responses', 'total_questions', 'topic', 'submission_date', 'difficulty'}
    missing_columns = required_columns - set(historical_df.columns)
    if missing_columns:
        print(f"Missing required columns in historical data: {missing_columns}")
        for col in missing_columns:
            historical_df[col] = None

    historical_df.loc[:, 'correct_responses'] = historical_df['correct_responses'].fillna(0)
    historical_df.loc[:, 'total_questions'] = historical_df['total_questions'].fillna(1)
    historical_df.loc[:, 'topic'] = historical_df['topic'].fillna('Unknown')
    historical_df.loc[:, 'submission_date'] = historical_df['submission_date'].fillna(pd.Timestamp.now())
    historical_df.loc[:, 'difficulty'] = historical_df['difficulty'].fillna('Unknown')

    historical_df['accuracy'] = historical_df['correct_responses'] / historical_df['total_questions'].replace(0, 1)

    topic_performance = historical_df.groupby('topic').agg({
        'accuracy': 'mean',
        'difficulty': 'mean'
    }).reset_index()

    weak_topics = topic_performance[topic_performance['accuracy'] < 0.5]

    historical_df['submission_date'] = pd.to_datetime(historical_df['submission_date'], errors='coerce')
    historical_df.dropna(subset=['submission_date'], inplace=True)
    historical_df.sort_values(by='submission_date', inplace=True)
    improvement_trends = historical_df.groupby('topic')['accuracy'].apply(lambda x: x.iloc[-1] - x.iloc[0])

    return topic_performance, weak_topics, improvement_trends

def generate_insights(topic_performance, weak_topics, improvement_trends):
    insights = []

    for _, row in weak_topics.iterrows():
        insights.append(f"Weak Topic: {row['topic']} - Focus on improving this topic as accuracy is below 50%.")

    for topic, trend in improvement_trends.items():
        if trend > 0:
            insights.append(f"Improvement: Your accuracy in {topic} has improved by {trend:.2%}.")
        else:
            insights.append(f"Decline: Your accuracy in {topic} has decreased by {-trend:.2%}.")

    return insights

def create_recommendations(weak_topics):
    recommendations = []

    for _, row in weak_topics.iterrows():
        recommendations.append({
            "topic": row['topic'],
            "suggestion": f"Practice more questions in {row['topic']} at a medium difficulty level to improve accuracy."
        })

    return recommendations

try:
    if not current_quiz_data or not historical_quiz_data:
        raise ValueError("Quiz data is empty or invalid.")

    topic_performance, weak_topics, improvement_trends = analyze_data(current_quiz_data, historical_quiz_data)
    print("\nTopic Performance:")
    print(topic_performance)

    insights = generate_insights(topic_performance, weak_topics, improvement_trends)
    recommendations = create_recommendations(weak_topics)

    print("\nInsights:")
    for insight in insights:
        print(f"  - {insight}")

    print("\nRecommendations:")
    for rec in recommendations:
        print(f"  - Topic: {rec['topic']} - {rec['suggestion']}")
except Exception as e:
    print(f"An error occurred: {e}")
