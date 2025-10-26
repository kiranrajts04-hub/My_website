from flask import Flask, render_template

# Create Flask app
app = Flask(__name__)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Main entry point
if __name__ == "__main__":
    import os
    # Use Render's assigned port or default 5000
    port = int(os.environ.get("PORT", 5000))
    # Listen on all network interfaces
    app.run(host="0.0.0.0", port=port, debug=True)
