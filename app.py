import base64
from io import BytesIO
import logging
import os
from flask import Flask, request, render_template
from logging.config import dictConfig
from matplotlib import pyplot as plt
import numpy as np
import requests
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest
from pytrends.request import TrendReq
import utils

# App configuration to show logs information in Deta
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

#================================================================================
# TP1 Create default page with 'Hello World :)' and connexion to google analytics
#================================================================================
@app.route("/", methods=['GET', 'POST'])
def hello_world():
    page_content = """
    <p>Hello World :)</p>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-FVQS2TWEVX"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-FVQS2TWEVX');
    </script>
    """
    return page_content

#=================================================================
# TP1: Display textbox from which input will go to Deta logs
#=================================================================
@app.route("/logger", methods=['GET', 'POST'])
def logger():
    """
    A Flask route that allows logging of text input from a textarea.

    This route provides a simple HTML page with a textarea where users can input text. When the form is submitted,
    the text is retrieved and logged to the system's log using the `logging.info` function.

    Returns:
        str: HTML page containing the textarea for text input.

    Example:
        Access the route '/logger' in a web browser, input text, and submit the form to log the text.
    """
    if request.method == 'POST':
        # Retrieve the text from the textarea
        text = request.form.get('textarea')
  
        # Print the text in terminal for verification
        logging.info(text)
  
    return render_template('logger.html')


#=================================================================
# TP2:  Send Google request and display cookies and status code
#=================================================================
@app.route('/google', methods=['GET', 'POST'])
def google_request():
    """
    A Flask route that serves as a Google request page with the ability to make requests to Google and display the results.

    This route displays a simple HTML page with a button to make a request to Google. Upon clicking the button,
    it sends a request to Google, stores cookies, and displays the status code and cookies.

    Returns:
        str: HTML page containing the Google request page and request form.

    Example:
        Access the route '/google' in a web browser and click the button to make a request to Google.
    """
    page_content = """
        <p>Welcome to the google request page :)</p>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-FVQS2TWEVX"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-FVQS2TWEVX');
        </script>
        """
    if request.method == 'POST':
        # Request to google and storing cookies
        response = requests.get('https://www.google.com')
        cookies = response.cookies.get_dict()
        page_content += f"<p>Status Code: {response.status_code}</p>"
        page_content += f"<p>Cookies: {cookies}</p>"
    
    return (
        page_content +
        """
        <form method="post">
            <input type="submit" value="Make Request to Google">
        </form>
        """
    )


#=========================================================================================
# TP2:  Access Google Analytics page (also displaying status code and cookies of request)
#=========================================================================================
@app.route("/google_analytics", methods=['GET', 'POST'])
def google_analytics_request():
    """
    A Flask route that serves as a Google Analytics login page and allows making requests to Google Analytics.

    This route displays a simple HTML page with a button to make a request to Google Analytics. Upon clicking the button,
    it sends a request to Google Analytics and displays the status code, cookies, and response text.

    Returns:
        str: HTML page containing the Google Analytics login page and request form.

    Example:
        Access the route '/google-analytics' in a web browser and click the button to make a request to Google Analytics.
    """
    page_content = """
    <p>Welcome to the google analytics login page :)</p>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-FVQS2TWEVX"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-FVQS2TWEVX');
    </script>
    """

    if request.method == 'POST':
        # Handle the button click to make the request to Google Analytics
        ganalytics_url = "https://analytics.google.com/analytics/web/#/p407466116/reports/intelligenthome"
        req2 = requests.get(ganalytics_url)
        cookies2 = req2.cookies.get_dict()
        page_content += f"<p>Status Code: {req2.status_code}</p>"
        page_content += f"<p>Cookies: {cookies2}</p>"
        page_content += f"<p>Response Text: {req2.text}</p>"

    return (
        page_content +
        """
        <form method="post">
            <input type="submit" value="Make Request to Google Analytics">
        </form>
        """
    )

#=================================================================
# TP2: OAuth2 access Google Analytics website data
#=================================================================
@app.route('/fetch_analytics', methods=['GET'])
def fetch_google_analytics_data():
    """
    Send a request to the Google Analytics Data API and return the response.

    Args:
        client: A Google Analytics Data API client (service account).
        property_id (str): The ID of the property for which to fetch data.

    Returns:
        google.analytics.data_v1beta.RunReportResponse: The API response.

    Example:
        response = get_request_result(client, PROPERTY_ID)
    """
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'datasources-401318-1df14cce6bc9.json'
    PROPERTY_ID = '407466116'
    starting_date = "90daysAgo"
    ending_date = "yesterday"

    client = BetaAnalyticsDataClient()
    
    def get_request_result(client, property_id):
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[{"start_date": starting_date, "end_date": ending_date}],
            metrics=[{"name": "activeUsers"}]
        )

        response = client.run_report(request)

        # return request response as JSON
        return response

    # Get the request result as JSON using the function
    response = get_request_result(client, PROPERTY_ID)

    # Get the visitor count by filtering the result
    if response and response.row_count > 0:
        metric_value = response.rows[0].metric_values[0].value
    else:
        metric_value = "N/A"  # Handle the case where there is no data

    return f'Number of visitors : {metric_value}'

#=================================================================
# TP3: get google trends for word 'pizza' and 'sushi'
#=================================================================
@app.route('/get_google_trends', methods=['GET'])
def get_google_trends():
    """
    Endpoint to retrieve and display Google Trends data for specified keywords as a line plot.

    This route uses the pytrends library to fetch Google Trends data for 'sushi' and 'pizza' within a specified timeframe,
    generates a line plot to visualize the search interest trends, and displays the plot in an HTML page.

    Returns:
        str: HTML page containing a line plot of Google Trends data.

    Example:
        Access the route '/get_google_trends' in a web browser.
    """
    pytrends = TrendReq(hl='en-US', tz=360)  # Create a pytrends instance with your preferred settings
    pytrends.build_payload(kw_list=['sushi', 'pizza'], timeframe='2019-03-01 2020-10-31')
    data = pytrends.interest_over_time()
    
    # Generate a line plot to see the trends
    plt.figure(figsize=(10, 4))
    plt.plot(data.index, data['sushi'], label='Sushi')
    plt.plot(data.index, data['pizza'], label='Pizza')
    plt.xlabel('Date')
    plt.ylabel('Search Interest')
    plt.title('Google Trends Data')
    plt.legend()

    # Convert the plot to a bytes object and then to base64 for embedding in a web page
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode()
    
    return render_template('trends.html', plot_data=plot_data)


#====================================================================
# TP3: word count experiment and time logs analysis of shakespear.txt
#====================================================================
@app.route('/word_count_experiment', methods=['GET'])
def word_count_experiment():
    """
    Endpoint to perform a word count experiment using two different counting methods and display the results as a boxplot.

    This route loads Shakespeare's text, counts words using dictionary and Counter methods, measures execution times,
    calculates mean and variance, and displays a boxplot of execution times.

    Returns:
        str: HTML page containing the boxplot with execution time distributions.

    Example:
        Access the route '/word_count_experiment' in a web browser.
    """
    # Load Shakespeare's text (you can also download it here if needed)
    with open('shakespeare.txt', 'r') as file:
        shakespeare_text = file.read()

    # Create lists to store execution times and results
    execution_times_dict = []
    execution_times_counter = []

    # Run the experiment 10 times
    for _ in range(100):
        result_dict, execution_time_dict = utils.count_dict(shakespeare_text)
        result_counter, execution_time_counter = utils.count_counter(shakespeare_text)

        execution_times_dict.append((result_dict, execution_time_dict))
        execution_times_counter.append((result_counter, execution_time_counter))

    # Extract execution times from the results
    execution_times_dict = [execution_time for _, execution_time in execution_times_dict]
    execution_times_counter = [execution_time for _, execution_time in execution_times_counter]

    # Calculate the mean and variance for each dataset
    mean_dict = np.mean(execution_times_dict)
    variance_dict = np.var(execution_times_dict)
    mean_counter = np.mean(execution_times_counter)
    variance_counter = np.var(execution_times_counter)

    # Create a boxplot
    data = [execution_times_dict, execution_times_counter]
    labels = ['Using Dictionary\nMean: {:.2f}\nVariance: {:.2f}'.format(mean_dict, variance_dict),
            'Using Counter\nMean: {:.2f}\nVariance: {:.2f}'.format(mean_counter, variance_counter)]

    plt.boxplot(data, labels=labels)
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time Distributions')
    plt.grid(True)

    # Convert the plot to a bytes object and then to base64 for embedding in a web page
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode()

    return render_template('word_count_results.html', plot_data=plot_data)
