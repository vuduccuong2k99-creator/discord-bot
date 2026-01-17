
import aiohttp
import asyncio
import os
import random
import time

status_lock = asyncio.Lock()
status_data = {}
hot_nhay = 0
message_lock = asyncio.Lock()

def _clr():
    cmd = 'cls' if os.name == 'nt' else 'clear'
    os.system(cmd)

def __pham_anh_tien__():
    banner = """
1: NHÂY
2: TREO
"""
    return banner

__TISA108__ = {
    'Author': 'Pham Anh Tien',
    'Comment': 'Mày mà bán là tao giết mày',
}

async def _u_stt(token_id, token_display, channel_name, count, status, che_do):
    async with status_lock:
        status_data[token_id] = {
            'token_display': token_display,
            'channel_name': channel_name,
            'count': count,
            'status': status,
            'che_do': che_do
        }
        _clr()
        print(f"Chức năng: {che_do}")
        print()
        for key in sorted(status_data.keys()):
            data = status_data[key]
            print(f"Token: {data['token_display']} > Lần: {data['count']:02d} > {data['status']} > Kênh: {data['channel_name']}")

def _noi_chung_la_vip(token):
    return {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/json',
        'Origin': 'https://discord.com',
        'Referer': 'https://discord.com/channels/@me',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'X-Discord-Locale': 'vi',
        'X-Discord-Timezone': 'Asia/Ho_Chi_Minh',
        'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InZpLVZOIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIyLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI4MTgzOCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ=='
    }

async def _get_ten(session, token):
    url = 'https://discord.com/api/v10/users/@me'
    try:
        async with session.get(url, headers=_noi_chung_la_vip(token), timeout=aiohttp.ClientTimeout(total=15)) as response:
            if response.status == 200:
                user_data = await response.json()
                if 'global_name' in user_data and user_data['global_name']:
                    return user_data['global_name']
                else:
                    return 'NoDisplayName'
    except:
        pass
    return 'ErrorToken'

async def _get_ten_chat(session, token, channel_id):
    url = f'https://discord.com/api/v10/channels/{channel_id}'
    try:
        async with session.get(url, headers=_noi_chung_la_vip(token), timeout=aiohttp.ClientTimeout(total=15)) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('name', f'Channel-{channel_id}')
    except:
        pass
    return f'Kênh-{channel_id}'

async def fake_typing(session, token, channel_id):
    url = f'https://discord.com/api/v10/channels/{channel_id}/typing'
    try:
        async with session.post(url, headers=_noi_chung_la_vip(token), timeout=aiohttp.ClientTimeout(total=10)) as response:
            pass
    except:
        pass

def _them_vo_lam_mau(content):
    if random.randint(1, 3) <= 15:
        invisible_chars = ['\u200B', '\u200C', '\u200D', '\u2060', '\u180E', '\uFEFF']
        return content + random.choice(invisible_chars)
    return content

async def _nhayvip(session, token, channel_id, messages, nguoi_tag, delay, fake_typing_enabled, token_id):
    global hot_nhay
    
    url = f'https://discord.com/api/v10/channels/{channel_id}/messages'
    
    token_display = await _get_ten(session, token)
    channel_name = await _get_ten_chat(session, token, channel_id)
    send_count = 0
    tag_index = 0
    total_messages = len(messages)
    
    while True:
        if fake_typing_enabled:
            await fake_typing(session, token, channel_id)
        
        async with message_lock:
            current_index = hot_nhay
            hot_nhay = (hot_nhay + 1) % total_messages
        
        tin_nhan = messages[current_index]
        
        if not tin_nhan.startswith('#'):
            tin_nhan = f"# {tin_nhan}"
        
        if nguoi_tag:
            tag_hien_tai = nguoi_tag[tag_index]
            tag_index = (tag_index + 1) % len(nguoi_tag)
            
            vi_tri = random.choice(['dau', 'cuoi'])
            
            if vi_tri == 'dau':
                tin_nhan = tin_nhan.replace("# ", f"# {tag_hien_tai} ", 1)
            else:
                tin_nhan = f"{tin_nhan} {tag_hien_tai}"
        
        tin_nhan = _them_vo_lam_mau(tin_nhan)
        
        nonce = str(int(time.time() * 1000000000)) + str(random.randint(1000, 9999))
        
        payload = {
            'content': tin_nhan,
            'nonce': nonce,
            'tts': False
        }
        
        try:
            async with session.post(url, headers=_noi_chung_la_vip(token), json=payload, timeout=aiohttp.ClientTimeout(total=25)) as response:
                
                if response.status == 200:
                    send_count += 1
                    await _u_stt(token_id, token_display, channel_name, send_count, "Thành công", "NHÂY")
                    await asyncio.sleep(delay + random.uniform(0.5, 2.0))
                    
                elif response.status == 429:
                    data = await response.json()
                    retry_after = data.get('retry_after', delay)
                    await asyncio.sleep(retry_after)
                    
                elif response.status == 401:
                    await _u_stt(token_id, token_display, channel_name, send_count, "Thất bại: Token không hợp lệ", "NHÂY")
                    await asyncio.sleep(delay)
                    
                elif response.status == 403:
                    await _u_stt(token_id, token_display, channel_name, send_count, "Thất bại: Không có quyền", "NHÂY")
                    await asyncio.sleep(delay)
                    
                elif response.status == 404:
                    await _u_stt(token_id, token_display, channel_name, send_count, "Thất bại: Kênh không tồn tại", "NHÂY")
                    await asyncio.sleep(delay)
                    
                else:
                    await _u_stt(token_id, token_display, channel_name, send_count, f"Thất bại: {response.status}", "NHÂY")
                    await asyncio.sleep(delay)
                    
        except Exception as e:
            await _u_stt(token_id, token_display, channel_name, send_count, f"Thất bại: {str(e)[:30]}", "NHÂY")
            await asyncio.sleep(delay)

async def _treovip(session, token, channel_id, noi_dung_full, delay, token_id):
    url = f'https://discord.com/api/v10/channels/{channel_id}/messages'
    
    token_display = await _get_ten(session, token)
    channel_name = await _get_ten_chat(session, token, channel_id)
    send_count = 0
    
    while True:
        tin_nhan = noi_dung_full
        
        nonce = str(int(time.time() * 1000000000)) + str(random.randint(1000, 9999))
        
        payload = {
            'content': tin_nhan,
            'nonce': nonce,
            'tts': False
        }
        
        try:
            async with session.post(url, headers=_noi_chung_la_vip(token), json=payload, timeout=aiohttp.ClientTimeout(total=25)) as response:
                
                if response.status == 200:
                    send_count += 1
                    await _u_stt(token_id, token_display, channel_name, send_count, "Thành công", "TREO")
                    await asyncio.sleep(delay + random.uniform(0.5, 2.0))
                    
                elif response.status == 429:
                    data = await response.json()
                    retry_after = data.get('retry_after', delay)
                    await asyncio.sleep(retry_after)
                    
                elif response.status == 401:
                    await _u_stt(token_id, token_display, channel_name, send_count, "Thất bại: Token không hợp lệ", "TREO")
                    await asyncio.sleep(delay)
                    
                elif response.status == 403:
                    await _u_stt(token_id, token_display, channel_name, send_count, "Thất bại: Không có quyền", "TREO")
                    await asyncio.sleep(delay)
                    
                elif response.status == 404:
                    await _u_stt(token_id, token_display, channel_name, send_count, "Thất bại: Kênh không tồn tại", "TREO")
                    await asyncio.sleep(delay)
                    
                else:
                    await _u_stt(token_id, token_display, channel_name, send_count, f"Thất bại: {response.status}", "TREO")
                    await asyncio.sleep(delay)
                    
        except Exception as e:
            await _u_stt(token_id, token_display, channel_name, send_count, f"Thất bại: {str(e)[:30]}", "TREO")
            await asyncio.sleep(delay)

def doc_token():
    while True:
        file_token = input("Nhập file chứa token: ").strip()
        if os.path.exists(file_token):
            with open(file_token, 'r', encoding='utf-8') as f:
                tokens = [line.strip() for line in f if line.strip()]
            return tokens
        print("File không tồn tại!")

def nhap_delay(tokens):
    delays = {}
    for token in tokens:
        token_hien = token[:4] + "..." + token[-4:]
        while True:
            try:
                delay = float(input(f"Token {token_hien} > Delay (giây): "))
                delays[token] = delay
                break
            except:
                print("Vui lòng nhập số!")
    return delays

def nhap_kenh():
    return input("Nhập ID kênh: ").strip()

def _nhap_uid():
    print("Nhập ID người cần tag (nhập 'done' để dừng, Enter để bỏ qua):")
    nguoi_tag = []
    while True:
        user_id = input(f"ID {len(nguoi_tag) + 1}: ").strip()
        if user_id.lower() == 'done' or user_id == '':
            break
        nguoi_tag.append(f"<@{user_id}>")
    return nguoi_tag

def _yes_no_ok():
    while True:
        choice = input("Bật fake typing? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        print("Vui lòng chọn y hoặc n!")

def _msg_nhay():
    file_tn = "nhay.txt"
    if os.path.exists(file_tn):
        with open(file_tn, 'r', encoding='utf-8') as f:
            messages = [line.strip() for line in f if line.strip()]
        return messages
    else:
        print("File nhay.txt không tồn tại!")
        exit()

def _msg_treo():
    while True:
        file_tn = input("Nhập file chứa tin nhắn: ").strip()
        if os.path.exists(file_tn):
            with open(file_tn, 'r', encoding='utf-8') as f:
                noi_dung = f.read().strip()
            return noi_dung
        print("File không tồn tại!")

async def che_do_nhay():
    tokens = doc_token()
    channel_id = nhap_kenh()
    nguoi_tag = _nhap_uid()
    fake_typing_enabled = _yes_no_ok()
    messages = _msg_nhay()
    delays = nhap_delay(tokens)
    
    print("\nLoading...")
    await asyncio.sleep(0.5)
    
    connector = aiohttp.TCPConnector(limit_per_host=10, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for i, token in enumerate(tokens, 1):
            task = asyncio.create_task(
                _nhayvip(
                    session,
                    token,
                    channel_id,
                    messages,
                    nguoi_tag,
                    delays[token],
                    fake_typing_enabled,
                    i
                )
            )
            tasks.append(task)
        
        await asyncio.gather(*tasks)

async def che_do_treo():
    tokens = doc_token()
    channel_id = nhap_kenh()
    noi_dung_full = _msg_treo()
    delays = nhap_delay(tokens)
    
    print("\nLoading...")
    await asyncio.sleep(0.5)
    
    connector = aiohttp.TCPConnector(limit_per_host=10, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for i, token in enumerate(tokens, 1):
            task = asyncio.create_task(
                _treovip(
                    session,
                    token,
                    channel_id,
                    noi_dung_full,
                    delays[token],
                    i
                )
            )
            tasks.append(task)
        
        await asyncio.gather(*tasks)

async def __pham_anh_tien_dep_try__():
    _clr()
    print("Author: Pham Anh Tien")
    print("Comment: Mày mà bán là tao giết mày\n")
    print(__pham_anh_tien__())
    
    while True:
        lua_chon = input("Chọn chức năng(1/2): ").strip()
        if lua_chon == '1':
            await che_do_nhay()
            break
        elif lua_chon == '2':
            await che_do_treo()
            break
        else:
            print("Vui lòng chọn 1 hoặc 2!")

asyncio.run(__pham_anh_tien_dep_try__())