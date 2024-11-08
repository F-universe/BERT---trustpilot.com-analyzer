from transformers import BertTokenizer, BertForSequenceClassification
import torch
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 1. Load the tokenizer and pre-trained model for multilingual sentiment analysis
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# 2. Function to predict sentiment for a batch of reviews
def predict_batch_sentiment(reviews):
    results = []
    for review in reviews:
        inputs = tokenizer(review, return_tensors="pt", padding=True, truncation=True, max_length=512)
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        sentiment_score = torch.argmax(predictions).item()
        
        sentiment = "Positive" if sentiment_score >= 3 else "Neutral" if sentiment_score == 2 else "Negative"
        results.append((review, sentiment))
    return results

# 3. Read reviews from the text file
reviews_file_path = "C:\\Users\\Fabio\\Desktop\\BERT-(trustpilot.com) analyzer\\data.txt"

try:
    with open(reviews_file_path, "r", encoding="utf-8") as file:
        reviews = [line.strip().strip('"') for line in file if line.strip()]  # Removes quotes and empty lines

    # Analyze reviews
    analysis_results = predict_batch_sentiment(reviews)

    # Convert to DataFrame for analysis
    df = pd.DataFrame(analysis_results, columns=["Review", "Sentiment"])
    df["Review Length"] = df["Review"].apply(len)

    # Calculate maximum review length for dynamic scaling
    max_length = df["Review Length"].max()

    # Create subplots for all graphs
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # 1. Sentiment Distribution (Pie Chart)
    sentiment_counts = df["Sentiment"].value_counts()
    axes[0].pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, colors=['#4CAF50', '#FFC107', '#F44336'])
    axes[0].set_title("Sentiment Distribution")
    axes[0].text(-1.5, -1.5, "This chart shows the proportion of Positive, Neutral, and Negative reviews.")

    # 2. Review Length Distribution (Histogram)
    sns.histplot(df["Review Length"], bins=30, kde=True, ax=axes[1], color='blue')
    axes[1].set_xlim(0, max_length)
    axes[1].set_title("Distribution of Review Lengths")
    axes[1].set_xlabel("Review Length")
    axes[1].set_ylabel("Frequency")
    axes[1].text(max_length * 0.4, 500, "This histogram illustrates how review lengths are distributed.", fontsize=9)

    # 3. Sentiment vs Review Length (Boxplot)
    sns.boxplot(x="Sentiment", y="Review Length", data=df, ax=axes[2], palette="Set2")
    axes[2].set_title("Review Length by Sentiment")
    axes[2].set_xlabel("Sentiment")
    axes[2].set_ylabel("Review Length")
    axes[2].text(-0.5, max_length * 0.8, "This boxplot shows the spread of review lengths for each sentiment category.", fontsize=9)

    # Adjust layout
    plt.tight_layout()
    plt.show()

except FileNotFoundError:
    print(f"File not found: {reviews_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
