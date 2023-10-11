import logging
from flask import Flask, request, render_template
from logging.config import dictConfig
import requests

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

# Google request page displaying status code and cookies of request
@app.route('/google', methods=['GET', 'POST'])
def google_request():
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

# Google AAnalytics request page displaying status code, cookies and result of request
@app.route("/google-analytics", methods=['GET', 'POST'])
def google_analytics_request():
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

@app.route("/logger", methods=['GET', 'POST'])
def logger():
    if request.method == 'POST':
        # Retrieve the text from the textarea
        text = request.form.get('textarea')
  
        # Print the text in terminal for verification
        logging.info(text)
  
    return render_template('logger.html')