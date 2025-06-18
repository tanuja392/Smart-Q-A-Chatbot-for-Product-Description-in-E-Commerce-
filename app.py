from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

class EcommerceBot:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        self.headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        }
        # Enhanced product database with categories, prices in rupees, and recommendations
        self.products = {
            # Laptops
            "premium_laptop": {
                "name": "Dell XPS 13",
                "price": 129999,
                "stock": 50,
                "category": "laptops",
                "specs": "13.4-inch FHD+, Intel i7, 16GB RAM, 512GB SSD",
                "recommendations": ["macbook_air", "thinkpad_x1"],
                "placeholder_link": "https://amzn.in/d/f3Tx6HE"
            },
            "macbook_air": {
                "name": "Apple MacBook Air M2",
                "price": 114900,
                "stock": 30,
                "category": "laptops",
                "specs": "13.6-inch Liquid Retina, M2 chip, 8GB RAM, 256GB SSD",
                "recommendations": ["premium_laptop", "macbook_pro"],
                "placeholder_link": "https://amzn.in/d/gSxCCaJ"
            },
            "thinkpad_x1": {
                "name": "Lenovo ThinkPad X1 Carbon",
                "price": 149999,
                "stock": 25,
                "category": "laptops",
                "specs": "14-inch 4K, Intel i7, 16GB RAM, 1TB SSD",
                "recommendations": ["premium_laptop", "macbook_air"],
                "placeholder_link": "https://amzn.in/d/7CxKNrk"
            },

            # Smartphones
            "iphone_15": {
                "name": "Apple iPhone 15",
                "price": 79900,
                "stock": 100,
                "category": "smartphones",
                "specs": "6.1-inch OLED, A16 Bionic, 128GB",
                "recommendations": ["pixel_8", "samsung_s23"],
                "placeholder_link": "https://amzn.in/d/6VND4ao"
            },
            "pixel_8": {
                "name": "Google Pixel 8",
                "price": 75999,
                "stock": 75,
                "category": "smartphones",
                "specs": "6.2-inch OLED, Tensor G3, 128GB",
                "recommendations": ["iphone_15", "samsung_s23"],
                "placeholder_link": "http://surl.li/yzerur"
            },
            "samsung_s23": {
                "name": "Samsung Galaxy S23",
                "price": 74999,
                "stock": 85,
                "category": "smartphones",
                "specs": "6.1-inch Dynamic AMOLED, Snapdragon 8 Gen 2, 256GB",
                "recommendations": ["iphone_15", "pixel_8"],
                "placeholder_link": "https://amzn.in/d/cY1c39E"
            },

            # Audio
            "sony_wh1000xm5": {
                "name": "Sony WH-1000XM5",
                "price": 34990,
                "stock": 200,
                "category": "audio",
                "specs": "Wireless Noise Cancelling, 30hr Battery",
                "recommendations": ["airpods_pro", "bose_qc45"],
                "placeholder_link": "http://surl.li/zrozlr"
            },
            "airpods_pro": {
                "name": "Apple AirPods Pro (2nd Gen)",
                "price": 26900,
                "stock": 150,
                "category": "audio",
                "specs": "Active Noise Cancellation, Spatial Audio",
                "recommendations": ["sony_wh1000xm5", "samsung_buds2_pro"],
                "placeholder_link": "http://surl.li/ysyjin"
            },
            "bose_qc45": {
                "name": "Bose QuietComfort 45",
                "price": 29900,
                "stock": 120,
                "category": "audio",
                "specs": "Wireless Noise Cancelling, 24hr Battery",
                "recommendations": ["sony_wh1000xm5", "airpods_pro"],
                "placeholder_link": "http://surl.li/loclhf"
            },

            # Tablets
            "ipad_air": {
                "name": "iPad Air (5th Gen)",
                "price": 59900,
                "stock": 75,
                "category": "tablets",
                "specs": "10.9-inch Liquid Retina, M1 chip, 64GB",
                "recommendations": ["samsung_tab_s9", "ipad_pro"],
                "placeholder_link": "http://surl.li/whtxtn"
            },
            "samsung_tab_s9": {
                "name": "Samsung Galaxy Tab S9",
                "price": 89999,
                "stock": 60,
                "category": "tablets",
                "specs": "11-inch AMOLED, Snapdragon 8 Gen 2, 256GB",
                "recommendations": ["ipad_air", "ipad_pro"],
                "placeholder_link": "http://surl.li/yilvnl"
            },
            "sonata_watch_sf": {
                "name": "Sonata SF",
                "price": 1200,
                "stock": 25,
                "category": "watches",
                "specs": "Quartz movement, Water-resistant, Black strap",
                "recommendations": ["timex_watch", "fossil_watch"],
                "placeholder_link": "http://surl.li/yilvnl"
            },
            "lg_split_ac": {
                "name": "LG Split AC 1.5 Ton",
                "price": 34990,
                "stock": 10,
                "category": "air_conditioners",
                "specs": "Inverter, 5-star rating, DualCool technology",
                "recommendations": ["voltas_window_ac", "blue_star_split_ac"],
                "placeholder_link": "http://surl.li/yilwom"
            },
            "samsung_double_door_fridge": {
                "name": "Samsung 253L Double Door Refrigerator",
                "price": 22999,
                "stock": 18,
                "category": "refrigerators",
                "specs": "Frost-free, 3-star rating, Digital Inverter Compressor",
                "recommendations": ["lg_double_door", "whirlpool_fridge"],
                "placeholder_link": "http://surl.li/yilwp"
            },
            "sony_bravia_55_inch_tv": {
                "name": "Sony Bravia 55-inch 4K UHD Smart TV",
                "price": 59990,
                "stock": 8,
                "category": "televisions",
                "specs": "55-inch UHD, Android TV, Dolby Vision & Atmos",
                "recommendations": ["samsung_4k_tv", "lg_oled_tv"],
                "placeholder_link": "http://surl.li/yilwq"
            },
            "samsung_tab_s9": {
                "name": "Samsung Galaxy Tab S9",
                "price": 89999,
                "stock": 60,
                "category": "tablets",
                "specs": "11-inch AMOLED, Snapdragon 8 Gen 2, 256GB",
                "recommendations": ["ipad_air", "ipad_pro"],
                "placeholder_link": "http://surl.li/yilvnl"
            },
            "men_casual_shirt": {
                "name": "Allen Solly Men's Casual Shirt",
                "price": 1499,
                "stock": 30,
                "category": "men_clothing",
                "specs": "100% Cotton, Slim Fit, Full Sleeves",
                "recommendations": ["peter_england_shirt", "van_heusen_shirt"],
                "placeholder_link": "http://surl.li/yilws"
            },
            "women_kurta_set": {
                "name": "Biba Women's Kurta Set",
                "price": 1999,
                "stock": 20,
                "category": "women_clothing",
                "specs": "Cotton Blend, 3/4th Sleeves, Ethnic Wear",
                "recommendations": ["w_kurta", "global_desi_kurta"],
                "placeholder_link": "http://surl.li/yilwt"
            },
            "kids_party_dress": {
                "name": "Hopscotch Girls' Party Dress",
                "price": 899,
                "stock": 15,
                "category": "kids_clothing",
                "specs": "Polyester, Sleeveless, Floral Pattern",
                "recommendations": ["cutecumber_girls_dress", "ufo_kids_dress"],
                "placeholder_link": "http://surl.li/yilwu"
            },
            "men_jeans": {
                "name": "Levi's Men's Slim Fit Jeans",
                "price": 2499,
                "stock": 25,
                "category": "men_clothing",
                "specs": "Denim, Stretchable, Slim Fit",
                "recommendations": ["wrangler_jeans", "pepe_jeans"],
                "placeholder_link": "http://surl.li/yilwv"
            },
            "women_top": {
                "name": "AND Women's Top",
                "price": 1299,
                "stock": 18,
                "category": "women_clothing",
                "specs": "Polyester, Ruffled Sleeves, Casual Wear",
                "recommendations": ["only_top", "veromoda_top"],
                "placeholder_link": "http://surl.li/yilww"
            },
            "kids_tshirt": {
                "name": "Puma Kids' T-Shirt",
                "price": 699,
                "stock": 40,
                "category": "kids_clothing",
                "specs": "Cotton, Short Sleeves, Graphic Print",
                "recommendations": ["nike_kids_tshirt", "adidas_kids_tshirt"],
                "placeholder_link": "http://surl.li/yilwx"
            },
            "fortune_sunflower_oil": {
                "name": "Fortune Sunflower Oil - 1L",
                "price": 180,
                "stock": 50,
                "category": "groceries",
                "specs": "Refined Sunflower Oil, 1L, Rich in Vitamins A & D",
                "recommendations": ["saffola_oil", "dhara_oil"],
                "placeholder_link": "http://surl.li/yimab"
            },
            "colgate_toothpaste": {
                "name": "Colgate Strong Teeth Toothpaste - 200g",
                "price": 99,
                "stock": 100,
                "category": "personal_care",
                "specs": "Calcium Enriched Formula, Mint Flavor, 200g",
                "recommendations": ["pepsodent_toothpaste", "sensodyne_toothpaste"],
                "placeholder_link": "http://surl.li/yimac"
            },
            "oralb_toothbrush": {
                "name": "Oral-B Toothbrush - Medium",
                "price": 49,
                "stock": 200,
                "category": "personal_care",
                "specs": "Medium Bristles, Pack of 1, Ergonomic Handle",
                "recommendations": ["colgate_toothbrush", "pepsodent_toothbrush"],
                "placeholder_link": "http://surl.li/yimad"
            },
            "lux_soap": {
                "name": "Lux Jasmine & Almond Oil Soap - 125g",
                "price": 40,
                "stock": 300,
                "category": "personal_care",
                "specs": "Moisturizing Bar Soap, Floral Fragrance, 125g",
                "recommendations": ["dove_soap", "pears_soap"],
                "placeholder_link": "http://surl.li/yimae"
            },
            "usha_ceiling_fan": {
                "name": "Usha Swift Ceiling Fan - 1200mm",
                "price": 2499,
                "stock": 50,
                "category": "home_appliances",
                "specs": "3 Blades, 1200mm Sweep, High Air Delivery",
                "recommendations": ["orient_fan", "havells_fan"],
                "placeholder_link": "http://surl.li/yimaf"
            },
            "philips_led_bulb": {
                "name": "Philips LED Bulb - 12W",
                "price": 199,
                "stock": 150,
                "category": "home_appliances",
                "specs": "12W, Cool Daylight, Energy Efficient",
                "recommendations": ["wipro_led", "syska_led"],
                "placeholder_link": "http://surl.li/yimag"
            }
        }
    def format_price(self, price):
        """Format price in Indian Rupees with appropriate notation"""
        return f"₹{price:,}"

    def format_link(self, text, url):
        """Format a link with blue color using HTML"""
        return f'<a href="{url}" style="color: #0066cc; text-decoration: underline;">{text}</a>'

    def generate_prompt(self, user_input):
        """Generate context-aware prompt for Gemini"""
        lower_input = user_input.lower()
        trigger_words = ["link", "recommend", "suggest", "show", "looking for", "want", "need"]
        
        # Check if this is a product request
        if any(word in lower_input for word in trigger_words):
            for product_id, product in self.products.items():
                if product['name'].lower() in lower_input:
                    # Get recommended products
                    recommendations = [self.products[rec] for rec in product['recommendations']]
                    response = f"Here's the {product['name']}:\n"
                    response += f"Price: {self.format_price(product['price'])}\n"
                    response += f"Specs: {product['specs']}\n"
                    response += f"Link: {self.format_link(product['placeholder_link'], product['placeholder_link'])}\n\n"
                    response += "You might also like:\n"
                    for rec in recommendations:
                        response += f"- {rec['name']} ({self.format_price(rec['price'])}): {self.format_link(rec['placeholder_link'], rec['placeholder_link'])}\n"
                    return response
        
        system_context = f"""
        You are an e-commerce shopping assistant. Current time: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        Available categories: {', '.join(set(p['category'] for p in self.products.values()))}
        
        When recommending products:
        1. Include prices in Indian Rupees (₹)
        2. Mention key specifications
        3. Include direct product links
        4. Suggest similar products with their links
        
        For any product recommendation, always include:
        - Product link
        - Price
        - Key specifications
        - Links to similar products
        
        User query: {user_input}
        """
        return system_context

    def chat(self, user_input):
        """Main chat function"""
        try:
            lower_input = user_input.lower()
            trigger_words = ["link", "recommend", "suggest", "show", "looking for", "want", "need"]
            
            # Check if this is a product request
            if any(word in lower_input for word in trigger_words):
                for product_id, product in self.products.items():
                    if product['name'].lower() in lower_input:
                        # Get recommended products
                        recommendations = [self.products[rec] for rec in product['recommendations']]
                        response = f"Here's the {product['name']}:\n"
                        response += f"Price: {self.format_price(product['price'])}\n"
                        response += f"Specs: {product['specs']}\n"
                        response += f"Link: {self.format_link(product['placeholder_link'], product['placeholder_link'])}\n\n"
                        response += "You might also like:\n"
                        for rec in recommendations:
                            response += f"- {rec['name']} ({self.format_format_price(rec['price'])}): {self.format_link(rec['placeholder_link'], rec['placeholder_link'])}\n"
                        return response
            
            # If no direct product match or not a recommendation request,
            # proceed with Gemini API
            payload = {
                "contents": [{
                    "parts":[{
                        "text": self.generate_prompt(user_input)
                    }]
                }]
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            response_text = result['candidates'][0]['content']['parts'][0]['text']
            
            # Enhance Gemini's response with formatted links if it mentions any products
            for product_id, product in self.products.items():
                if product['name'].lower() in response_text.lower():
                    link_text = f"{product['name']} ({self.format_price(product['price'])})"
                    formatted_link = self.format_link(link_text, product['placeholder_link'])
                    response_text = response_text.replace(
                        product['name'],
                        formatted_link
                    )
            
            return response_text
            
        except requests.exceptions.RequestException as e:
            return f"Sorry, I encountered an error: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

# Initialize the bot with API key
API_KEY = "AIzaSyCmbOQmHEB_1fuCFfPg1US4x5eL6EHXOVM"
bot = EcommerceBot(API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    response = bot.chat(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)