import hashlib
from flask import Flask, request, render_template_string

app = Flask(__name__)

# SHA-256 hashes of the valid strings. This prevents the plaintext strings from leaking.
VALID_HASHES = {
    "854e2b57feda820d9c2d2b9e8f9f53bc1093ec18b7930641e66ab7e652782094",
    "c3c4a603c7903d6edbf9afa906af6d6ddd97a0d25b7c558a4eaaec0a8fd91679",
    "aa5aacd0be447160c7ed533dd5cb7b62ea49059934d4f6a4310a22c1aa3f7e16",
    "4efc597c1962f1402b03ed0055189aedac62d7cb2c126217ce084ff23bbe0853",
    "46ec9d9cbb59a1bcb940518a29af99f2f459a53897c754bcb19c5d4cd8271941",
    "e9af058f38904446c29394a6ab6c567d47dd5ec84562a7e49675fe4234479191",
    "369ec126c1233a467314026f44f4766fcff80d82d225dd4d80b1e180e31b52a1",
    "48131cc02783a3e1ea6b51ea38ce7ec46d45a3a1d01dccbf668e4f286f4b41c8",
    "d4c2291aeeb3106558e5c16db1e2011102f897bf9599cad34727b50b8d314ac5",
    "5793a837f830d862e8d2b0ad48fd36fc6a6144e963baa1dd08f8000e2b3f875d"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flag Validator</title>
</head>
<body>
    <h1>Flag Validator</h1>
    <div>
        <form method="POST">
            <label for="flag">Enter your flag:</label><br><br>
            <input type="text" id="flag" name="flag" required autofocus>
            <br><br>
            <button type="submit">Validate</button>
        </form>
    </div>
    <br>
    {% if message %}
        <div><strong>{{ message }}</strong></div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    status = None
    if request.method == "POST":
        flag = request.form.get("flag", "").strip()
        flag_hash = hashlib.sha256(flag.encode()).hexdigest()
        
        if flag_hash in VALID_HASHES:
            message = "Flag valid."
            status = "valid"
        else:
            message = "Flag invalid."
            status = "invalid"
            
    return render_template_string(HTML_TEMPLATE, message=message, status=status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
