from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

order_list = []


def load_bike_parts():
    df = pd.read_excel('bike_parts.xlsx')
    df['brand'].fillna('', inplace=True)
    df['subcategory'].fillna('', inplace=True)
    df['subcategory_image'].fillna('', inplace=True)
    bike_parts = df.to_dict(orient='records')
    return bike_parts


@app.route('/')
def index():
    bike_parts = load_bike_parts()
    return render_template('index.html', bike_parts=bike_parts)


@app.route('/order', methods=['POST'])
def order():
    global order_list
    bike_parts = load_bike_parts()
    order_list = []
    for part in bike_parts:
        quantity = int(request.form.get(f"quantity_{part['id']}", 0))
        extra_info = request.form.get(f"extra_info_{part['id']}", "")
        if quantity > 0:
            order_list.append({
                "id": part['id'],
                "name": part['name'],
                "brand": part['brand'],
                "model": part['model'],
                "subcategory": part['subcategory'],
                "quantity": quantity,
                "extra_info": extra_info
            })

    # Handle multiple new parts
    new_names = request.form.getlist("new_name[]")
    new_brands = request.form.getlist("new_brand[]")
    new_models = request.form.getlist("new_model[]")
    new_subcategories = request.form.getlist("new_subcategory[]")
    new_quantities = request.form.getlist("new_quantity[]")
    new_extra_infos = request.form.getlist("new_extra_info[]")

    for i in range(len(new_names)):
        new_name = new_names[i]
        new_brand = new_brands[i]
        new_model = new_models[i]
        new_subcategory = new_subcategories[i]
        new_quantity = int(new_quantities[i])
        new_extra_info = new_extra_infos[i]
        if new_name and new_quantity > 0:
            order_list.append({
                "id": "New",
                "name": new_name,
                "brand": new_brand,
                "model": new_model,
                "subcategory": new_subcategory,
                "quantity": new_quantity,
                "extra_info": new_extra_info
            })

    return render_template('order_list.html', order_list=order_list)


@app.route('/clear', methods=['POST'])
def clear():
    global order_list
    order_list = []
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
