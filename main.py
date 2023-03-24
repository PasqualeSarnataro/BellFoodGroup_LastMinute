from employeeInfo import dicEmployee
from flask import Flask, request, render_template
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot

import json
app = Flask(__name__, static_folder='static')


@app.route('/')
def index():
    return render_template('sign-in.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    empl = int(request.form['number'])
    global id
    id = empl
    my_dict = dicEmployee(empl)

    count_0 = 0
    count_1 = 0

    for key, value in my_dict.items():
        if type(value) == dict:
            for k, v in value.items():
                if v == 0:
                    count_0 += 1
                elif v == 1:
                    count_1 += 1
        else:
            if value == 0:
                count_0 += 1
            elif value == 1:
                count_1 += 1
    result = count_1/(count_0+count_1)*10+1
    if int(result) == 10:
        return render_template('app.html', result=int(result))
    else:
        val = str(int(result)).zfill(2)
        print(val)
        return render_template('app.html', result=val)


@app.route('/profile')
def profile():
    my_dict = dicEmployee(id)
    print(my_dict)
    return render_template("profile.html", data=my_dict)

@app.route('/ecobank')
def ecobank():
    return render_template("ecobank.html")

@app.route('/marketplace')
def marketplace():
    return render_template("marketplace.html")


@app.route('/dashboard')
def dashboard():
    # Read the CSV file into a pandas DataFrame
    dftrash = pd.read_csv('trash_factories.csv')
    dfproduced = pd.read_csv('produced_food.csv')
    dfpurchase = pd.read_csv('purchase.csv')
    dfLearn = pd.read_csv('learning.csv')

    # Group the DataFrame by the 'trash' column and sum the 'weight' column
    trashType = dftrash.groupby('trash')['weight'].sum()
    factoryTrash = dftrash.groupby('factory_id')['weight'].sum()
    proximity = dfpurchase[dfpurchase['origin'] == 'switzerland'].groupby('factory_id')['kg'].sum()
    factoryRecycling = dfproduced[dfproduced['recicled'] == 1].groupby('factory_id')['kg'].sum()
    video_avg_hours = dfLearn[dfLearn['learning'] == 'video']['hours'].mean()
    seminars_avg_hours = dfLearn[dfLearn['learning'] == 'seminar']['hours'].mean()

    trashType = go.Bar(x=trashType.index, y=trashType['trash'])
    factoryTrash = go.Bar(x=factoryTrash.index, y=factoryTrash['weight'])
    proximity = go.Bar(x=proximity.index, y=proximity['kg'])
    factoryRecycling = go.Bar(x=factoryRecycling.index, y=factoryRecycling['kg'])
    video_avg_hours = go.Bar(x=video_avg_hours.index, y=video_avg_hours['hours'])
    seminars_avg_hours = go.Bar(x=seminars_avg_hours.index, y=seminars_avg_hours['hours'])


    layout = go.Layout(title='Trash Production',
                       xaxis=dict(title='Trash type'),
                       yaxis=dict(title='Trash in kg'))
    # create figure
    fig = go.Figure(data=trashType, layout=layout)
    # plot figure in HTML page
    trashtype_fig = plot(fig, output_type='div')

    layout = go.Layout(title='Factory Trash',
                       xaxis=dict(title='Factory ID'),
                       yaxis=dict(title='Trash in kg'))
    # create figure
    fig = go.Figure(data=factoryTrash, layout=layout)
    # plot figure in HTML page
    trash_fig = plot(fig, output_type='div')

    layout = go.Layout(title='Proximity',
                       xaxis=dict(title='Factory ID'),
                       yaxis=dict(title='Kg from Switzerland'))
    # create figure
    fig = go.Figure(data=proximity, layout=layout)
    # plot figure in HTML page
    prox_fig = plot(fig, output_type='div')

    return render_template('index.html', trashtype_fig=trashtype_fig, trash_fig=trash_fig, prox_fig=prox_fig)


if __name__ == '__main__':
    app.run(debug=True)
