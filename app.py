from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

menu = [
    {"name": "Black Coffee", "price": 5},
    {"name": "Americano", "price": 6},
    {"name": "Espresso", "price": 8},
    {"name": "Latte", "price": 9},
    {"name": "Cappuccino", "price": 10},
    {"name": "Frappuccino", "price": 11},
    {"name": "Flat White", "price": 9},
    {"name": "Cafecito", "price": 200},
    {"name": "Cafe con Leche", "price": 300},
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'step' not in session:
        session['step'] = 0

    if request.method == 'POST':
        if 'reset' in request.form:
            session.clear()
            return redirect(url_for('index'))

        if session['step'] == 0:
            session['name'] = request.form['name']
            if session['name'].lower() == "alison":
                session['step'] = 1
            else:
                session['step'] = 4

        elif session['step'] == 1:
            session['evil_status'] = request.form['evil_status']
            session['step'] = 2

        elif session['step'] == 2:
            session['good_deeds'] = int(request.form['good_deeds'])
            if session['good_deeds'] < 4:
                session.clear()
                return render_template('index.html', message="Get out and don't come back until you have done 4 or more good deeds.", show_reset=True)
            session['step'] = 3

        elif session['step'] == 3:
            session['evil_status_confirm'] = request.form['evil_status_confirm']
            if session['evil_status_confirm'].lower() == "no":
                session.clear()
                return render_template('index.html', message="You need to get out and think about your life choices, come back when you have done at least 4 good deeds.", show_reset=True)
            session['step'] = 4

        elif session['step'] == 4:
            session['has_beard'] = request.form['has_beard']
            if session['has_beard'].lower() == 'yes':
                session['step'] = 5
            else:
                session.clear()
                return render_template('index.html', message="Get out, and come back when you grow one!!", show_reset=True)

        elif session['step'] == 5:
            session['beard_length'] = int(request.form['beard_length'])
            if session['beard_length'] >= 2:
                session['step'] = 6
            else:
                session.clear()
                return render_template('index.html', message="Get out, and come back when you have a beard longer than 2 inches!!", show_reset=True)

        elif session['step'] == 6:
            session['order'] = request.form['order']
            session['step'] = 7

        elif session['step'] == 7:
            session['quantity'] = int(request.form['quantity'])
            price_dict = {item['name']: item['price'] for item in menu}
            session['total'] = price_dict[session['order']] * session['quantity']
            session['step'] = 0
            return render_template('index.html', 
                                   message=f"Sounds good {session['name']}! Thank You for your order. Your total is: ${session['total']}. We'll have your {session['quantity']} {session['order']} ready for you in a moment.",
                                   show_reset=True)
        
        return redirect(url_for('index'))

    step = session['step']
    context = {'step': step}

    if step == 0:
        context['question'] = "Hi, my name is Karen. What is your name?"
    elif step == 1:
        context['question'] = "Oh oh, must Alison be evil, are you?" if session['name'].lower() == "alison" else "Are you evil?"
    elif step == 2:
        context['question'] = "How many good deeds have you done today?"
    elif step == 3:
        context['question'] = "Are you sure?"
    elif step == 4:
        context['question'] = f"Hello, {session['name']}, do you have a beard?"
    elif step == 5:
        context['question'] = "Nice beard! How long is it?"
    elif step == 6:
        context['question'] = "Below is our menu, what can I make you today?"
        context['menu'] = menu
    elif step == 7:
        context['question'] = "How many coffees would you like?"
    
    return render_template('index.html', **context)

if __name__ == '__main__':
    app.run(debug=True)
