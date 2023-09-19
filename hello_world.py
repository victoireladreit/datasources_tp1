from flask import Flask

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