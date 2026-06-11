

# 📊 WhatsApp Chat Analyzer

A powerful **Streamlit-based WhatsApp Chat Analyzer** that extracts meaningful insights from exported WhatsApp chats. The application provides detailed statistics, activity analysis, sentiment analysis, emoji analysis, response-time insights, word clouds, and interactive visualizations.

---

## 🚀 Features

### 📈 Chat Statistics

Get a quick overview of the chat:

* Total Messages
* Total Words
* Media Messages Shared
* Links Shared

---

### 👥 User Activity Analysis

Identify the most active participants in the chat.

Features:

* Most Busy Users
* User Contribution Percentage
* User-wise Message Count

---

### ☁️ Word Cloud

Generate a visual representation of the most frequently used words in the conversation.

Features:

* Stopword Removal
* Media Message Filtering
* User-specific Word Clouds
* Clean and Meaningful Word Visualization

---

### 🔤 Most Common Words Analysis

Discover the most frequently used meaningful words.

Features:

* Stopword Removal
* URL Removal
* Media Message Filtering
* Frequency-Based Ranking
* Top 20 Common Words Visualization

---

### 😀 Emoji Analysis

Analyze emoji usage patterns in conversations.

Features:

* Most Used Emojis
* Emoji Frequency Distribution
* Interactive Pie Chart Visualization

---

### 📅 Monthly Timeline Analysis

Visualize message activity across months.

Features:

* Month-wise Message Trends
* Activity Peaks Detection
* Historical Chat Growth Analysis

---

### 📆 Daily Timeline Analysis

Track daily messaging activity.

Features:

* Date-wise Message Count
* Activity Trend Visualization
* Chat Consistency Analysis

---

### 📊 Weekly Activity Analysis

Understand which days are most active.

Features:

* Messages per Weekday
* Weekly Engagement Insights

---

### 🔥 Activity Heatmap

Visualize messaging activity across days and hours.

Features:

* Hour-wise Activity
* Day-wise Activity
* Heatmap Representation
* Peak Communication Time Detection

---

### ⏱️ Response Time Analysis

Measure how quickly users respond to messages.

Features:

* Average Response Time
* Fastest Responder Identification
* User-wise Response Metrics

---

### 😊 Sentiment Analysis

Analyze the emotional tone of conversations.

Features:

* Positive Messages
* Neutral Messages
* Negative Messages
* Sentiment Distribution Pie Chart

---

## 🛠️ Technologies Used

### Backend

* Python

### Data Processing

* Pandas
* NumPy
* Regular Expressions (Regex)

### Data Visualization

* Matplotlib
* Seaborn
* Plotly

### NLP & Text Analysis

* TextBlob
* WordCloud
* Emoji

### Web Framework

* Streamlit

---

## 📂 Project Structure

```text
Whatsapp Chat Analyzer/
│
├── app.py
├── helper.py
├── preprocessor.py
├── requirements.txt
├── README.md
├── .gitignore
└── sample_chat.txt
```

### app.py

Main Streamlit application.

Responsibilities:

* User Interface
* Visualization Rendering
* Dashboard Layout
* User Selection

### helper.py

Contains all analysis functions.

Responsibilities:

* Statistics Calculation
* Word Cloud Generation
* Emoji Analysis
* Sentiment Analysis
* Timeline Generation
* Response Time Analysis

### preprocessor.py

Handles WhatsApp chat preprocessing.

Responsibilities:

* Date Extraction
* User Extraction
* Message Parsing
* Feature Engineering

---


---

## 📤 Exporting WhatsApp Chat

1. Open WhatsApp.
2. Open the desired chat.
3. Click More Options.
4. Select Export Chat.
5. Choose Without Media.
6. Save the exported `.txt` file.
7. Upload it to the application.

---

## 🔄 Workflow

### Step 1: Upload Chat File

User uploads WhatsApp exported text file.

↓

### Step 2: Preprocessing

The application:

* Extracts dates
* Extracts usernames
* Separates messages
* Creates structured dataset

↓

### Step 3: Feature Engineering

Additional fields generated:

* Year
* Month
* Day
* Hour
* Weekday
* Period

↓

### Step 4: Analysis

The application performs:

* Statistics Analysis
* Word Analysis
* Emoji Analysis
* Sentiment Analysis
* Timeline Analysis
* Activity Analysis

↓

### Step 5: Visualization

Results displayed through:

* Bar Charts
* Pie Charts
* Heatmaps
* Line Charts
* Word Clouds

---

## 📊 Example Insights

The analyzer can answer questions such as:

* Who sends the most messages?
* Which day is most active?
* What are the most common discussion topics?
* Which emojis are used most frequently?
* What is the overall sentiment of the chat?
* Who replies the fastest?
* What are the peak activity hours?

---

## 🔮 Future Enhancements

* AI-based Topic Modeling
* Chat Summarization
* Advanced NLP Analysis
* Message Classification
* Language Detection
* Export Reports as PDF
* User Interaction Network Graphs
* Interactive Dashboard Filters

---

---

## 📜 License

This project is intended for educational and learning purposes.

---

## 👨‍💻 Author

**Burhanuddin Husain**

Python Developer | Machine Learning Enthusiast | Data Science Learner

