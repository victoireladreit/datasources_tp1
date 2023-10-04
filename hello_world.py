import logging
from flask import Flask, request, render_template
from logging.config import dictConfig

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

@app.route("/")
def hello_world():
    var = """
    <!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-FVQS2TWEVX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-FVQS2TWEVX');
</script>
    """
    return "<p>Hello, World! :)</p>" + var


@app.route("/logger", methods=['GET', 'POST'])
def logger():
    if request.method == 'POST':
        # Retrieve the text from the textarea
        text = request.form.get('textarea')
  
        # Print the text in terminal for verification
        logging.info(text)
  
    return render_template('logger.html')