This project, like some previous ones, uses the BERT model to analyze reviews for an entity
available on Trustpilot.com. The project consists of three Python scripts and one text file.
The first script, firstcode.py, is connected to the index.html file located in the templates folder.
When executed, it launches a Flask application that redirects to http://127.0.0.1:5000, where a web 
page displays a search form. Users can input the name of a company or any entity available on Trustpilot. 
Upon clicking the "Search" button, a web driver is activated, which scrapes all reviews for the selected 
topic and stores them in data.txt. The second script, test.py, analyzes the reviews in data.txt using the 
BERT model. It classifies each review as positive, negative, or neutral and generates three illustrative
graphs to visually represent the sentiment analysis results, providing a comprehensive 
summary of customer feedback.
