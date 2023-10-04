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


@app.route("/logger")
def logger():
    # display a log on the server side
    print("Vicky in da place")

    # display a log on the browser side 
    js_code = """
    <script>
        console.log("Hi ! I am a log on the browser side");
    </script>
    """

    return "<p>Logging Page</p>" + js_code