from flask import Flask, render_template, redirect, request
import csv

app = Flask(__name__)
lista = list()


def read_story_from_csv():
    try:
        with open('data.csv', 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            story = []
            for row in reader:
                if row[-1] == "False":
                    row[-1] = False
                story.append(row)
    except FileNotFoundError:
        story = []
        with open('data.csv', 'w'):
            pass
    return story


@app.route('/', methods=['GET', 'POST'])
def route_index():
    if request.method == 'GET':
        story = read_story_from_csv()
        return render_template('list.html', story=story)


@app.route('/story', methods=['GET', 'POST'])
def route_new_story():
    if request.method == 'POST':
        story = read_story_from_csv()
        try:
            story_id = int(story[-1][0]) + 1
        except IndexError:
            story_id = 1
        title = request.form.get("title")
        description = request.form.get("story")
        criteria = request.form.get("criteria")
        business_value = request.form.get("business_value")
        estimation = request.form.get("estimation")
        status = request.form.get("select")
        user_story = [story_id, title, description, criteria, business_value, estimation, status, False]
        story.append(user_story)
        with open("data.csv", "w", newline='') as csv_file:
            writer = csv.writer(csv_file)
            for line in story:
                writer.writerow(line)
        return redirect('/')
    return render_template('form.html')


@app.route('/story/<story_id>', methods=['GET', 'POST'])
def route_edit(story_id):
    story = read_story_from_csv()
    if request.method == 'GET':
        edit_story = []
        for row in story:
            if row[0] == story_id:
                edit_story = row
        return render_template("form.html", edit_story=edit_story)
    elif request.method == 'POST':
        for row in story:
            if row[0] == story_id:
                row[1] = request.form.get("title")
                row[2] = request.form.get("story")
                row[3] = request.form.get("criteria")
                row[4] = request.form.get("business_value")
                row[5] = request.form.get("estimation")
                row[6] = request.form.get("select")
                with open("data.csv", "w", newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    for line in story:
                        if line[7] == "":
                            line[7] = False
                        writer.writerow(line)
                return redirect('/')


@app.route('/story/delete/<story_id>', methods=['GET'])
def route_delete(story_id):
    story = read_story_from_csv()
    with open("data.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for row in story:
            if row[0] == story_id:
                row[7] = True
            writer.writerow(row)
    return redirect('/')


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
