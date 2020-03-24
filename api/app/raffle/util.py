from requests_html import HTMLSession
import re
import json
import threading
from .models import Shoes
from app import db
from flask import session
import ast
import random
from flask_login import (
    current_user,
    login_required
)
from app.base.util import Settings, send_log
from dhooks import Webhook, Embed
from app.base.util import Settings
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask

from app import celery
import time
import random
import numpy as np


def send_hooks(name, site, link, size, email='', password=''):
    settings = Settings()
    try:
        hook = Webhook(settings.webhooks)
    except:
        send_log('Error', 'Invalid Webhook URL')
        return
    embed = Embed(
        description=name,
        color=0xC462DB,
        timestamp='now'  # sets the timestamp to current time
    )

    image1 = 'https://i.imgur.com/6xRknRi.png'
    image2 = 'https://cdn.shopify.com/s/files/1/0027/4445/1133/products/nike-sb-dunk-low-pro-strangelove-shoes-bright-melon-gym-red-medium-soft-pink-1_bd75837e-794f-4b0b-907d-0ee23f4f31bc.jpg?v=1580139863'

    embed.set_author(name='%s Successful Raffle Entry!' % (site))
    embed.add_field(name='Raffle Link', value='||%s||' % (link))
    embed.add_field(name='Sizes', value='US ' + size)
    if email:
        embed.add_field(name='Email', value=email, inline=False)
    if password:
        embed.add_field(name='Password', value='||%s||' % (password))
    embed.set_footer(text='Raven Raffles', icon_url=image1)

    embed.set_image(image2)

    hook.send(embed=embed)


class RaffleSpider:
    def __init__(self):
        self.session = HTMLSession()

        # Store All Products
        self.products = []
        self.run()

    def run(self):
        for spider in (self.RenartsSpider(), self.HanonshopSpider(), self.FootpatrolSpider(), self.FootshopSpider(), self.VooberlinSpider(), self.FlatspotSpider()):
            threading.Thread(target=spider, args=(self,)).start()

    def RenartsSpider(self):
        # Configuration
        site = "renarts"

        api_endpoint = "https://renarts-draw.herokuapp.com/draws/"
        available_raffle_id = []

        homepage_result = self.session.get('https://renarts.com/collections/release-draws')
        for raffle_link in homepage_result.html.find('.product-thumbnail'):
            product_endpoint = api_endpoint + \
                raffle_link.find('.shopify-product-reviews-badge')[0].attrs['data-id']

            product_json_result = self.session.get(product_endpoint).json()[0]

            name = product_json_result['title'].split(' [')[0]
            image = json.loads(product_json_result['product']['image'])['src']
            date = product_json_result['ends_at']
            link = 'https://renarts.com/collections/release-draws/products/'

            variant = {}
            for size in product_json_result['variants']:
                variant[size['variant_label']] = size['draw_id']

            self.products.append(
                {
                    "site": site,
                    "name": name,
                    "image": image,
                    "date": date,
                    "link": link,
                    "variant": variant
                }
            )

    def VooberlinSpider(self):
        # Configuration
        site = 'vooberlin'
        url = 'https://raffle.vooberlin.com/'

        # Get Products
        r = self.session.get(url)

        products = r.html.find('.sub-heading')[0].find('li')
        for product in products:
            name = product.text
            link = product.html.split('"')[1]

            r = self.session.get(link)

            image = r.html.find('img')[1].attrs['src']
            date = r.html.find('br+ center .p+ .p span')[0].text

            # check if it's available
            if r.html.find('input.text-filed'):
                # Get Sizes Variant
                variant = {}

                for size in r.html.find('#ul_top_hypers')[0].find('li'):
                    if "US MEN" in size.text:
                        continue

                    variant[str(size.find('a')[0].text.split(',')[0].replace(' ', ''))
                            ] = str(size.attrs['id'].replace('li_', ''))

                self.products.append(
                    {
                        "site": site,
                        "name": name,
                        "image": image,
                        "date": date,
                        "link": link,
                        "variant": variant
                    }
                )

    def FootshopSpider(self):
        # Configuration
        site = 'footshop'
        url = 'https://releases.footshop.com/'
        apiurl = 'https://releases.footshop.com/api/raffles/'

        # Get Products
        try:
            r = self.session.get(url)
        except:
            return
        try:
            products_raw = r.html.find('.container')[1].find('a')
        except:
            return
        products = []
        for product_raw in products_raw:
            links = product_raw.attrs['href']
            if links not in products:
                products.append(links)
        for product in products:
            r = self.session.get(url + product)
            rjson = json.loads(r.html.find(
                'script')[2].text.replace('window.__INITIAL_STATE__ =', ''))

            name = rjson['raffleDetail']['raffle']['translations']['en']['title'] + \
                ' ' + rjson['raffleDetail']['raffle']['translations']['en']['subtitle']
            image = 'https://1101058148.rsc.cdn77.org/admin/images/raffle/' + \
                rjson['raffleDetail']['raffle']['images'][0]
            date = rjson['raffleDetail']['raffle']['closeRegistrationAt']
            link = apiurl + rjson['raffleDetail']['raffle']['id']
            # Get Sizes Variant
            variant = {}

            try:
                for size in rjson['raffleDetail']['raffle']['sizeSets']['Unisex']['sizes']:
                    variant[size['us']] = size['id']
            except:
                for size in rjson['raffleDetail']['raffle']['sizeSets']['Women']['sizes']:
                    variant[size['us']] = size['id']

            self.products.append(
                {
                    "site": site,
                    "name": name,
                    "image": image,
                    "date": date,
                    "link": link,
                    "variant": variant
                }
            )

    def FootpatrolSpider(self):
        # Configuration
        site = 'footpatrol'
        url = 'https://blog.footpatrol.com/'
        apiurl = 'https://raffles-resources.jdsports.co.uk/raffles/raffles_'
        # Get Products
        r = self.session.get(url)

        productslink = []
        # check raffle
        for article in r.html.find('h2.entry-title'):
            if 'online raffles' in article.text:
                productslink.append(article.find('a')[0].attrs['href'])

        # Iterate Products
        if productslink:
            for productlink in productslink:
                r = self.session.get(productlink)

                for link in r.html.find('a'):
                    if 'https://raffles.footpatrol.com/' in link.attrs['href']:

                        rafflelink = link.attrs['href']
                        raffleid = link.attrs['href'].split('-')[-1]
                        # Found Raffle

                r = self.session.get(apiurl + raffleid + '.js')
                html_raw = r.text

                final = r.text.replace('var raffles = [', '').replace('];', '')
                rjson = json.loads(final)

                variants = {}
                for sizes in rjson['size_options']:
                    size = rjson['size_options'][sizes].split(' ')[0]
                    key = sizes
                    variants[size] = key

                self.products.append(
                    {
                        "site": site,
                        "name": rjson['product_name'],
                        "image": rjson['product_image'],
                        "date": rjson['raffle_end_date'],
                        'site_id_captcha': rjson['captcha'],
                        "link": rafflelink,
                        "variant": variants
                    }
                )

    def HanonshopSpider(self):
        site = 'hanonshop'
        r = self.session.get('https://launches.hanon-shop.com/collections/launch/')

        products_available = r.html.find('div.item.centered.hasLaunchedfalse')
        for product in products_available:
            name = product.find('h2.product-name')[0].text
            link = product.find('a')[0].attrs['href']
            image = product.find('img')[0].attrs['src']
            date = product.find('.launches-time')[0].text.replace('Launches on', '')
            sizes = {}
            # check size
            r = self.session.get('https://launches.hanon-shop.com/' + link + '.json')
            rdata = r.json()

            try:
                for size in rdata['product']['variants']:
                    sizes[size['option1'].split('US ')[1]] = size['id']
            except:
                for size in rdata['product']['variants']:
                    convert_uk_to_us_size(size['option1'].split('UK ')[1])
                    sizes[convert_uk_to_us_size] = size['id']
            self.products.append({
                'site': site,
                'name': name,
                'link': 'https://launches.hanon-shop.com/' + link,
                'image': image,
                'date': date,
                'variant': sizes
            })

    def FlatspotSpider(self):
        site = 'flatspot'
        baseurl = "https://releases.flatspot.com"

        response_releases = self.session.get(
            'https://releases.flatspot.com/collections/releases-flatspot')
        available_raffles = response_releases.html.find(
            'li.prod-item.col-sm-6.col-md-5th.col-lg-5th.prod-item-1')

        for available_raffle in available_raffles:
            raffle_link = baseurl + available_raffle.find('a')[0].attrs['href']

            response_products_json = self.session.get(raffle_link + '.json').json()

            name = response_products_json['product']['title']
            image = response_products_json['product']['images'][0]['src']
            date = response_products_json['product']['body_html'].split("The draw closes on")[
                1].split('.')[0]
            variant = {}
            for size in response_products_json['product']['variants']:
                variant[convert_uk_to_us_size(size['option1'].split('UK ')[1])] = size['id']
            print(name)
            self.products.append({
                'site': site,
                'name': name,
                'link': raffle_link,
                'image': image,
                'date': date,
                'variant': variant
            })

    def process_item(products):
        pass


class RaffleCheckout:
    def __init__(self, tasks_all):
        self.session = HTMLSession()

        self.settings = Settings()
        # self.settings.load_profile_by_id()

        self.tasks_all = tasks_all
        self.tasks_done = []

        self.renarts_tasks = []
        self.footshop_tasks = []
        self.hanonshop_tasks = []
        self.flatspot_tasks = []

    def run(self):
        # Multi Proccess by the sites
        # Filtering
        for task in self.tasks_all['tasks']:
            print(task)
            if task['sites'] == 'renarts':
                self.renarts_tasks.append(task)
            elif task['sites'] == 'footshop':
                self.footshop_tasks.append(task)
            elif task['sites'] == 'hanonshop':
                self.hanonshop_tasks.append(task)
            elif task['sites'] == 'flatspot':
                self.flatspot_tasks.append(task)
        for spider in (self.renarts_bot(self.renarts_tasks), self.footshop_bot(self.footshop_tasks), self.hanon_bot(self.hanonshop_tasks), self.flatspot_bot(self.flatspot_tasks)):
            threading.Thread(target=spider, args=(self,)).start()

    def renarts_bot(self, tasks):
        # Configuration
        name = 'renarts'
        registration_url = 'https://renarts-draw.herokuapp.com/customers/new'
        releases_url = 'https://renarts.com/collections/release-draws'
        submit_raffle_url = 'https://renarts-draw.herokuapp.com/draws/entries/new'
        raffle_checkout_url = 'https://renarts-draw.herokuapp.com/draws/entries/checkout'
        stripe_url = 'https://api.stripe.com/v1/tokens'
        api_url = 'https://renarts-draw.herokuapp.com/login'
        email = "raffle@xxx.com"
        passwd = "raihan123"
        session = HTMLSession()
        headers = {
            'authority': 'renarts.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests_manager': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
        }
        # Iterate to tasks
        for task in tasks:
            print(task)
            # Iterate to task entries
            for i in range(int(task['entries'])):
                raffle_data = get_raffle_by_id(task['shoeid'])

                # Check shoes size
                if ":" in task['size']:
                    choosen_size = random_size_range(task['size'])
                    print("random size: " + str(choosen_size))
                elif task['size'] == 'random':
                    # random choose
                    print(raffle_data['sizes'])
                    choosen_size = random.choice(list(raffle_data['sizes'].keys()))
                else:
                    choosen_size = convert_us_to_int(task['size'])
                is_size_matched = choosen_size in raffle_data['sizes']
                choosen_size_data = ""

                if is_size_matched:
                    # get the data
                    choosen_size_data = raffle_data['sizes'][choosen_size]
                else:
                    # random choose
                    choosen_size_data = random.choice(raffle_data['sizes'])

                # Start bot

                self.settings.load_profile_by_id(task['profileid'])
                print('settings loaded!')

                while True:
                    registration_result = session.post(
                        url=registration_url,
                        headers={
                            'origin': 'https://renarts.com',
                            'referer': 'https://renarts.com',
                            'cache-control': 'max-age=0',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                            'accept': 'application/json, text/javascript, */*; q=0.01',
                        },
                        data={
                            'first_name': self.settings.firstname,
                            'last_name': self.settings.lastname,
                            'email': self.settings.email
                        }
                    )
                    response = registration_result.json()
                    try:
                        print(response['errors'])
                        return response['errors']
                    except:
                        customer_id = response['id']
                    break
                if registration_result.status_code == 200:
                    raffles_page = session.get(
                        url=releases_url
                    )
                if raffles_page.status_code == 200:
                    # Submitting Address
                    submit_raffle = session.post(
                        url=submit_raffle_url,
                        headers={
                            'origin': 'renarts.com',
                            'referer': '{}'.format('https://renarts.com/'),
                            'Sec-Fetch-Mode': 'cors',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                            'accept': 'application/json, text/javascript, */*; q=0.01',
                            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        },
                        data={
                            'shipping_first_name': self.settings.firstname,
                            'shipping_last_name': self.settings.lastname,
                            'customer_id': customer_id,
                            'variant_id': choosen_size_data,
                            'street_address': self.settings.address,
                            'city': self.settings.city,
                            'zip': self.settings.zipcode,
                            'state': self.settings.stateprovince,
                            'phone': self.settings.phonenumber,
                            'country': self.settings.country,
                            'delivery_method': 'online'
                        }
                    )
                if submit_raffle.status_code == 200:
                    submit_raffle_response = json.loads(submit_raffle.text)
                    submit_raffle_message = submit_raffle_response['message']
                    submit_raffle_id = submit_raffle_response['id']
                    submit_raffle_tax = submit_raffle_response['tax']

                    stripe_request = session.post(
                        url=stripe_url,
                        headers={
                            'origin': 'https://js.stripe.com',
                            'referer': 'https://js.stripe.com/v3/controller-6d44288e82d0a800188a2538d642b274.html',
                            'Sec-Fetch-Mode': 'cors',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                            'accept': 'application/json',
                            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        },
                        data={
                            'card[number]': self.settings.cardno,
                            'card[cvc]': self.settings.cvv,
                            'card[exp_month]': self.settings.expmonth,
                            'card[exp_year]': self.settings.expyear,
                            'guid': 'NA',
                            'muid': 'cc6060d3-b78c-47c5-958c-c5f344b53fea',
                            'sid': '6c5280ce-4388-457b-ad66-ab060becb1c2',
                            'payment_user_agent': 'stripe.js/a0ac7be1; stripe-js-v3/a0ac7be1',
                            'referrer': '{}'.format('https://renarts.com/'),
                            'key': 'pk_live_5Lmme6XlFQopCKpv9mkUutcl',
                            'pasted_fields': 'number'
                        }
                    )
                if stripe_request.status_code == 200:
                    stripe_request_response = json.loads(stripe_request.text)
                    stripe_token_id = stripe_request_response['id']

                    checkout_request = session.post(
                        url=raffle_checkout_url,
                        headers={
                            'origin': 'https://renarts.com',
                            'referer': '{}'.format('https://renarts.com/'),
                            'Sec-Fetch-Mode': 'cors',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                            'accept': 'application/json, text/javascript, */*; q=0.01',
                            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        },
                        data={
                            'checkout_token': stripe_token_id,
                            'entry_id': submit_raffle_id,
                        }
                    )
                    if checkout_request.status_code == 200:
                        send_hooks(task['name'], name, task['link'], choosen_size)
                        send_log('Success', task['name'] + ' with US ' + str(choosen_size))
                        pprint('Discord notification sent!', site=self.name, type='success')
                    else:
                        send_log('Error', task['name'] + ' with US ' +
                                 str(choosen_size) + ': ' + checkout_request.text)

                    self.settings.random()

    def hanon_bot(self, tasks):
        name = 'hanonshop'
        url = 'https://launches.hanon-shop.com/'
        account_url = 'https://launches.hanon-shop.com/account'
        register_url = 'https://launches.hanon-shop.com/account/register'
        submit_raffle_url = 'https://launches.hanon-shop.com/wallets/checkouts.json'
        raffle_checkout_url = ''
        site_key = '6LeoeSkTAAAAAA9rkZs5oS82l69OEYjKRZAiKdaF'
        launch_url = 'https://launches.hanon-shop.com/collections/launch/'
        api_url = 'https://deposit.us.shopifycs.com/sessions'
        session = HTMLSession()

        headers = {
            'authority': 'renarts.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests_manager': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
        }

        # Iterate to tasks
        for task in tasks:
            for i in range(int(task['entries'])):
                try:
                    self.settings.random()
                except:
                    pass
                # check
                raffle_details = get_raffle_by_id(task['shoeid'])

                if ":" not in task['size']:
                    choosen_size = task['size'].replace('US ', '')
                else:
                    choosen_size = task['size']
                if ":" in task['size']:
                    choosen_size = random_size_range(task['size'])
                    print("random size: " + str(choosen_size))
                elif task['size'] == 'random':
                    # random choose
                    choosen_size = random.choice(list(raffle_details['sizes'].keys()))
                size_id = raffle_details['sizes'][choosen_size]
                self.settings.load_profile_by_id(task['profileid'])
                print('settings loaded!')
                # Register
                data = {
                    "form_type": "create_customer",
                    "utf8": "✓",
                    "customer[first_name]": self.settings.firstname,
                    "customer[last_name]": self.settings.lastname,
                    "customer[email]": self.settings.email,
                    "customer[password]": self.settings.password
                }

                register_data = self.session.post(account_url, data=data)
                token = register_data.html.find('input[name=authenticity_token]')[0].attrs['value']
                dataregis = {
                    'authenticity_token': token,
                    'g-recaptcha-response': solve_captcha(site_key, register_url)
                }
                regis = session.post('https://launches.hanon-shop.com/account', data=dataregis)

                if regis.status_code != 400:
                    data = {"checkout": {"line_items": [{"variant_id": size_id, "quantity": 1, "properties": {"_render_as": "date_time"}}],
                                         "secret": True, "wallet_name": "PayPalInContext", "is_upstream_button": True, "page_type": "product", "presentment_currency": "GBP"}}
                    headers = {
                        'authority': 'launches.hanon-shop.com',
                        'origin': 'https://launches.hanon-shop.com',
                        'authorization': 'Basic MjA1N2VkZjgzNzZlYWNkY2ZlY2NjNGNiOTVkNWVkZTk=',
                        'accept': 'application/json',
                        'user-agent': '[{"key":"user-agent","value":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36","enabled":true}]',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'en-US,en;q=0.9,id;q=0.8'
                    }

                    submit_raffle_response = session.post(
                        submit_raffle_url, json=data, headers=headers)

                    if submit_raffle_response.status_code == 201:
                        data = {
                            "form_type": "customer_login",
                            "utf8": "✓",
                            "customer[email]": self.settings.email,
                            "customer[password]": self.settings.password,
                            "checkout_url": submit_raffle_response.json()['checkout']['web_url']
                        }

                        login_page_response = session.post(
                            'https://launches.hanon-shop.com/account/login', data=data)
                        if login_page_response.status_code == 200:
                            raffle_checkout_url = login_page_response.html.url
                            token = login_page_response.html.find(
                                'input[name=authenticity_token]')[0].attrs['value']

                            data = {
                                "_method": "patch",
                                "authenticity_token": token,
                                "previous_step": "contact_information",
                                "step": " shipping_method",
                                "checkout[email]": "raihanstarkrk@gmail.com",
                                "checkout[buyer_accepts_marketing]": "0",
                                "checkout[shipping_address][first_name]": "",
                                "checkout[shipping_address][last_name]": "",
                                "checkout[shipping_address][address1]": "",
                                "checkout[shipping_address][address2]": "",
                                "checkout[shipping_address][city]": "",
                                "checkout[shipping_address][country]": "",
                                "checkout[shipping_address][province]": "",
                                "checkout[shipping_address][zip]": "",
                                "checkout[shipping_address][first_name]": self.settings.firstname,
                                "checkout[shipping_address][last_name]": self.settings.lastname,
                                "checkout[shipping_address][address1]": self.settings.address,
                                "checkout[shipping_address][address2]": self.settings.aptsuite,
                                "checkout[shipping_address][city]": self.settings.city.upper(),
                                "checkout[shipping_address][province]": self.settings.stateprovince.upper(),
                                "checkout[shipping_address][country]": self.settings.country,
                                "checkout[shipping_address][zip]": self.settings.zipcode,
                                "g-recaptcha-response": solve_captcha(site_key, register_url),
                                "button": "",
                                "checkout[client_details][browser_width]": "1903",
                                "checkout[client_details][browser_height]": "969",
                                "checkout[client_details][javascript_enabled]": "1"
                            }

                            print(data)
                            r = self.session.post(raffle_checkout_url, data=data)

                            shipping_page_response = self.session.get(
                                raffle_checkout_url + '?previous_step=contact_information&step=shipping_method')

                            token = shipping_page_response.html.find(
                                'input[name=authenticity_token]')[0].attrs['value']
                            data = {
                                "_method": "patch",
                                "authenticity_token": token,
                                "previous_step": " shipping_method",
                                "step": "payment_method",
                                "checkout[shipping_rate][id]": "shopify-Global%20Priority-15.00",
                                "button": " ",
                                "checkout[client_details][browser_width]": "1041",
                                "checkout[client_details][browser_height]": "969",
                                "checkout[client_details][javascript_enabled]": "1"}

                            raffle_checkout_response = session.post(raffle_checkout_url, data=data)
                            content = raffle_checkout_response.text
                            s = raffle_checkout_response.html.find('script.analytics')[0].html.split(
                                '"checkoutToken":"')[1].split('"}},"Performance":')[0]
                            payment_gateway = raffle_checkout_response.html.find(
                                'div.radio-wrapper.content-box__row.content-box__row--secondary')[0].attrs['data-subfields-for-gateway']
                            totalprice = raffle_checkout_response.html.find(
                                'input#checkout_total_price')[0].attrs['value']

                            datajson = {"credit_card": {"number": self.settings.cardno, "name": self.settings.firstname + ' ' + self.settings.lastname, "start_month": None,
                                                        "start_year": None, "month": self.settings.expmonth, "year": self.settings.expyear, "verification_value": self.settings.cvv, "issue_number": ""}}

                            raffle_card_response = session.post(
                                'https://deposit.us.shopifycs.com/sessions', json=datajson)

                            data = {
                                "_method": "patch",
                                "authenticity_token": token,
                                "previous_step": "payment_method",
                                "step": "",
                                "s": '',
                                "checkout[payment_gateway]": payment_gateway,
                                "checkout[different_billing_address]": False,
                                "checkout[total_price]": totalprice,
                                "complete": "1",
                                "checkout[client_details][browser_width]": "1024",
                                "checkout[client_details][browser_height]": "969",
                                "checkout[client_details][javascript_enabled]": "1",

                            }

                            raffle_submit_response = session.post(raffle_checkout_url, data=data)

                            print(raffle_submit_response.text)

    def flatspot_bot(self, tasks):
        name = 'flatspot'
        for task in tasks:
            time.sleep(10)
            send_hooks(task['name'], name, task['link'], task['size'].replace('US ', ''))

    def footshop_bot(self, tasks):
        name = 'Footshop'
        releases_url = 'https://releases.footshop.com'
        get_raffle_details_base_url = 'https://releases.footshop.com/api/raffles/'
        checkout_url = 'https://api2.checkout.com/v2/tokens/card'
        headers = {
            'authority': 'releases.footshop.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests_manager': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
        }

        session = HTMLSession()
        # iterate
        for task in tasks:
            for i in range(int(task['entries'])):
                try:
                    self.settings.random()
                except:
                    pass
                raffle_details = get_raffle_by_id(task['shoeid'])
                choosen_size = convert_us_to_int(task['size'])
                if ":" in task['size']:
                    choosen_size = random_size_range(task['size'])
                    print("random size: " + str(choosen_size))
                elif task['size'] == 'random':
                    # random choose
                    choosen_size = random.choice(list(raffle_data['sizes'].keys()))
                size_id = raffle_details['sizes'][choosen_size]
                raffle_id = raffle_details['link'].replace(
                    "https://releases.footshop.com/api/raffles/", "")
                raffle_url = 'https://releases.footshop.com/register/{}/Unisex/{}'.format(
                    raffle_id, size_id)

                self.settings.load_profile_by_id(task['profileid'])
                print('settings loaded!')
                # Register the size
                raffle_registration = session.get(
                    'https://releases.footshop.com/register/{}/Unisex/{}'.format(raffle_id, size_id), headers=headers)
                if raffle_registration.status_code == 404:
                    raffle_registration = session.get(
                        'https://releases.footshop.com/register/{}/Women/{}'.format(raffle_id, size_id), headers=headers)
                if raffle_registration.status_code == 200:
                    raffle_registration_duplicity_check = session.post('https://releases.footshop.com/api/registrations/check-duplicity/{}'.format(raffle_id),
                                                                       headers={
                        'origin': 'https://releases.footshop.com',
                        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
                        'content-type': 'application/json;charset=UTF-8',
                        'accept': 'application/json, text/plain, */*',
                        'cache-control': 'no-cache',
                        'authority': 'releases.footshop.com',
                        'referer': raffle_url
                    },
                        json={
                        'email': self.settings.email,
                        'phone': self.settings.phonenumber,
                        'id': None
                    })
                    print(raffle_registration_duplicity_check.text)
                    if raffle_registration_duplicity_check.status_code == 200:
                        raffle_registration_duplicity_check_json = json.loads(
                            raffle_registration_duplicity_check.text)
                        raffle_registration_card_checkout = session.post(checkout_url,
                                                                         headers={
                                                                             'Accept': 'application/json, text/javascript, */*; q=0.01',
                                                                             'Referer': 'https://js.checkout.com/frames/?v=1.0.16&publicKey=pk_76be6fbf-2cbb-4b4a-bd3a-4865039ef187&localisation=EN-GB&theme=standard',
                                                                             'Origin': 'https://js.checkout.com',
                                                                             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                                                                             'AUTHORIZATION': 'pk_76be6fbf-2cbb-4b4a-bd3a-4865039ef187',
                                                                             'Content-Type': 'application/json'
                                                                         },
                                                                         json={
                                                                             'number': self.settings.cardno,
                                                                             'expiryMonth': self.settings.expmonth,
                                                                             'expiryYear': self.settings.expyear[len(self.settings.expyear) - 2:],
                                                                             'cvv': self.settings.cvv,
                                                                             'requestSource': 'JS'
                                                                         })
                        if raffle_registration_card_checkout.status_code == 200:
                            print('submitting raffle')
                            card_token = json.loads(raffle_registration_card_checkout.text)['id']
                            print(card_token)
                            raffle_registration_url = 'https://releases.footshop.com/api/registrations/create/{}'.format(
                                raffle_id)
                            data = {
                                'id': None,
                                'sizerunId': size_id,
                                'account': 'New Customer',
                                'email': self.settings.email,
                                'phone': self.settings.phonenumber,
                                'gender': 'Mr',
                                'firstName': self.settings.firstname,
                                'lastName': self.settings.lastname,
                                'birthday': '{}-0{}-0{}'.format(random.randrange(1982, 2000),
                                                                random.randrange(1, 9),
                                                                random.randrange(1, 9)),
                                "deliveryAddress": {
                                    "country": country_formatter(self.settings.country),
                                    "state": self.settings.stateprovince,
                                    "county": "",
                                    "city": self.settings.city,
                                    "street": self.settings.address,
                                    "houseNumber": self.settings.housenumber,
                                    "additional": self.settings.aptsuite,
                                    "postalCode": self.settings.zipcode
                                },
                                "consents": ["privacy-policy-101"],
                                "cardToken": card_token,
                                "cardLast4": self.settings.cardno[len(self.settings.cardno) - 4:]
                            }
                            print(data)
                            raffle_registration = session.post(raffle_registration_url,
                                                               headers={
                                                                   'origin': 'https://releases.footshop.com',
                                                                   'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                                                                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                                                                   'content-type': 'application/json;charset=UTF-8',
                                                                   'accept': 'application/json, text/plain, */*',
                                                                   'cache-control': 'no-cache',
                                                                   'authority': 'releases.footshop.com',
                                                                   'referer': 'https://releases.footshop.com/register/{}/Unisex/{}'
                                                                   .format(raffle_id, size_id)
                                                               },
                                                               json=data)
                            raffle_registration_json = json.loads(raffle_registration.text)
                            # print(raffle_registration_json['errors'])

                            # if response_code == 200:
                            send_hooks(task['name'], name, task['link'], choosen_size)
                            send_log('Success', task['name'] + ' with US ' + str(choosen_size))


def random_size_range(size_range: str):
    range_size_split = size_range.split(' ')[1].split(':')
    randomed_size = np.random.choice(
        np.arange(float(range_size_split[0]), float(range_size_split[1]), 0.5))

    if randomed_size % 1 == 0:
        return str(int(randomed_size))
    else:
        return str(randomed_size)


def convert_us_to_int(size_us: "US 10"):
    return size_us.split(' ')[1]


def convert_uk_to_us_size(uk_size: float):
    us_size = float(uk_size) + 0.5
    if us_size % 1 == 0.0:
        return int(us_size)
    return us_size


def country_formatter(profile_country: str):
    profile_countries = {
        'United Kingdom': 'GB',
        'United States': 'US',
        'Canada': 'CA',
        'North Ireland': 'IE',
        'Germany': 'DE',
        'Switzerland': 'CH',
        'France': 'FR',
        'Spain': 'ES',
        'Italy': 'IT',
        'Netherlands': 'NL',
        'Czech Republic': 'CZ'
    }
    return profile_countries[profile_country]


def solve_captcha(sitekey, url):
    settings = Settings()
    fail_attempt = 0
    try:
        client = AnticaptchaClient(settings.anticaptcha)
        task = NoCaptchaTaskProxylessTask(url, sitekey)
        job = client.createTask(task)
    except:
        send_log('Error', 'AntiCaptcha API ERROR')
    print('solving captcha')
    while True:
        try:
            job.join(60)
            job.get_solution_response()
            break
        except:
            if fail_attempt >= 3:
                print('Solving Recaptcha Failed, Creating Task Again')
                job = client.createTask(task)
            print('Solving Recaptcha Failed, Trying Again')
            fail_attempt += 1
    print('captcha solved')
    return job.get_solution_response()


@celery.task()
def refresh_raffles():
    # Delete all record
    db.session.query(Shoes).delete()
    db.session.commit()

    # Insert Raffles into databse

    products = RaffleSpider().products

    for product in products:
        print(product)
        shoe = Shoes(name=str(product['name']),
                     sites=str(product['site']),
                     img=str(product['image']),
                     sizes=str(product['variant']),
                     link=str(product['link']),
                     date=str(product['date']),
                     price='xxx')
        db.session.add(shoe)
        db.session.commit()
    return 200


def get_all_raffles():
    datas = db.session.query(Shoes).all()

    shoes = []
    for data in datas:
        shoes.append({
            'id': data.id,
            'name': data.name,
            'date': data.date,
            'image': data.img,
            'price': data.price,
            'sizes': data.sizes,
            'sites': data.sites,
            'link': data.link
        })
    return shoes


def get_raffle_by_id(id):
    query = db.session.query(Shoes).filter_by(id=id).first()
    return {
        'id': id,
        'name': query.name,
        'sites': query.sites,
        'price': query.price,
        'img': query.img,
        'date': query.date,
        'link': query.link,
        'sizes': ast.literal_eval(query.sizes)}


def renarts():
    pass
