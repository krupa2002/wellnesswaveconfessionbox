import datetime
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)

def record_mood(mood):
    date = datetime.date.today().strftime("%Y-%m-%d")
    with open("mood_tracker.txt", "a") as file:
        file.write(f"{date}: {mood}\n")

def write_journal_entry(entry):
    date = datetime.date.today().strftime("%Y-%m-%d")
    with open("journal.txt", "a") as file:
        file.write(f"{date}:\n{entry}\n\n")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    mood = request.form['mood']
    confession = request.form['confession']

    record_mood(mood)
    write_journal_entry(confession)

    return render_template('success.html')

@app.route('/data')
def data():
    mood_data = pd.read_csv("mood_tracker.txt", header=None, names=["Date", "Mood"])
    confession_data = pd.read_csv("journal.txt", sep=":\n", header=None, names=["Date", "Confession"])
    return render_template('data.html', mood_data=mood_data.to_html(), confession_data=confession_data.to_html())

@app.route('/mood_chart')
def mood_chart():
    mood_data = pd.read_csv("mood_tracker.txt", header=None, names=["Date", "Mood"])
    mood_counts = mood_data['Mood'].value_counts()

    # Create pie chart using Matplotlib
    plt.figure(figsize=(8, 6))
    plt.pie(mood_counts, labels=mood_counts.index, autopct='%1.1f%%')
    plt.title('My Moods')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.tight_layout()

    # Save the pie chart to a temporary file
    chart_filename = 'static/mood_chart.png'
    plt.savefig(chart_filename)

    # Close the Matplotlib plot to free up memory
    plt.close()

    return render_template('mood_chart.html', chart_filename=chart_filename)

if __name__ == "__main__":
    app.run(debug=True)
