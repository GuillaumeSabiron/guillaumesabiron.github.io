from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    #return render_template('index_mine.html')
    return render_template('index.html')


@app.route('/header')
def header():
    return render_template('header.html')

@app.route('/experience')
def experience():
    return render_template('experience.html')

@app.route('/expertise')
def expertise():
    return render_template('expertise.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/references')
def references():
    return render_template('references.html')

@app.route('/interests')
def interests():
    return render_template('interests.html')

@app.route('/awards')
def awards():
    return render_template('awards.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/footer')
def footer():
    return render_template('footer.html')

if __name__ == '__main__':
    app.run(debug=True)
