
from flask import Flask, jsonify, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164"
                  " Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/query/<food>")
def search_food(food):
    try:
        search_url = f"https://www.nutritionvalue.org/search.php?food_query={food}"
        response = requests.get(url=search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        soup_urls = soup.find_all("a", class_="table_item_name")
        links = [{"link": f'https://www.nutritionvalue.org{url["href"]}', "title": url["title"]} for url in soup_urls]


        return jsonify(links)

    except:
        return jsonify("We're very sorry but an error occurred")


@app.route("/food-nutrient")
def get_food():
    try:
        url = request.args.get('url')
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find("table", id="nutrition-label")
        inner_table = table.find("table")

        clean_html_table = str(inner_table).replace('"', "'").replace("\n", " ").replace("colspan='2' style='background-color:black;padding:0px;height:1px'>", "><hr>")
        images = soup.find_all("img")
        graphs = [image["src"] for image in images]

        data = {
            "food_imgurl": "None" if graphs[0].startswith('http') else f"https://www.nutritionvalue.org{graphs[0]}",
            "table": clean_html_table,
            "graphs": graphs[1:] if not graphs[0].startswith('http') else graphs,
        }

        return jsonify(data)

    except:
        return jsonify("We're very sorry but an error occurred")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
