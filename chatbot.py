from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import re
import nltk
import string
import re
import random
import os
import matplotlib.pyplot as plt
import matplotlib
from openai import OpenAI
matplotlib.use('Agg')
app = Flask(__name__)

client = OpenAI(
    api_key="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"
)


def chat_with_gpt3(user_input):
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [{"role":"user","content":user_input}],
        stream = False
    )
    return response.choices[0].message.content
#Functions
def process_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(text)
    tokens = [word for word in tokens if word not in nltk.corpus.stopwords.words('english')]
    return tokens
#Queries
brands_names = ['samsung','iphone','oneplus','redmi','realme','oppo','vivo','nokia','motorola','lg','htc','sony','google','lenovo','huawei','asus','micromax','blackberry','panasonic','gionee','honor','infinix','itel','jio','karbonn','lava','meizu','moto','tecno','coolpad','xolo','zopo','iball','intex','leeco','lyf','mobiistar','nubia','philips','spice','videocon','xiaomi','yureka','zen','ziox','zopo','zuk','apple','micromax','samsung','nokia','sony','lg','htc','motorola','lenovo','xiaomi','huawei','zte','meizu','gionee','oppo','oneplus','vivo','coolpad','xolo','lava','panasonic','iball','intex','leeco','lyf','nubia','philips','spice','videocon','yureka','zen','ziox','zopo','zuk','iberry','acer','alcatel','asus','blackberry','celkon','fly','google','hp','honor','htc','huawei','iball','infocus','intex','karbonn','lava','leeco','lenovo','lg','lyf','meizu','micromax','motorola','nokia','oneplus','oppo','panasonic','philips','samsung','sony','spice','videocon','vivo','xiaomi','xolo','yureka','zen','ziox','zopo','zuk','iberry','acer','alcatel','asus','blackberry','celkon','fly','google','hp','honor','htc','huawei','iball','infocus','intex','karbonn','lava','leeco','lenovo','lg','lyf','meizu','micromax','motorola','nokia','oneplus','oppo','panasonic','philips','samsung','sony','spice','videocon','vivo','xiaomi','xolo','yureka','zen','ziox','zopo','zuk','iberry','acer','alcatel','asus','blackberry','celkon','fly','google','hp','honor','htc','huawei','iball','infocus','intex','karbonn','lava','leeco','lenovo','lg','lyf','meizu','micromax','motorola','nokia','oneplus','oppo','panasonic','philips','samsung','sony','spice','videocon','vivo','xiaomi','xolo','yureka','zen','ziox','zopo','zuk','iberry','acer','alcatel','asus','blackberry','celkon','fly','google','hp','honor','htc','huawei','iball','infocus','intex','karbonn','lava','leeco','lenovo','lg','lyf','meizu','micromax','motorola','nokia','oneplus','oppo','panasonic','philips','samsung','sony','spice','videocon','vivo','xiaomi','xolo','yureka','zen','ziox','zopo','zuk','iberry','acer','alcatel','asus','blackberry','celkon','fly','google','hp','honor','htc','huawei','iball','infocus','intex','karbonn','lava','leeco','lenovo','lg','lyf','meizu','micromax','motorola','nokia','oneplus','oppo','panasonic','philips','samsung','sony','spice','videocon','vivo','xiaomi','xolo','yureka','zen','ziox','zopo','zuk','iberry','acer','alcatel','asus','blackberry','celkon','fly','google','hp','honor','htc','huawei','iball','infocus','intex','karbonn','lava','leeco','lenovo','lg','lyf','meizu','micromax','motorola','nokia','oneplus','oppo','panasonic','philips','samsung','sony','spice','videocon','vivo','xiaomi','xolo','yureka','zen','ziox','zopo','zuk','iberry','acer','alcatel','asus','blackberry','celkon','fly','google','hp','honor','htc','huawei','iball','infocus','intex']
# priceQueries = ['price', 'cost', 'rate', 'budget', 'range']
# ratingQueries = ['rating', 'ratings', 'rate', 'rates']
# nameQueries = ['name', 'names', 'title', 'titles', 'model', 'models', 'product', 'products', 'phone', 'phones', 'mobile', 'mobiles', 'smartphone', 'smartphones', 'cellphone', 'cellphones', 'cell phone', 'cell phones', 'cell', 'cells']
# brandQueries = ['brand', 'brands', 'company', 'companies', 'manufacturer', 'manufacturers', 'make', 'makes', 'producer', 'producers', 'creator', 'creators', 'builder', 'builders', 'developer', 'developers', 'brand name', 'brand names', 'company name', 'company names', 'manufacturer name', 'manufacturer names', 'make name', 'make names', 'producer name', 'producer names', 'creator name', 'creator names', 'builder name', 'builder names', 'developer name', 'developer names']

# priceAboveQueries = ['above', 'more', 'greater', 'higher', 'over', 'exceeding', 'exceed', 'greater than', 'higher than', 'over than', 'exceeding than', 'exceed than']
# priceBelowQueries = ['below', 'less', 'lower', 'under', 'lesser', 'lower than', 'under than', 'lesser than']

# bestPhoneQueries = ['best', 'top', 'greatest', 'highest', 'most', 'excellent', 'finest', 'leading', 'premier', 'prime', 'principal', 'supreme', 'topmost', 'ultimate', 'unrivalled', 'unsurpassed', 'utmost', 'first-class', 'first-rate', 'superlative', 'superior', 'top-notch', 'top-quality', 'top-tier', 'top-drawer', 'top-hole', 'top-flight', 'crack', 'crackerjack', 'dandy', 'great', 'keen', 'nifty', 'peachy', 'slap-up', 'swell', 'smashing', 'bang-up', 'blue-ribbon', 'choice', 'select', 'prize', 'quality', 'quality']


def extract_price_under(user_input):
    regex = r'under\s*(\d+)(k|K)?'
    match = re.search(regex, user_input)
    if match:
        price = int(match.group(1))
        if match.group(2):  # if 'k' or 'K' is present
            price *= 1000
        return price
    return None
def extract_price_over(user_input):
    regex = r'over\s*(\d+)(k|K)?'
    match = re.search(regex, user_input)
    if match:
        price = int(match.group(1))
        if match.group(2):  # if 'k' or 'K' is present
            price *= 1000
        return price
    return None
def extract_price_inbetween(user_input):
    regex = r'between\s*(\d+)(k|K)?\s*and\s*(\d+)(k|K)?'
    match = re.search(regex, user_input)
    if match:
        price1 = int(match.group(1))
        price2 = int(match.group(3))
        if match.group(2):  # if 'k' or 'K' is present
            price1 *= 1000
        if match.group(4):  # if 'k' or 'K' is present
            price2 *= 1000
        return price1, price2
    return None
def extract_rating(user_input):
    regex = r'over\s*a\s*rating\s*of\s*([0-5](?:\.[0-9])?)'
    match = re.search(regex, user_input)
    if match:
        return float(match.group(1))
    return None

def extract_brand(user_input, brands_names):
    for brand in brands_names:
        if brand in user_input.lower():
            return brand
    return None

def extract_spec(user_input, spec_name):
    regex = r'(\d+)\s*GB\s*' + spec_name
    match = re.search(regex, user_input)
    if match:
        return int(match.group(1))
    return None
def extract_spec_from_title(spec_regex, products, spec_name):
    for _, row in products.iterrows():
        match = re.search(spec_regex, row['Title'])
        if match:
            row[spec_name] = int(match.group(1))
    return products
def extract_brand_from_title(title, brands_names):
    for brand in brands_names:
        if brand.lower() in title.lower():
            return brand
    return None
def get_reviews_for_product(product_index):
    reviews = pd.read_csv("reviews.csv")
    reviews = reviews[reviews['id'] == product_index]
    reviews = reviews.head(10)
    return reviews
def chatbotResponse(user_input, products):
    response = ""
    products_filtered = products.copy()
    if 'Brand' not in products_filtered.columns:
        products_filtered['Brand'] = products_filtered['Title'].apply(lambda title: extract_brand_from_title(title, brands_names))
    price_under = extract_price_under(user_input)
    price_over = extract_price_over(user_input)
    price_inbetween = extract_price_inbetween(user_input)
    rating = extract_rating(user_input)
    brand = extract_brand(user_input, brands_names)
    ram = extract_spec(user_input, 'RAM')
    rom = extract_spec(user_input, 'ROM')
    battery = extract_spec(user_input, 'Battery')
    camera = extract_spec(user_input, 'Camera')

    if price_under:
        products_filtered = products_filtered[products_filtered['Price'] <= price_under]
    if price_over:
        products_filtered = products_filtered[products_filtered['Price'] >= price_over]
    if price_inbetween:
        products_filtered = products_filtered[(products_filtered['Price'] >= price_inbetween[0]) & (products_filtered['Price'] <= price_inbetween[1])]
    if rating:
        products_filtered = products_filtered[products_filtered['User Rating'] >= rating]
    if brand:
        products_filtered = products_filtered[products_filtered['Brand'].str.lower() == brand.lower()]
    if ram:
        products_filtered = products_filtered[products_filtered['RAM'] == ram]
    if rom:
        products_filtered = products_filtered[products_filtered['ROM'] == rom]
    if battery:
        products_filtered = products_filtered[products_filtered['Battery'] == battery]
    if camera:
        products_filtered = products_filtered[products_filtered['Camera'] == camera]

    if price_under is None and price_over is None and price_inbetween is None and rating is None and brand is None and ram is None and rom is None and battery is None and camera is None:
        response = chat_with_gpt3(user_input)
        return "A1LL2", products_filtered

    products_filtered = products_filtered.sort_values(by=['Score'], ascending=False)
    if products_filtered.empty:
        response = "Sorry, I could not find any products matching your query."
        return response, products_filtered
    response += "<br><br>Click <a href='/results'>here</a> to see all the results.<br><br>Here are the top 2 results:<br><br>"
    return response, products_filtered


@app.route("/")
def index():
    return render_template('home.html')
@app.route("/chatbot")
def chatbot():
    return render_template('chatbot.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    greetings = ['hi', 'hello', 'hey', 'hola', 'greetings', 'wassup', 'hey there']
    greetings_response = ['howdy', 'hi', 'hey', 'what`s good', 'hello', 'hey there']
    if msg.lower() in greetings:
        return jsonify({"msg": random.choice(greetings_response)})
    response, products = chatbotResponse(msg, products_df)
    if response == "A1LL2":
        response = chat_with_gpt3(msg)
        return jsonify({"msg": response})
    products.to_csv('temp.csv')
    if isinstance(products, pd.DataFrame) and not products.empty:
        bot_response = response
        for i in range(2):
            bot_response += 'Name: ' + str(products.iloc[i]['Title']) + '<br>Price: ' + str(products.iloc[i]['Price']) + 'Rupees<br>Rating: ' + str(products.iloc[i]['User Rating']) + '<br><br>'
    else:
        bot_response = response
    
    return jsonify({"msg": bot_response})

@app.route("/results")
def results():
    products = pd.read_csv('temp.csv') # Load the data
    avg_price = int(products['Price'].mean())
    avg_price = f"Rs. {avg_price}"
    avg_rating = round(products['User Rating'].mean(), 2)
    total_listings = len(products)
    products = products.head(20)
    products_html = ""
    for index, product in products.iterrows():
        product['Price'] = int(product['Price'])
        product['Price'] = f"Rs. {product['Price']}"
        products_html += f"""
    <tr>
        <td>{product['Title']}</td>
        <td>{product['Price']}</td>
        <td>{product['User Rating']}</td>
        <td><a href="{product['link']}" target="_blank">View</a></td>
        <td><a href="/reviews/{index}" class="btn btn-primary">Reviews</a></td>
    </tr>
    """
    return render_template('results.html', products_html=products_html, avg_price=avg_price, avg_rating=avg_rating, total_listings=total_listings)

@app.route("/reviews/<int:product_index>")
def reviews(product_index):
    products = pd.read_csv('temp.csv') # Load the data again
    product = products.iloc[product_index]
    reviews = get_reviews_for_product(product_index)
    print(reviews)
    reviews_html = ""
    for index, review in reviews.iterrows():
        reviews_html += f"""
    <tr>
        <td>{review['Review']}</td>
        <td>{5}</td>
    </tr>
    """
    return render_template('reviews.html',reviews_html=reviews_html, product=product)


@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/top_phones", methods=["GET"])
def top_phones():
    return render_template('top_phones.html')

@app.route("/top_phones_category", methods=["POST"])
def top_phones_category():
    selected_category = request.form['category']
    if selected_category == 'generalA':
        top_phones_list = products_df.sort_values(by=['Score'], ascending=True).head(30)
    elif selected_category == 'priceA':
        top_phones_list = products_df.sort_values(by=['Price'], ascending=True).head(30)
    elif selected_category == 'ratingA':
        top_phones_list = products_df.sort_values(by=['User Rating'], ascending=True).head(30)
    elif selected_category == 'ramA':
        top_phones_list = products_df.sort_values(by=['RAM'], ascending=True).head(30)
    elif selected_category == 'romA':
        top_phones_list = products_df.sort_values(by=['ROM'], ascending=True).head(30)
    elif selected_category == 'generalD':
        top_phones_list = products_df.sort_values(by=['Score'], ascending=False).head(30)
    elif selected_category == 'priceD':
        top_phones_list = products_df.sort_values(by=['Price'], ascending=False).head(30)
    elif selected_category == 'ratingD':
        top_phones_list = products_df.sort_values(by=['User Rating'], ascending=False).head(30)
    elif selected_category == 'ramD':
        top_phones_list = products_df.sort_values(by=['RAM'], ascending=False).head(30)
    elif selected_category == 'romD':
        top_phones_list = products_df.sort_values(by=['ROM'], ascending=False).head(30)
    top_phones_html = ""
    for index, product in top_phones_list.iterrows():
        product['Price'] = int(product['Price'])
        product['Price'] = f"Rs. {product['Price']}"
        top_phones_html += f"""
    <tr>
        <td>{product['Title']}</td>
        <td>{product['Price']}</td>
        <td>{product['User Rating']}</td>
        <td><a href="{product['link']}" target="_blank">View</a></td>
    </tr>
    """
    return render_template('top_phones_results.html', top_phones_html=top_phones_html, selected_category=selected_category)

@app.route("/statistics")
def statistics():
    products_filtered = products_df.copy()
    if 'Brand' not in products_filtered.columns:
        products_filtered['Brand'] = products_filtered['Title'].apply(lambda title: extract_brand_from_title(title, brands_names))
    stats = {
        'average_price': round(products_filtered['Price'].mean(), 2),
        'average_rating': round(products_filtered['User Rating'].mean(),2),
        'most_occuring_brand': products_filtered['Brand'].value_counts().index[0],
        'most_occuring_ram': products_filtered['RAM'].value_counts().index[0],
        'most_occuring_rom': products_filtered['ROM'].value_counts().index[0],
        'cheapest_brand': products_filtered.groupby('Brand')['Price'].mean().sort_values().index[0],
        'expensive_brand': products_filtered.groupby('Brand')['Price'].mean().sort_values(ascending=False).index[0],
    }
    return render_template('statistics.html', stats=stats)

@app.route("/visual_statistics")
def visual_statistics():
    save_brand_bar_chart(products_df)
    generate_ram_pie_chart(products_df)
    save_line_graph(products_df)
    save_price_bar_chart(products_df)
    save_rating_bar_chart(products_df)
    save_rom_bar_chart(products_df)
    price_bar_chart_path = 'static/price_bar_chart.png'
    rating_bar_chart_path = 'static/rating_bar_chart.png'
    rom_bar_chart_path = 'static/rom_bar_chart.png'
    line_graph_path = 'static/line_graph.png'
    brand_chart_path = 'static/brand_bar_chart.png'
    ram_pie_chart_path = 'static/ram_pie_chart.png'
    return render_template('visual_statistics.html', price_bar_chart_path=price_bar_chart_path,
                           rating_bar_chart_path=rating_bar_chart_path, rom_bar_chart_path=rom_bar_chart_path,
                           line_graph_path=line_graph_path, brand_chart_path=brand_chart_path,
                           ram_pie_chart_path=ram_pie_chart_path)


def save_price_bar_chart(data):
    plt.figure(figsize=(10, 6))
    plt.bar(data['Title'], data['Price'], color='#16a085')
    plt.xlabel('Product')
    plt.ylabel('Price')
    plt.title('Price of Products')
    plt.xticks(rotation=45)
    plt.savefig('static/price_bar_chart.png', format='png')
    plt.close()


def save_rating_bar_chart(data):
    plt.figure(figsize=(10, 6))
    plt.bar(data['Title'], data['User Rating'], color='#16a085')
    plt.xlabel('Product')
    plt.ylabel('Rating')
    plt.title('Rating of Products')
    plt.xticks(rotation=45)
    plt.savefig('static/rating_bar_chart.png', format='png')
    plt.close()


def save_rom_bar_chart(data):
    plt.figure(figsize=(10, 6))
    plt.bar(data['Title'], data['ROM'], color='#16a085')
    plt.xlabel('Product')
    plt.ylabel('ROM')
    plt.title('ROM of Products')
    plt.xticks(rotation=45)
    plt.savefig('static/rom_bar_chart.png', format='png')
    plt.close()


def save_line_graph(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Title'], data['Price'], color='#16a085')
    plt.xlabel('Product')
    plt.ylabel('Price')
    plt.title('Price of Products')
    plt.xticks(rotation=45)
    plt.savefig('static/line_graph.png', format='png')
    plt.close()


def save_brand_bar_chart(data):
    plt.figure(figsize=(10, 6))
    brand_counts = data['Brand'].value_counts()
    labels = brand_counts.index
    sizes = brand_counts.values
    plt.bar(labels, sizes, color='#16a085')
    plt.xlabel('Brand')
    plt.ylabel('Count')
    plt.title('Count of Products by Brand')
    plt.xticks(rotation=45)
    plt.savefig('static/brand_bar_chart.png', format='png')
    plt.close()

def generate_ram_pie_chart(data):
    data_copy = data.copy()
    ram_counts = data_copy['RAM'].value_counts()
    labels = ram_counts.index
    sizes = ram_counts.values

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Distribution of RAM Sizes')

    plt.savefig('static/ram_pie_chart.png', format='png')
    plt.close()
if __name__ == '__main__':
    products_df = pd.read_csv('final_products.csv')
    app.run(debug=True)