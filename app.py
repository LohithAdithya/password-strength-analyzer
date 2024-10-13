from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# Function to evaluate password strength
def password_strength(password):
    # Length check
    length = len(password)
    
    # Define character categories
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    
    # Calculate strength score
    score = 0
    if length >= 8:
        score += 1
    if has_lower and has_upper:
        score += 1
    if has_digit:
        score += 1
    if has_special:
        score += 1

    # Determine strength level
    if score == 4:
        strength = "Strong"
    elif score == 3:
        strength = "Moderate"
    else:
        strength = "Weak"
    
    # Provide suggestions
    suggestions = []
    if length < 8:
        suggestions.append("Increase the length to at least 8 characters.")
    if not has_lower or not has_upper:
        suggestions.append("Include both lowercase and uppercase characters.")
    if not has_digit:
        suggestions.append("Include at least one digit.")
    if not has_special:
        suggestions.append("Include at least one special character (e.g., !, @, #, etc.).")
    
    return strength, suggestions

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to analyze password
@app.route('/analyze', methods=['POST'])
def analyze():
    password = request.form['password']
    strength, suggestions = password_strength(password)
    return jsonify({'strength': strength, 'suggestions': suggestions})

if __name__ == '__main__':
    app.run(debug=True)
