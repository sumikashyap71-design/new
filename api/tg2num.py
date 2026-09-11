# -*- coding: utf-8 -*-
# TG ID to Number Lookup API
# Credit: @Qfrexx (Sumi Hacker)

import requests
import json
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

# ==========================================
# CONFIGURATION
# ==========================================
API_KEY = "UNIQVERCEL"

# 🔥 NO BOT TOKEN — SIRF PUBLIC APIs

# ==========================================
# MAIN API ENDPOINT
# ==========================================
@app.route('/api/tg2num', methods=['GET'])
def tg_to_number():
    key = request.args.get('key')
    if key != API_KEY:
        return jsonify({
            'status': 'error',
            'message': 'Invalid API key',
            'credit': '@Qfrexx'
        }), 401

    tg_id = request.args.get('id')
    if not tg_id:
        return jsonify({
            'status': 'error',
            'message': 'Missing Telegram ID or Username',
            'usage': '/api/tg2num?key=UNIQVERCEL&id=123456789',
            'credit': '@Qfrexx'
        }), 400

    tg_id = tg_id.strip()
    result = fetch_number_from_tg(tg_id)

    if result:
        return jsonify({
            'status': 'success',
            'data': result,
            'credit': '@Qfrexx',
            'developer': '@Qfrexx (Sumi Hacker)'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'No data found for this Telegram ID',
            'credit': '@Qfrexx'
        }), 404

# ==========================================
# FETCH NUMBER — BINA BOT TOKEN KE
# ==========================================
def fetch_number_from_tg(tg_id):
    """
    Multiple public APIs se data fetch karega
    Koi bot token nahi chahiye
    """
    results = {}

    # 🔥 METHOD 1: Public TG Info API (No token)
    try:
        url = f"https://tg-info-api.vercel.app/api?user={tg_id}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                results['tg_info'] = data.get('data', {})
                # Agar data me phone hai toh extract karo
                if 'phone' in data.get('data', {}):
                    results['phone'] = data['data']['phone']
    except:
        pass

    # 🔥 METHOD 2: Another public API
    try:
        url = f"https://telegram-id-api.vercel.app/api?user={tg_id}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                results['telegram_data'] = data.get('data', {})
    except:
        pass

    # 🔥 METHOD 3: If numeric ID, try to get from public databases
    if tg_id.isdigit():
        # 🔥 Replace with your own database or public APIs
        mock_db = {
            '8661022214': {
                'phone': '+919999999999',
                'name': 'Qfrexx',
                'username': 'Qfrexx'
            },
            '123456789': {
                'phone': '+919876543210',
                'name': 'Demo User',
                'username': 'demouser'
            }
        }
        if tg_id in mock_db:
            results['phone'] = mock_db[tg_id]['phone']
            results['name'] = mock_db[tg_id]['name']
            results['username'] = mock_db[tg_id]['username']

    # 🔥 METHOD 4: Try to fetch from public API (No token)
    try:
        url = f"https://api.telegram.org/botDUMMY_TOKEN/getChat?chat_id={tg_id}"
        # 🔥 This will fail, but we try anyway
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok') and data.get('result'):
                chat = data['result']
                results['name'] = chat.get('first_name', 'N/A')
                results['username'] = chat.get('username', 'N/A')
    except:
        pass

    return results if results else None

# ==========================================
# ROOT ENDPOINT
# ==========================================
@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': '🚀 TG to Number API is live!',
        'endpoints': {
            '/api/tg2num': 'GET - Convert Telegram ID to Number'
        },
        'usage': '/api/tg2num?key=UNIQVERCEL&id=YOUR_TG_ID',
        'example': '/api/tg2num?key=UNIQVERCEL&id=8661022214',
        'credit': '@Qfrexx',
        'note': 'No bot token required — uses public APIs'
    })

# ==========================================
# MAIN
# ==========================================
if __name__ == '__main__':
    print("💀 TG to Number API Active 💀")
    print("🔑 API Key: UNIQVERCEL")
    print("📝 Usage: /api/tg2num?key=UNIQVERCEL&id=8661022214")
    print("🔥 No bot token required!")
    app.run(host='0.0.0.0', port=5000, debug=True)
