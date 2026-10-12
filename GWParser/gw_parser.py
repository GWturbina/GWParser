# -*- coding: utf-8 -*-
# ===========================================================================
# GW PARSER v3.2 (12.10.2026) - сборщик ищущих из Telegram-чатов.
# v3.2: ПРОГРАММА-УСТАНОВЩИК. Собирается на GitHub в GWParser_Setup.exe:
#   ставится как обычная программа, Python не нужен. Ключи Telegram - клубные,
#   вшиваются при сборке (файл _club_keys.py делает сборка из секретов GitHub).
#   Настройки, вход и память лежат в папке пользователя %APPDATA%\GWParser.
#   При первом запуске программа сама спрашивает часть света и страны
#   (заново - ярлык «Поиск контактов - выбрать страну» или запуск с  setup).
#   Как раньше - запуском  python gw_parser.py  - тоже работает.
# v3.1: ВХОД В TELEGRAM ПО QR-КОДУ - без кода из сообщения.
#   Программа показывает QR (в окне и в браузере). На телефоне: Telegram ->
#   Настройки -> Устройства -> «Подключить устройство» -> навести камеру.
#   Код из сообщения часто не приходит или «Invalid code» - теперь он не нужен.
#   QR не вышел - программа сама предложит старый способ (номер и код).
# v3.0: ВХОД КОШЕЛЬКОМ КЛУБА.
#   - при первом запуске программа откроет страницу cgift.club: нажать
#     «Войти через SafePal» и подписать (бесплатно). Пропуск - на 30 дней,
#     лежит в файле token.json рядом с программой (никому не передавать);
#   - парсер работает у тех, у кого оплачен ассистент клуба, или кому доступ
#     открыл Автор клуба. Закрыли доступ - программа останавливается;
#   - правила «ищущий или нет» теперь на сервере клуба: программа шлёт тексты
#     на проверку, сервер отвечает, к какой кнопке относится каждый.
#     Тексты на сервере не хранятся. Улучшения правил приходят сами.
# v2.4: СТРАНЫ И ПАКЕТЫ.
#   - строка countries в config.ini: искать группы только в этих странах
#     (например «Германия» или «Казахстан, Узбекистан»); пусто - вся часть света;
#   - ярлык может задать страну и направления сам:  c=DE  d=health
#       python gw_parser.py c=DE          - только Германия
#       python gw_parser.py c=KZ,UZ d=metr - Казахстан и Узбекистан, только Метр²
#     коды стран - в таблице COUNTRY_CODES ниже; направления: work, health,
#     metr, diamond или ключи кнопок (job, hc_consult, m2_house...);
#   - строка package в config.ini - имя пакета («Германия»), печатается при запуске;
#   - строже «клиенты для своего дела»: объявления «Нужны клиенты? Пишите» -
#     это реклама услуг, а не просьба о помощи.
# v2.3: шире словарь здоровья (специальности, анализы, жалобы), автопоиск
#       ищет и группы о здоровье и свадьбах, строже «клиенты для своего дела».
#
# v2.1: ЧАТЫ БЕЗ РУЧНОЙ ВОЗНИ.
#   1) АВТОПОИСК. Программа сама ищет в Telegram публичные группы по городам
#      русскоязычного мира (кроме России) - «работа Берлин», «украинцы Варшава»,
#      «мамы Тель-Авив»... - и читает их БЕЗ ВСТУПЛЕНИЯ, как предпросмотр.
#      Понемногу за запуск, с паузами - чтобы Telegram не ограничил аккаунт.
#      Группы, которые 3 раза подряд пустые, сама перестаёт читать.
#   2) ПАПКИ. Все чаты из папок Telegram, название которых начинается на GWay
#      («GWay Европа», «GWay Азия», «GWay Америка», «GWay Остальные»), читаются
#      сами - вписывать их в config.ini не нужно.
#   3) СТРАНА определяется сама по названию чата и тексту (Берлин -> Германия);
#      не узнал - ставится часть света из папки или автопоиска.
#   regions в config.ini - какие части света искать (у Автора - все, партнёру
#   можно дать только свою: например «Европа»).
#
# v2.2: ЖИВОЙ РЕЖИМ (свой «Упоминатор»):   python gw_parser.py live
#   Программа не закрывается: каждые 20 минут проверяет чаты, папки GWay и
#   лучшие группы автопоиска и СРАЗУ присылает найденных людей вам в Telegram -
#   с цитатой, ссылкой на сообщение и готовым первым сообщением. Раз в сутки
#   сама ищет новые группы. Найденные люди уходят и в копилку клуба
#   (live_to_pool = on). Остановить - закрыть окно или Ctrl+C.
#
# v2.0: ЗА ОДИН ПРОХОД - ВСЕ НАПРАВЛЕНИЯ КЛУБА. Каждое сообщение программа
# сама относит к одной кнопке «Поиска клиентов» и отправляет в её копилку:
#   GlobalWay:  job (работа), team (команда), debt (долги), tools (клиенты для дела)
#   Здоровье:   hc_consult (совет врача/специалиста), hc_wellness (здоровый образ жизни)
#   Метр²:      m2_house (жильё), m2_refugee (переселенцы), m2_nature (жить на природе),
#               m2_business (своё дело)
#   Diamond:    jewelry (ищут кольцо, бриллиант, украшение)
# У чата можно указать страну:  vakansii_Zakarpatyya | Украина  - тогда люди
# из него попадут в копилку этой страны (партнёр, выбравший Украину, их и получит).
# Какие направления собирать - строка directions в config.ini (по умолчанию все).
#
# ЧТО ДЕЛАЕТ: заходит в Telegram ПОД ТВОИМ РАБОЧИМ АККАУНТОМ (как ещё одно
# устройство), проходит по чатам из списка в config.ini, читает свежие
# сообщения, отбирает людей, которые САМИ пишут "ищу работу / подработку /
# нужен доход" и т.п., и отправляет их на склад GlobalWay (cgift.club).
# НИКОМУ НИЧЕГО НЕ ПИШЕТ И НЕ ОТПРАВЛЯЕТ В ЧАТЫ - только читает.
#
# ЗАПУСК: дважды в день или раз в день, вручную или планировщиком:
#   python gw_parser.py
# Первый запуск спросит номер телефона рабочего аккаунта и код из Telegram.
# ===========================================================================

import asyncio
import random
import configparser
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone

try:
    from telethon import TelegramClient
    from telethon.errors import FloodWaitError
    from telethon.tl import functions as tl_functions
    from telethon.tl import types as tl_types
    import requests
except ImportError:
    print('Не хватает библиотек. Выполни в командной строке:')
    print('   pip install telethon requests')
    sys.exit(1)

HERE = os.path.dirname(os.path.abspath(__file__))
# v3.2: в собранной программе (GWParser.exe) файлы программы лежат во временной
# папке сборки, а настройки, вход и память - в папке пользователя.
FROZEN = bool(getattr(sys, 'frozen', False))
APP_DIR = getattr(sys, '_MEIPASS', HERE)
if FROZEN:
    HERE = os.path.join(os.environ.get('APPDATA') or os.path.expanduser('~'), 'GWParser')
    os.makedirs(HERE, exist_ok=True)
# Направление можно передать при запуске:  python gw_parser.py team
# Тогда берётся config.team.ini и своя память прочитанного state.team.json.
# v1.5: слово  all  при запуске = перечитать заново, не глядя на память.
#   python gw_parser.py all        - работа, перечитать за неделю
#   python gw_parser.py team all   - команда, перечитать за неделю
# Память (state) при этом НЕ удаляется - просто игнорируется на один заход,
# а в конце перезаписывается. Файлы руками трогать не нужно.
ARGS = [a.strip().lower() for a in sys.argv[1:] if a.strip()]
FULL = 'all' in ARGS
LIVE = 'live' in ARGS      # v2.2: живой режим
SETUP = 'setup' in ARGS    # v3.2: заново выбрать часть света и страны
ARG = next((a for a in ARGS if a not in ('all', 'live', 'setup') and '=' not in a), '')
# v2.4: страна и направления из ярлыка:  c=DE,PL  d=health
ARG_C = next((a.split('=', 1)[1] for a in ARGS if a.startswith('c=')), '')
ARG_D = next((a.split('=', 1)[1] for a in ARGS if a.startswith('d=')), '')
VERSION = '3.2'
SUFFIX = ('.' + ARG) if ARG else ''
CONFIG = os.path.join(HERE, 'config%s.ini' % SUFFIX)
if not os.path.exists(CONFIG) and ARG:
    CONFIG = os.path.join(HERE, 'config.ini')
STATE = os.path.join(HERE, 'state%s.json' % SUFFIX)   # докуда дочитали каждый чат
STATS = os.path.join(HERE, 'stats%s.json' % SUFFIX)   # сколько людей дал каждый чат
SESSION = os.path.join(HERE, 'gw_session')            # вход в Telegram (не удалять)

# ===========================================================================
# v3.1 (11.10.2026): ВХОД В TELEGRAM ПО QR-КОДУ.
# Код из сообщения Telegram у партнёров часто не приходит, или Telegram
# отменяет его («Invalid code»), если код переслали. По QR кода нет вовсе:
# человек сканирует QR телефоном (Настройки -> Устройства -> Подключить
# устройство), и сеанс входит. QR рисуется библиотекой qrcode, которая лежит
# в папке программы (qrcode\) - ставить ничего не нужно.
# ===========================================================================
QR_FILE = os.path.join(HERE, 'vhod_qr.html')   # страница с QR, удаляется после входа
_QR_OPENED = []                                # браузер открываем один раз, дальше страница обновляется сама

def _qr_matrix(url):
    try:
        import qrcode
    except Exception:
        return None
    q = qrcode.QRCode(border=2, error_correction=qrcode.constants.ERROR_CORRECT_L)
    q.add_data(url)
    q.make(fit=True)
    return q.get_matrix()

def _qr_show(url, left_sec):
    m = _qr_matrix(url)
    if not m:
        return False
    # 1) в окне: два ряда модулей в одной строке (полублоки), светлый фон
    lines = []
    for y in range(0, len(m), 2):
        row = ''
        for x in range(len(m)):
            top = m[y][x]
            bot = m[y + 1][x] if y + 1 < len(m) else False
            row += ' ' if (top and bot) else ('\u2584' if top else ('\u2580' if bot else '\u2588'))
        lines.append('  ' + row)
    try:
        print()
        print('\n'.join(lines))
        print()
    except Exception:
        pass
    # 2) в браузере: крупно и чётко (если в окне QR не читается)
    n = len(m)
    cells = ''.join('<rect x="%d" y="%d" width="1" height="1"/>' % (x, y)
                    for y in range(n) for x in range(n) if m[y][x])
    html = ('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="5"><title>Вход в Telegram</title>'
            '<body style="font-family:Arial,sans-serif;background:#f4f6f8;text-align:center;padding:24px">'
            '<h2>Вход парсера в Telegram</h2>'
            '<svg viewBox="0 0 %d %d" width="320" height="320" style="background:#fff;padding:12px;'
            'shape-rendering:crispEdges"><g fill="#000">%s</g></svg>'
            '<p style="font-size:18px;max-width:520px;margin:16px auto">На телефоне: <b>Telegram -&gt; Настройки -&gt; '
            'Устройства -&gt; Подключить устройство</b> - и наведите камеру на этот код.</p>'
            '<p style="color:#666">Код меняется сам примерно раз в %d секунд, страница обновляется сама. '
            'Вошли - закройте эту вкладку.</p></body>') % (n, n, cells, max(10, int(left_sec)))
    try:
        with open(QR_FILE, 'w', encoding='utf-8') as f:
            f.write(html)
        if not _QR_OPENED:
            import webbrowser
            webbrowser.open('file:///' + QR_FILE.replace('\\', '/'))
            _QR_OPENED.append(1)
    except Exception:
        pass
    return True

async def _ask_cloud_password(client):
    from telethon.errors import PasswordHashInvalidError
    print('У аккаунта стоит облачный пароль Telegram (тот, что вы ставили сами в')
    print('Telegram -> Настройки -> Конфиденциальность -> Облачный пароль).')
    loop = asyncio.get_event_loop()
    for attempt in range(3):
        pwd = ''
        while not pwd:
            pwd = (await loop.run_in_executor(None, input, 'Введите облачный пароль Telegram и нажмите Enter: ')).strip()
            if not pwd:
                print('Пароль пустой - введите его ещё раз.')
        try:
            if not client.is_connected():
                await client.connect()
            await client.sign_in(password=pwd)
            return
        except PasswordHashInvalidError:
            print('Пароль неверный.' + (' Попробуйте ещё раз.' if attempt < 2 else ''))
    raise RuntimeError('облачный пароль не подошёл 3 раза')

async def tg_login(client):
    await client.connect()
    if await client.is_user_authorized():
        return
    print()
    print('ВХОД В TELEGRAM ПО QR-КОДУ (один раз).')
    print('На телефоне откройте Telegram -> Настройки -> Устройства ->')
    print('«Подключить устройство» и наведите камеру на QR-код ниже.')
    print('Если QR в окне плохо читается - он открыт и в браузере, крупно.')
    try:
        from telethon.errors import SessionPasswordNeededError
        qr = await client.qr_login()
        for _ in range(20):            # ~10 минут, QR обновляется сам
            left = 30
            try:
                left = max(10, (qr.expires - datetime.now(timezone.utc)).total_seconds())
            except Exception:
                pass
            if not _qr_show(qr.url, left):
                raise RuntimeError('нет библиотеки qrcode в папке программы')
            try:
                await qr.wait(timeout=left)
                break
            except asyncio.TimeoutError:
                print('QR обновился - наведите камеру на новый.')
                await qr.recreate()
            except SessionPasswordNeededError:
                # v3.1: пароль спрашиваем, НЕ останавливая связь с Telegram (input в отдельном
                # потоке) - иначе, пока человек печатает, Telegram рвёт соединение.
                await _ask_cloud_password(client)
                break
        else:
            raise RuntimeError('время на вход вышло')
        try:
            os.remove(QR_FILE)
        except Exception:
            pass
        if await client.is_user_authorized():
            print('Вход по QR выполнен.')
            return
    except Exception as e:
        print('Вход по QR не получился (%s).' % e)
    try:
        os.remove(QR_FILE)
    except Exception:
        pass
    print('Старый способ: номер телефона и код, который придёт в чат «Telegram».')
    await client.start()

PHONE_RE = re.compile(r'(\+?\d[\d\s\-\(\)]{8,17}\d)')
STOP_USER = re.compile(r'bot$', re.I)   # ботов в контакты не берём

# ===========================================================================
# v3.0: ПРАВИЛА ОТБОРА ЖИВУТ НА СЕРВЕРЕ КЛУБА (api/_parser-rules.js).
# Программа читает чаты и отправляет тексты на проверку; сервер отвечает, к
# какой кнопке относится каждое сообщение. Тексты на сервере не хранятся.
# Работает только после входа кошельком клуба (подпись SafePal).
# ===========================================================================
DIR_TITLES = {
    'jewelry': 'Diamond - украшения',
    'hc_consult': 'Здоровье - совет специалиста',
    'hc_wellness': 'Здоровье - образ жизни',
    'm2_refugee': 'Метр² - переселенцы',
    'm2_house': 'Метр² - жильё',
    'm2_nature': 'Метр² - жить на природе',
    'm2_business': 'Метр² - своё дело',
    'debt': 'GlobalWay - выход из долгов',
    'team': 'GlobalWay - команда',
    'tools': 'GlobalWay - клиенты для своего дела',
    'job': 'GlobalWay - работа',
}
ALL_DIRECTIONS = list(DIR_TITLES.keys())
TOKEN_FILE = os.path.join(HERE, 'token.json')   # пропуск кошелька (30 дней). Не передавать другим!
AUTH = {}                                       # {'token': ...} или {'key': ...}


class NoAccess(Exception):
    """Сервер не пускает: нет пропуска или доступ закрыт."""


def parser_url(cfg):
    s = cfg['server'].rstrip('/')
    return s[:-len('/api/assistant')] + '/api/parser' if s.endswith('/api/assistant') else s.rsplit('/api/', 1)[0] + '/api/parser'


def api(cfg, body, timeout=60):
    r = requests.post(parser_url(cfg), json=body, timeout=timeout)
    try:
        d = r.json()
    except Exception:
        d = {'error': 'сервер ответил %s' % r.status_code}
    d['_status'] = r.status_code
    return d


def login(cfg):
    """Вход кошельком клуба: страница cgift.club, подпись SafePal, пропуск на 30 дней."""
    d = api(cfg, {'action': 'start'})
    if not d.get('code'):
        print('Сервер не начал вход:', d.get('error', d.get('_status')))
        sys.exit(1)
    print('')
    print('=' * 60)
    print('  ВХОД КОШЕЛЬКОМ КЛУБА')
    print('  Код входа:  %s' % d['code'])
    print('  Откройте ссылку (браузер откроется сам):')
    print('  ' + d['url'])
    print('  Нажмите «Войти через SafePal» и подпишите. Это бесплатно.')
    print('  Нет SafePal на компьютере - откройте ссылку в браузере')
    print('  приложения SafePal на телефоне.')
    print('=' * 60)
    try:
        import webbrowser
        webbrowser.open(d['url'])
    except Exception:
        pass
    deadline = time.time() + int(d.get('minutes', 15)) * 60
    while time.time() < deadline:
        time.sleep(3)
        try:
            p = api(cfg, {'action': 'poll', 'code': d['code']}, timeout=20)
        except Exception:
            continue
        if p.get('token'):
            with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
                json.dump({'token': p['token'], 'wallet': p.get('wallet', ''), 'saved': datetime.now().strftime('%d.%m.%Y')}, f)
            print('Вход выполнен: %s (%s). Пропуск на %s дней.' % (short_wallet(p.get('wallet')), p.get('why', ''), p.get('days', 30)))
            return p['token']
        if p.get('denied'):
            print('Доступа нет: ' + (p.get('why') or ''))
            sys.exit(1)
        if p.get('expired'):
            break
    print('Вход не выполнен (код устарел). Запустите программу ещё раз.')
    sys.exit(1)


def short_wallet(w):
    w = str(w or '')
    return (w[:6] + '...' + w[-4:]) if len(w) > 12 else w


def ensure_access(cfg):
    """Перед работой: есть ли пропуск. Нет - вход кошельком."""
    if cfg['key']:                       # старый ключ PARSER_KEYS (компьютер Автора) - работает как раньше
        AUTH.clear()
        AUTH['key'] = cfg['key']
        print('Доступ: ключ парсера из config.ini')
        return
    tok = ''
    try:
        with open(TOKEN_FILE, encoding='utf-8') as f:
            tok = (json.load(f) or {}).get('token', '')
    except Exception:
        tok = ''
    if tok:
        try:
            c = api(cfg, {'action': 'check', 'token': tok}, timeout=30)
        except Exception as e:
            print('Не дозвонился до сервера клуба:', e)
            sys.exit(1)
        if c.get('ok') and int(c.get('days_left', 0)) >= 2:
            print('Кошелёк: %s · %s · пропуск ещё %s дн.' % (short_wallet(c.get('wallet')), c.get('why', ''), c.get('days_left')))
            AUTH.clear()
            AUTH['token'] = tok
            return
        if c.get('why'):
            print(c['why'])
    tok = login(cfg)
    AUTH.clear()
    AUTH['token'] = tok


def remote_classify(cfg, texts):
    """Сервер клуба решает, к какой кнопке относится каждый текст (None - ни к какой)."""
    out = []
    for i in range(0, len(texts), 400):
        part = texts[i:i + 400]
        body = {'action': 'classify', 'wanted': cfg['wanted'], 'texts': part}
        body.update(AUTH)
        d = api(cfg, body)
        if d['_status'] in (401, 403):
            raise NoAccess(d.get('error') or 'Нет доступа')
        if not isinstance(d.get('dirs'), list) or len(d['dirs']) != len(part):
            raise RuntimeError(d.get('error') or 'сервер не ответил на проверку')
        out.extend(d['dirs'])
    return out


def ok_len(text):
    return 12 <= len(text) <= 1200



# v3.2: клубные ключи Telegram (вшиты при сборке). Свои ключи в config.ini важнее.
def _club_keys():
    try:
        import _club_keys as K
        return int(K.API_ID), str(K.API_HASH).strip()
    except Exception:
        return 0, ''

# v3.2: мастер первого запуска - часть света и страны кнопками-цифрами
def setup_wizard():
    try:
        txt = open(CONFIG, encoding='utf-8').read()
    except Exception:
        return
    regs = list(GEO.keys())
    print()
    print('=' * 60)
    print('  НАСТРОЙКА: где искать людей')
    print('=' * 60)
    for i, r in enumerate(regs, 1):
        print('  %d - %s' % (i, r))
    print('  %d - весь мир' % (len(regs) + 1))
    sel = ''
    while not sel:
        a = input('Впишите цифру части света и нажмите Enter: ').strip()
        if a.isdigit() and 1 <= int(a) <= len(regs) + 1:
            sel = a
    n = int(sel)
    chosen = regs if n == len(regs) + 1 else [regs[n - 1]]
    countries = []
    if len(chosen) == 1:
        names = list(GEO[chosen[0]].keys())
        print()
        print('Страны (%s):' % chosen[0])
        for i, c in enumerate(names, 1):
            print('  %d - %s' % (i, c))
        a = input('Впишите номера стран через запятую (например 3,5) или просто Enter - вся часть света: ').strip()
        for x in re.split(r'[\s,;]+', a):
            if x.isdigit() and 1 <= int(x) <= len(names) and names[int(x) - 1] not in countries:
                countries.append(names[int(x) - 1])
    package = ', '.join(countries) if countries else ', '.join(chosen)
    def setline(t, key, val):
        if re.search(r'(?m)^%s\s*=.*$' % key, t):
            return re.sub(r'(?m)^%s\s*=.*$' % key, lambda m: '%s = %s' % (key, val), t, count=1)
        return t.rstrip() + '\n%s = %s\n' % (key, val)
    txt = setline(txt, 'regions', ', '.join(chosen))
    txt = setline(txt, 'countries', ', '.join(countries))
    txt = setline(txt, 'package', package)
    with open(CONFIG, 'w', encoding='utf-8') as f:
        f.write(txt)
    print('Сохранено: ищу - %s. Поменять потом: ярлык «Поиск контактов - выбрать страну».' % package)
    print()

def ensure_config():
    # v3.2: в установленной программе настроек ещё нет - кладём заготовку и спрашиваем страну
    if not os.path.exists(CONFIG):
        src = os.path.join(APP_DIR, 'config.ini')
        if FROZEN and os.path.exists(src):
            with open(src, encoding='utf-8') as f, open(CONFIG, 'w', encoding='utf-8') as g:
                g.write(f.read())
            setup_wizard()
            return
    if SETUP:
        setup_wizard()

def load_cfg():
    ensure_config()
    if not os.path.exists(CONFIG):
        print('Нет файла настроек: ' + os.path.basename(CONFIG))
        print('Положи его рядом с программой и заполни - там всё подписано.')
        sys.exit(1)
    cp = configparser.ConfigParser()
    cp.read(CONFIG, encoding='utf-8')
    c = cp['parser']
    # v2.0: строка чата может быть  имя | Страна  - страна чата для копилки
    chats = []
    for x in c.get('chats', '').replace('\n', ',').split(','):
        x = x.split(';')[0].strip()
        if not x:
            continue
        name, _, reg = x.partition('|')
        chats.append((name.strip(), reg.strip()))
    chats = [ch for ch in chats if ch[0]]
    raw_dirs = c.get('directions', 'all').strip().lower()
    if ARG_D:   # v2.4: направления из ярлыка  d=health
        raw_dirs = ','.join(sum((DIR_GROUPS.get(x.strip(), [x.strip()]) for x in ARG_D.split(',')), []))
    if raw_dirs in ('', 'all', 'все'):
        wanted = list(ALL_DIRECTIONS)
    else:
        wanted = [d.strip() for d in re.split(r'[\s,;]+', raw_dirs) if d.strip() in ALL_DIRECTIONS]
        if not wanted:
            print('В строке directions нет ни одного известного направления. Беру все.')
            wanted = list(ALL_DIRECTIONS)
    # v2.1: список chats может быть пустым - чаты дадут папки GWay и автопоиск
    own_id = int(re.sub(r'\D', '', c.get('api_id', '0') or '') or 0)   # v2.4: пустое поле - понятное сообщение, а не ошибка Python
    own_hash = c.get('api_hash', '').strip()
    if not own_id or not own_hash:          # v3.2: своих ключей нет - клубные из сборки
        own_id, own_hash = _club_keys()
    return {
        'api_id': own_id,
        'api_hash': own_hash,
        'server': c.get('server', 'https://cgift.club/api/assistant').strip(),
        'key': c.get('parser_key', '').strip(),
        'direction': c.get('direction', 'job').strip() or 'job',
        'region': c.get('region', '').strip(),
        'hours_back': int(c.get('hours_back', '26')),
        'max_per_chat': int(c.get('max_per_chat', '60')),
        'chats': chats,
        'wanted': wanted,
        # v2.1
        'regions': [r for r in (x.strip().capitalize() for x in re.split(r'[,;]+', c.get('regions', 'all'))) if r in GEO] or list(GEO.keys()),
        # v2.4: страны (пусто - вся часть света); ярлык c=DE важнее строки в файле
        'countries': parse_countries(ARG_C or c.get('countries', '')),
        'package': c.get('package', '').strip(),
        'auto_search': c.get('auto_search', 'on').strip().lower() in ('on', 'yes', 'да', '1', 'true'),
        'search_per_run': max(0, min(30, int(c.get('search_per_run', '15') or 15))),
        'groups_per_run': max(0, min(60, int(c.get('groups_per_run', '40') or 40))),
        'folder_prefix': c.get('folder_prefix', 'GWay').strip() or 'GWay',
        # v2.2: живой режим
        'live_minutes': max(10, min(120, int(c.get('live_minutes', '20') or 20))),
        'notify_to': c.get('notify_to', 'me').strip() or 'me',
        'live_to_pool': c.get('live_to_pool', 'on').strip().lower() in ('on', 'yes', 'да', '1', 'true'),
    }


def load_state():
    try:
        with open(STATE, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(st):
    with open(STATE, 'w', encoding='utf-8') as f:
        json.dump(st, f, ensure_ascii=False, indent=1)


def load_stats():
    try:
        with open(STATS, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_stats(st):
    with open(STATS, 'w', encoding='utf-8') as f:
        json.dump(st, f, ensure_ascii=False, indent=1)


def report_chats(stats, chats):
    """Отчёт по чатам: кто кормит, а кто только время отнимает."""
    today = datetime.now(timezone.utc).strftime('%d.%m')
    print('')
    print('--- ЧАТЫ: что дают ---')
    dead = []
    for ref, _reg in chats:
        key = ref.replace('https://t.me/', '').replace('t.me/', '').strip('/@ ')
        st = stats.get(key) or {}
        runs = int(st.get('runs', 0))
        found = int(st.get('found', 0))
        last = st.get('last_found') or '-'
        mark = ' '
        if runs >= 3 and found == 0:
            mark = '!'
            dead.append(key)
        print('%s %-28s заходов: %-3d людей: %-4d последний улов: %s'
              % (mark, key[:28], runs, found, last))
    if dead:
        print('')
        print('ПУСТЫЕ (3+ захода, ни одного человека) - можно убрать из config:')
        for d in dead:
            print('   ' + d)
    print('----------------------')
    print('Сегодня: ' + today)


def pick_contact(msg, sender):
    """Контакт: телефон из текста, иначе @username автора."""
    text = msg.message or ''
    m = PHONE_RE.search(text)
    if m:
        digits = re.sub(r'\D', '', m.group(1))
        if 9 <= len(digits) <= 15:
            return m.group(1).strip()
    if sender and getattr(sender, 'username', None) and not STOP_USER.search(sender.username):
        return '@' + sender.username
    return ''


def msg_link(chat, chat_username, msg_id):
    if chat_username:
        return f'https://t.me/{chat_username}/{msg_id}'
    return f'https://t.me/c/{chat.id}/{msg_id}'


# ===========================================================================
# v2.1: ГЕОГРАФИЯ - части света, страны, города (русскоязычные общины).
# РОССИЯ ИСКЛЮЧЕНА ПОЛНОСТЬЮ (правило клуба).
# ===========================================================================
GEO = {
    'Европа': {
        'Украина': ['Киев', 'Львов', 'Одесса', 'Днепр', 'Харьков', 'Ужгород', 'Ивано-Франковск', 'Винница', 'Запорожье'],
        'Германия': ['Берлин', 'Мюнхен', 'Гамбург', 'Франкфурт', 'Кёльн', 'Дюссельдорф', 'Штутгарт', 'Лейпциг', 'Дрезден', 'Ганновер', 'Нюрнберг'],
        'Польша': ['Варшава', 'Краков', 'Вроцлав', 'Гданьск', 'Познань', 'Лодзь'],
        'Чехия': ['Прага', 'Брно'],
        'Словакия': ['Братислава'],
        'Австрия': ['Вена'],
        'Швейцария': ['Цюрих', 'Женева'],
        'Нидерланды': ['Амстердам', 'Роттердам'],
        'Бельгия': ['Брюссель', 'Антверпен'],
        'Франция': ['Париж', 'Ницца'],
        'Испания': ['Мадрид', 'Барселона', 'Валенсия', 'Аликанте', 'Малага'],
        'Португалия': ['Лиссабон', 'Порту'],
        'Италия': ['Рим', 'Милан', 'Неаполь'],
        'Великобритания': ['Лондон'],
        'Ирландия': ['Дублин'],
        'Швеция': ['Стокгольм'],
        'Норвегия': ['Осло'],
        'Дания': ['Копенгаген'],
        'Финляндия': ['Хельсинки'],
        'Литва': ['Вильнюс'],
        'Латвия': ['Рига'],
        'Эстония': ['Таллин'],
        'Молдова': ['Кишинёв'],
        'Румыния': ['Бухарест'],
        'Болгария': ['Варна', 'София'],
        'Греция': ['Афины'],
        'Кипр': ['Лимассол', 'Пафос'],
        'Черногория': ['Будва'],
        'Сербия': ['Белград'],
        'Венгрия': ['Будапешт'],
        'Беларусь': ['Минск'],
    },
    'Азия': {
        'Казахстан': ['Алматы', 'Астана', 'Шымкент'],
        'Узбекистан': ['Ташкент'],
        'Кыргызстан': ['Бишкек'],
        'Грузия': ['Тбилиси', 'Батуми'],
        'Армения': ['Ереван'],
        'Азербайджан': ['Баку'],
        'Израиль': ['Тель-Авив', 'Хайфа', 'Ашдод', 'Иерусалим'],
        'Турция': ['Стамбул', 'Анталья', 'Алания'],
        'ОАЭ': ['Дубай'],
        'Таиланд': ['Пхукет', 'Паттайя', 'Бангкок'],
        'Вьетнам': ['Нячанг', 'Хошимин'],
        'Индонезия': ['Бали'],
    },
    'Америка': {
        'США': ['Нью-Йорк', 'Майами', 'Чикаго', 'Лос-Анджелес', 'Сан-Франциско', 'Сиэтл'],
        'Канада': ['Торонто', 'Ванкувер', 'Монреаль', 'Калгари'],
        'Мексика': ['Канкун'],
        'Аргентина': ['Буэнос-Айрес'],
    },
    'Остальные': {
        'Египет': ['Хургада'],
        'Австралия': ['Сидней', 'Мельбурн'],
        'ЮАР': ['Кейптаун'],
        'Новая Зеландия': ['Окленд'],
    },
}
# Фразы автопоиска для каждого города: люди пишут сами в таких группах.
SEARCH_TEMPLATES = ['{c} чат', 'работа {c}', 'украинцы {c}', 'русскоязычные {c}', 'барахолка {c}', 'мамы {c}',
                    # v2.3: группы, где спрашивают о здоровье и где ищут кольца
                    'врачи {c}', 'русскоязычные врачи {c}', 'здоровье {c}', 'невесты {c}', 'свадьба {c}']
# Группы, работающие на Россию, - мимо (по названию).
RU_TITLE_RE = re.compile(r'(росси|russia|москв|moscow|петербург|питер\b|спб\b|рф\b|новосибирск|екатеринбург|казань|краснодар|сочи|днр|лнр)', re.I)

CITY_TO_COUNTRY = {}
COUNTRY_TO_REGION = {}
for _reg, _countries in GEO.items():
    for _country, _cities in _countries.items():
        COUNTRY_TO_REGION[_country] = _reg
        for _c in _cities:
            CITY_TO_COUNTRY[_c.lower()] = _country
# короткие корни для узнавания страны в тексте (Германия/Германии/германский...)
COUNTRY_ROOTS = {
    'Украина': ['украин', 'україн'], 'Германия': ['герман', 'німеччин'], 'Польша': ['польш', 'польщ'],
    'Чехия': ['чехи', 'чехії'], 'Израиль': ['израил', 'ізраїл'], 'Казахстан': ['казахст'], 'Молдова': ['молдов'],
    'Грузия': ['грузи'], 'Армения': ['армени'], 'Турция': ['турци', 'туреччин'], 'Испания': ['испани', 'іспані'],
    'Италия': ['итали', 'італі'], 'Португалия': ['португал'], 'Франция': ['франци', 'франці'],
    'Великобритания': ['британи', 'англи'], 'США': ['сша', 'америк'], 'Канада': ['канад'],
    'Нидерланды': ['нидерланд', 'голланд'], 'Австрия': ['австри'], 'Литва': ['литв'], 'Латвия': ['латви'],
    'Эстония': ['эстони', 'естоні'], 'Кипр': ['кипр', 'кіпр'], 'ОАЭ': ['оаэ', 'эмират', 'дубай'],
    'Таиланд': ['таиланд', 'тайланд'], 'Вьетнам': ['вьетнам', "в'єтнам"], 'Болгария': ['болгари'],
}


# город узнаём в любом падеже: «Варшава», «Варшавы», «в Берлине» - по корню слова,
# и только с начала слова (чтобы «Рим» не находился внутри «примерно»)
_LET = 'a-zа-яёіїєґ'
CITY_RES = []
for _city, _country in CITY_TO_COUNTRY.items():
    _root = _city if len(_city) <= 4 else _city[:max(4, len(_city) - 2)]
    CITY_RES.append((re.compile('(?<![' + _LET + '])' + re.escape(_root), re.I), _country))
COUNTRY_RES = [(re.compile('(?<![' + _LET + '])' + re.escape(r), re.I), c)
               for c, roots in COUNTRY_ROOTS.items() for r in roots]


def detect_country(text):
    """Страна по названию чата или тексту: город или корень названия страны."""
    t = (text or '').lower()
    for rx, country in CITY_RES:
        if rx.search(t):
            return country
    found = []
    for rx, country in COUNTRY_RES:
        if rx.search(t) and country not in found:
            found.append(country)
    # «Українці в Німеччині», «Украинцы в Польше» - это община ЗА ГРАНИЦЕЙ
    if len(found) > 1 and 'Украина' in found:
        found.remove('Украина')
    return found[0] if found else ''


def macro_regions(cfg):
    if cfg.get('countries'):   # v2.4: части света - по выбранным странам
        return [r for r in GEO.keys() if any(COUNTRY_TO_REGION.get(ct) == r for ct in cfg['countries'])]
    want = cfg.get('regions') or list(GEO.keys())
    return [r for r in GEO.keys() if r in want]


# v2.4: коды стран для ярлыков (латиницей - Windows не путает буквы)
COUNTRY_CODES = {
    'UA': 'Украина', 'DE': 'Германия', 'PL': 'Польша', 'CZ': 'Чехия', 'SK': 'Словакия', 'AT': 'Австрия',
    'CH': 'Швейцария', 'NL': 'Нидерланды', 'BE': 'Бельгия', 'FR': 'Франция', 'ES': 'Испания', 'PT': 'Португалия',
    'IT': 'Италия', 'GB': 'Великобритания', 'IE': 'Ирландия', 'SE': 'Швеция', 'NO': 'Норвегия', 'DK': 'Дания',
    'FI': 'Финляндия', 'LT': 'Литва', 'LV': 'Латвия', 'EE': 'Эстония', 'MD': 'Молдова', 'RO': 'Румыния',
    'BG': 'Болгария', 'GR': 'Греция', 'CY': 'Кипр', 'ME': 'Черногория', 'RS': 'Сербия', 'HU': 'Венгрия',
    'BY': 'Беларусь', 'KZ': 'Казахстан', 'UZ': 'Узбекистан', 'KG': 'Кыргызстан', 'GE': 'Грузия', 'AM': 'Армения',
    'AZ': 'Азербайджан', 'IL': 'Израиль', 'TR': 'Турция', 'AE': 'ОАЭ', 'TH': 'Таиланд', 'VN': 'Вьетнам',
    'ID': 'Индонезия', 'US': 'США', 'CA': 'Канада', 'MX': 'Мексика', 'AR': 'Аргентина', 'EG': 'Египет',
    'AU': 'Австралия', 'ZA': 'ЮАР', 'NZ': 'Новая Зеландия',
}
# v2.4: группы направлений для ярлыков  d=health
DIR_GROUPS = {
    'work': ['job', 'team', 'debt', 'tools'], 'health': ['hc_consult', 'hc_wellness'],
    'metr': ['m2_house', 'm2_refugee', 'm2_nature', 'm2_business'], 'diamond': ['jewelry'],
}


def parse_countries(raw):
    out = []
    for x in re.split(r'[,;]+', str(raw or '')):
        x = x.strip()
        if not x:
            continue
        name = COUNTRY_CODES.get(x.upper(), x[:1].upper() + x[1:])
        if name in COUNTRY_TO_REGION and name not in out:
            out.append(name)
        else:
            print('  Страна «%s» не знакома программе - пропускаю. Коды: %s' % (x, ', '.join(sorted(COUNTRY_CODES))))
    return out


AUTO = os.path.join(HERE, 'autosearch%s.json' % SUFFIX)   # что найдено автопоиском


def load_auto():
    try:
        with open(AUTO, encoding='utf-8') as f:
            d = json.load(f)
            d.setdefault('queries', {})
            d.setdefault('groups', {})
            return d
    except Exception:
        return {'queries': {}, 'groups': {}}


def save_auto(d):
    with open(AUTO, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)


def next_queries(cfg, auto, n):
    """Следующие n фраз поиска: те, что не задавались 30 дней, по кругу."""
    today = datetime.now(timezone.utc)
    cands = []
    only = set(cfg.get('countries') or [])
    for reg in macro_regions(cfg):
        for country, cities in GEO[reg].items():
            if only and country not in only:   # v2.4: только выбранные страны
                continue
            for c in cities:
                for tpl in SEARCH_TEMPLATES:
                    cands.append((tpl.format(c=c), country, reg))
    random.shuffle(cands)
    fresh = []
    for q, country, reg in cands:
        last = auto['queries'].get(q)
        if last:
            try:
                if (today - datetime.fromisoformat(last)).days < 30:
                    continue
            except Exception:
                pass
        fresh.append((q, country, reg))
        if len(fresh) >= n:
            break
    return fresh


async def discover_groups(client, cfg, auto):
    """Автопоиск: ищем публичные группы (где пишут люди), запоминаем их."""
    n = cfg['search_per_run']
    if n <= 0:
        return 0
    added = 0
    for q, country, reg in next_queries(cfg, auto, n):
        try:
            res = await client(tl_functions.contacts.SearchRequest(q=q, limit=20))
        except FloodWaitError as e:
            print(f'  Поиск групп: Telegram просит паузу {e.seconds}с - поиск на сегодня закончен.')
            break
        except Exception as e:
            print(f'  Поиск «{q}»: {e}')
            continue
        auto['queries'][q] = datetime.now(timezone.utc).isoformat()
        for ch in getattr(res, 'chats', []) or []:
            # только ГРУППЫ (люди пишут сами) с открытым именем; каналы-ленты - мимо
            if not getattr(ch, 'megagroup', False) or not getattr(ch, 'username', None):
                continue
            title = getattr(ch, 'title', '') or ''
            if RU_TITLE_RE.search(title) or RU_TITLE_RE.search(ch.username):
                continue
            key = ch.username.lower()
            if key in auto['groups']:
                continue
            auto['groups'][key] = {
                'username': ch.username, 'title': title,
                'id': ch.id, 'access_hash': getattr(ch, 'access_hash', None),   # чтобы не искать имя заново (Telegram это ограничивает)
                'country': detect_country(title) or country, 'region': reg,
                'runs': 0, 'found': 0, 'empty_runs': 0, 'last_found': '', 'closed': False,
                'added': datetime.now(timezone.utc).strftime('%d.%m.%Y'), 'query': q,
            }
            added += 1
        await asyncio.sleep(random.uniform(10, 18))   # пауза между поисками - против ограничений
    return added


def auto_targets(cfg, auto):
    """Какие найденные группы читать сегодня: сначала те, что дают людей, потом новые."""
    want = set(macro_regions(cfg))
    only = set(cfg.get('countries') or [])   # v2.4
    alive = [g for g in auto['groups'].values()
             if not g.get('closed') and g.get('empty_runs', 0) < 3 and g.get('region') in want
             and (not only or g.get('country') in only)]
    alive.sort(key=lambda g: (-int(g.get('found', 0)), int(g.get('runs', 0))))
    return alive[:cfg['groups_per_run']]


async def folder_targets(client, prefix):
    """Чаты из папок Telegram, название которых начинается на prefix (GWay ...)."""
    out = []
    try:
        res = await client(tl_functions.messages.GetDialogFiltersRequest())
    except Exception as e:
        print(f'  Папки Telegram не прочитались: {e}')
        return out
    filters = getattr(res, 'filters', res) or []
    for f in filters:
        title = getattr(f, 'title', '')
        title = getattr(title, 'text', title) or ''
        if not str(title).lower().startswith(prefix.lower()):
            continue
        reg_word = str(title)[len(prefix):].strip(' -:')
        region = next((r for r in GEO if r.lower() == reg_word.lower()), reg_word)
        for peer in getattr(f, 'include_peers', []) or []:
            out.append((peer, region, str(title)))
    return out


async def harvest():
    cfg = load_cfg()
    if not cfg['api_id'] or not cfg['api_hash']:
        print('В config.ini не заполнены api_id / api_hash (с my.telegram.org).')
        sys.exit(1)
    ensure_access(cfg)   # v3.0: вход кошельком клуба (или старый ключ Автора)

    st = load_state()
    stats = load_stats()
    hours = cfg['hours_back']
    if FULL:
        # перечитываем всё за неделю, память этого захода не учитываем
        st = {}
        hours = max(hours, 168)
        print('РЕЖИМ ПЕРЕЧИТЫВАНИЯ: смотрю за последние %d ч, память не учитываю.' % hours)
        print('Тех, кого уже отправляли, склад отсеет как повторы - это нормально.')
        print()
    since = datetime.now(timezone.utc) - timedelta(hours=hours)
    client = TelegramClient(SESSION, cfg['api_id'], cfg['api_hash'])
    await tg_login(client)   # v3.1: первый раз - вход по QR-коду (или номер и код)
    me = await client.get_me()
    print(f'Вошёл как: {me.first_name or ""} @{me.username or me.id}')
    print('Программа: версия %s%s' % (VERSION, (' · Пакет: ' + cfg['package']) if cfg.get('package') else ''))   # v2.4
    print('Собираю направления: ' + ', '.join(DIR_TITLES[d] for d in cfg['wanted']))

    leads, seen_contacts = [], set()
    by_dir = {}
    # v2.1: что читаем сегодня - чаты из config.ini, папки GWay, автопоиск
    print('Части света: ' + ', '.join(macro_regions(cfg)))
    if cfg.get('countries'):
        print('Страны: ' + ', '.join(cfg['countries']))
    targets = [{'ref': r, 'region': g, 'kind': 'config'} for r, g in cfg['chats']]
    folder = await folder_targets(client, cfg['folder_prefix'])
    if folder:
        print(f'Папки {cfg["folder_prefix"]}: чатов {len(folder)}')
    for peer, region, ftitle in folder:
        targets.append({'peer': peer, 'region': region, 'kind': 'folder'})
    auto = load_auto()
    if cfg['auto_search']:
        added = await discover_groups(client, cfg, auto)
        print(f'Автопоиск: новых групп {added}, всего в списке {len(auto["groups"])}')
        save_auto(auto)
        for g in auto_targets(cfg, auto):
            t_auto = {'ref': g['username'], 'region': g.get('country') or g.get('region', ''), 'kind': 'auto', 'auto': g}
            if g.get('id') and g.get('access_hash'):
                t_auto['peer'] = tl_types.InputPeerChannel(int(g['id']), int(g['access_hash']))
            targets.append(t_auto)
    seen_chats = set()
    stopped = False
    for tg in targets:
        ref = tg.get('ref') or ''
        ref = ref.replace('https://t.me/', '').replace('t.me/', '').strip('/@ ')
        try:
            chat = await client.get_entity(tg['peer'] if 'peer' in tg else ref)
        except FloodWaitError as e:
            print(f'  Telegram просит паузу {e.seconds}с - остальные чаты доберём в следующий раз.')
            break
        except Exception as e:
            if tg['kind'] == 'auto':
                tg['auto']['closed'] = True          # группа закрыта или пропала - больше не читаем
            else:
                print(f'  [{ref or "чат из папки"}] не открылся: {e}. Рабочий аккаунт вступил в этот чат?')
            continue
        if chat.id in seen_chats:
            continue
        seen_chats.add(chat.id)
        if RU_TITLE_RE.search(getattr(chat, 'title', '') or ''):
            continue                                  # группы, работающие на Россию, - мимо
        chat_username = getattr(chat, 'username', None)
        title = getattr(chat, 'title', ref)
        ref = ref or chat_username or str(chat.id)
        # страна: из строки config / по названию чата / часть света из папки или автопоиска
        chat_region = (tg['region'] or detect_country(title)) if tg['kind'] == 'config' else (detect_country(title) or tg['region'])
        last_id = int(st.get(str(chat.id), 0))
        newest_id, got, looked = last_id, 0, 0
        try:
            batch = []   # v3.0: сначала читаем чат, потом одной пачкой - на проверку серверу
            async for msg in client.iter_messages(chat, limit=800):
                if msg.id <= last_id:
                    break
                if msg.date and msg.date < since:
                    break
                looked += 1
                newest_id = max(newest_id, msg.id)
                text = (msg.message or '').strip()
                if ok_len(text):
                    batch.append((msg, text))
            dirs = remote_classify(cfg, [t for _m, t in batch]) if batch else []
            for (msg, text), direction in zip(batch, dirs):
                # к какой кнопке относится (или ни к какой) - ответ сервера
                if not direction:
                    continue
                sender = await msg.get_sender()
                if sender and getattr(sender, 'bot', False):
                    continue
                contact = pick_contact(msg, sender)
                link = msg_link(chat, chat_username, msg.id)
                fp = contact or link
                if fp in seen_contacts:
                    continue
                seen_contacts.add(fp)
                name_bits = []
                if sender is not None:
                    fn = (getattr(sender, 'first_name', '') or '').strip()
                    if fn:
                        name_bits.append(fn)
                quote = re.sub(r'\s+', ' ', text)[:300]
                lead_region = chat_region or cfg['region']
                leads.append({
                    'direction': direction,
                    'kind': 'request',
                    'name': (', '.join(name_bits) or 'Автор сообщения') + ' - ' + quote[:60],
                    'region': lead_region or 'Telegram',
                    'source': link,
                    'contact': contact,
                    'date': msg.date.strftime('%d.%m.%Y') if msg.date else '',
                    'quote': quote,
                    'note': f'Чат: {title}',
                    'hook': '',
                    '_region': lead_region,
                })
                by_dir[direction] = by_dir.get(direction, 0) + 1
                got += 1
                if got >= cfg['max_per_chat']:
                    break
        except NoAccess as e:
            print('')
            print('СТОП: ' + str(e))
            print('Запустите программу ещё раз - она предложит войти кошельком.')
            try:
                os.remove(TOKEN_FILE)
            except Exception:
                pass
            stopped = True
            break
        except FloodWaitError as e:
            print(f'  [{title}] Telegram просит паузу {e.seconds}с - чат пропущен, доберём в следующий раз.')
        except Exception as e:
            print(f'  [{title}] ошибка чтения: {e}')
            if 'проверку' in str(e) or isinstance(e, requests.RequestException):
                continue   # сервер не ответил - этот чат перечитаем в следующий раз
        st[str(chat.id)] = newest_id
        if tg['kind'] == 'auto':
            ag = tg['auto']
            ag['runs'] = int(ag.get('runs', 0)) + 1
            ag['found'] = int(ag.get('found', 0)) + got
            ag['empty_runs'] = 0 if got else int(ag.get('empty_runs', 0)) + 1
            if got:
                ag['last_found'] = datetime.now(timezone.utc).strftime('%d.%m.%Y')
        cs = stats.setdefault(ref, {'runs': 0, 'found': 0, 'last_found': ''})
        cs['runs'] = int(cs.get('runs', 0)) + 1
        cs['found'] = int(cs.get('found', 0)) + got
        cs['title'] = title
        if got:
            cs['last_found'] = datetime.now(timezone.utc).strftime('%d.%m.%Y')
        print(f'  [{title}] просмотрено {looked}, ищущих {got}' + ('  (автопоиск)' if tg['kind'] == 'auto' else ''))
        await asyncio.sleep(random.uniform(3, 6))   # вежливая пауза между чатами

    await client.disconnect()
    save_auto(auto)
    if cfg['auto_search'] and auto['groups']:
        live = [g for g in auto['groups'].values() if not g.get('closed') and g.get('empty_runs', 0) < 3]
        good = sorted([g for g in live if g.get('found')], key=lambda g: -int(g['found']))
        print('')
        print('--- АВТОПОИСК: найдено групп %d, читаются %d, дают людей %d ---' % (len(auto['groups']), len(live), len(good)))
        for g in good[:10]:
            print('   %-30s %-14s людей: %d' % (g['title'][:30], (g.get('country') or g.get('region', ''))[:14], int(g['found'])))
        print('   Лучшие группы можно добавить в свою папку GWay - тогда они читаются каждый раз.')
    save_state(st)
    save_stats(stats)
    report_chats(stats, cfg['chats'])

    if stopped:
        return
    if not leads:
        print('Новых ищущих в этот заход нет. Это нормально - запускай ежедневно.')
        return

    send_to_pool(cfg, leads, by_dir)


def send_to_pool(cfg, leads, by_dir, quiet=False):
    """Отправка в копилку клуба: каждое направление и страна - своей пачкой."""
    if not quiet:
        print(f'Собрано {len(leads)}. По направлениям:')
        for d in ALL_DIRECTIONS:
            if by_dir.get(d):
                print('   %-38s %d' % (DIR_TITLES[d], by_dir[d]))
        print('Отправляю на склад...')
    # v2.0: каждое направление и каждая страна - отдельной пачкой, в свою копилку
    groups = {}
    for ld in leads:
        groups.setdefault((ld['direction'], ld['_region']), []).append(ld)
    total_stored = total_sieved = total_dup = 0
    for (g_dir, g_reg), g_leads in groups.items():
        clean = [{k: v for k, v in ld.items() if k not in ('direction', '_region')} for ld in g_leads]
        for i in range(0, len(clean), 40):
            batch = clean[i:i + 40]
            try:
                body = {
                    'ingest': True,
                    'direction': g_dir,
                    'region': g_reg,
                    'leads': batch,
                }
                body.update(AUTH)   # v3.0: пропуск кошелька (или старый ключ Автора)
                r = requests.post(cfg['server'], json=body, timeout=60)
                d = r.json()
                if r.status_code != 200 or d.get('error'):
                    print('  Склад отказал:', d.get('error', r.status_code))
                    continue
                if not quiet:
                    print('   %-38s %-12s новых: %s, отсеяно: %s, повторы: %s' % (
                        DIR_TITLES.get(g_dir, g_dir), (g_reg or 'без страны')[:12], d.get('stored', 0), d.get('sieved', 0), d.get('duplicates', 0)))
                total_stored += int(d.get('stored', 0))
                total_sieved += int(d.get('sieved', 0))
                total_dup += int(d.get('duplicates', 0))
            except Exception as e:
                print('  Не дозвонился до склада:', e)

    if not quiet:
        print('ГОТОВО. Новых в копилку:', total_stored,
              '| отсеяно проверкой:', total_sieved,
              '| повторы (уже были):', total_dup)
    return total_stored



# ===========================================================================
# v2.2: ЖИВОЙ РЕЖИМ - свой «Упоминатор»
# ===========================================================================
# Первое сообщение человеку - по направлению. Коротко, без цифр и обещаний:
# поздороваться и спросить, актуально ли. Дальше человек ведётся вручную.
FIRST_TOUCH = {
    'job': 'вы писали, что ищете работу',
    'team': 'вы писали, что ищете команду',
    'debt': 'вы писали про долги и кредиты',
    'tools': 'вы писали, что нужны клиенты для вашего дела',
    'hc_consult': 'вы спрашивали совета по здоровью',
    'hc_wellness': 'вы писали, что хотите заняться здоровьем',
    'm2_house': 'вы писали, что ищете жильё',
    'm2_refugee': 'вы писали, что ищете жильё и работу после переезда',
    'm2_nature': 'вы писали, что мечтаете жить на природе',
    'm2_business': 'вы писали, что хотите открыть своё дело',
    'jewelry': 'вы искали украшение',
}


def alert_text(ld, chat_title):
    name = (ld['name'].split(' - ')[0] or '').strip()
    hello = 'Здравствуйте' + (', ' + name if name and name != 'Автор сообщения' else '') + '!'
    touch = '%s Мне попалось ваше сообщение в чате «%s» - %s. Ещё актуально?' % (
        hello, chat_title[:60], FIRST_TOUCH.get(ld['direction'], 'вы писали'))
    lines = [
        '🔔 %s · %s' % (DIR_TITLES.get(ld['direction'], ld['direction']), ld['_region'] or 'страна не указана'),
        'Чат: %s' % chat_title[:80],
        '«%s»' % ld['quote'][:400],
        'Кому писать: %s' % (ld['contact'] or 'нет открытого ника - ответьте в чате по ссылке'),
        'Сообщение: %s' % ld['source'],
        '',
        'Первое сообщение (можно изменить):',
        touch,
    ]
    return '\n'.join(lines)


async def live():
    cfg = load_cfg()
    if not cfg['api_id'] or not cfg['api_hash']:
        print('В config.ini не заполнены api_id / api_hash (с my.telegram.org).')
        sys.exit(1)
    ensure_access(cfg)   # v3.0: вход кошельком клуба
    st = load_state()
    stats = load_stats()
    auto = load_auto()
    client = TelegramClient(SESSION, cfg['api_id'], cfg['api_hash'])
    await tg_login(client)   # v3.1: вход по QR-коду
    me = await client.get_me()
    print(f'Вошёл как: {me.first_name or ""} @{me.username or me.id}')
    print('Программа: версия %s%s' % (VERSION, (' · Пакет: ' + cfg['package']) if cfg.get('package') else ''))   # v2.4
    notify = cfg['notify_to']
    try:
        notify_peer = 'me' if notify.lower() in ('me', 'я', 'избранное') else await client.get_entity(notify)
    except Exception as e:
        print(f'Не нашёл, кому слать уведомления ({notify}): {e}. Шлю в «Избранное».')
        notify_peer = 'me'
    print('ЖИВОЙ РЕЖИМ: проверка каждые %d мин. Уведомления: %s. В копилку клуба: %s.' % (
        cfg['live_minutes'], 'Избранное' if notify_peer == 'me' else notify, 'да' if cfg['live_to_pool'] else 'нет'))
    print('Остановить - закрыть окно или Ctrl+C.')
    print('Собираю направления: ' + ', '.join(DIR_TITLES[d] for d in cfg['wanted']))

    entities = {}          # chat.id -> (entity, region-from-config-or-folder, kind, auto-record)
    last_refresh = None
    seen_contacts = set()
    while True:
        now = datetime.now(timezone.utc)
        # раз в 6 часов - обновить список чатов; раз в сутки - автопоиск новых групп
        if last_refresh is None or (now - last_refresh).total_seconds() > 6 * 3600:
            if last_refresh is not None:
                ensure_access(cfg)   # v3.0: пропуск проверяется заново (и продлевается входом, если кончается)
            if cfg['auto_search']:
                last_disc = auto.get('last_discovery')
                fresh = True
                if last_disc:
                    try:
                        fresh = (now - datetime.fromisoformat(last_disc)).total_seconds() > 20 * 3600
                    except Exception:
                        fresh = True
                if fresh:
                    added = await discover_groups(client, cfg, auto)
                    auto['last_discovery'] = now.isoformat()
                    print(f'Автопоиск: новых групп {added}, всего {len(auto["groups"])}')
                    save_auto(auto)
            targets = [{'ref': r, 'region': g, 'kind': 'config'} for r, g in cfg['chats']]
            for peer, region, _t in await folder_targets(client, cfg['folder_prefix']):
                targets.append({'peer': peer, 'region': region, 'kind': 'folder'})
            if cfg['auto_search']:
                for g in auto_targets(cfg, auto):
                    t_auto = {'ref': g['username'], 'region': g.get('country') or g.get('region', ''), 'kind': 'auto', 'auto': g}
                    if g.get('id') and g.get('access_hash'):
                        t_auto['peer'] = tl_types.InputPeerChannel(int(g['id']), int(g['access_hash']))
                    targets.append(t_auto)
            entities = {}
            for tg in targets:
                ref = (tg.get('ref') or '').replace('https://t.me/', '').replace('t.me/', '').strip('/@ ')
                try:
                    chat = await client.get_entity(tg['peer'] if 'peer' in tg else ref)
                except FloodWaitError as e:
                    print(f'  Telegram просит паузу {e.seconds}с - остальные чаты подключу позже.')
                    break
                except Exception:
                    if tg['kind'] == 'auto':
                        tg['auto']['closed'] = True
                    continue
                if chat.id in entities or RU_TITLE_RE.search(getattr(chat, 'title', '') or ''):
                    continue
                entities[chat.id] = (chat, tg)
                await asyncio.sleep(random.uniform(1, 2))
            last_refresh = now
            print(f'Слежу за чатами: {len(entities)}')

        # один круг проверки
        leads, by_dir, alerts = [], {}, []
        for chat_id, (chat, tg) in list(entities.items()):
            title = getattr(chat, 'title', '') or str(chat_id)
            chat_username = getattr(chat, 'username', None)
            region = (tg['region'] or detect_country(title)) if tg['kind'] == 'config' else (detect_country(title) or tg['region'])
            last_id = int(st.get(str(chat_id), 0))
            newest_id, got = last_id, 0
            since = datetime.now(timezone.utc) - timedelta(hours=cfg['hours_back'])
            try:
                batch = []   # v3.0: пачкой на проверку серверу
                async for msg in client.iter_messages(chat, limit=200):
                    if msg.id <= last_id or (msg.date and msg.date < since):
                        break
                    newest_id = max(newest_id, msg.id)
                    text = (msg.message or '').strip()
                    if ok_len(text):
                        batch.append((msg, text))
                dirs = remote_classify(cfg, [t for _m, t in batch]) if batch else []
                for (msg, text), direction in zip(batch, dirs):
                    if not direction:
                        continue
                    sender = await msg.get_sender()
                    if sender and getattr(sender, 'bot', False):
                        continue
                    contact = pick_contact(msg, sender)
                    link = msg_link(chat, chat_username, msg.id)
                    fp = contact or link
                    if fp in seen_contacts:
                        continue
                    seen_contacts.add(fp)
                    fn_ = (getattr(sender, 'first_name', '') or '').strip() if sender else ''
                    quote = re.sub(r'\s+', ' ', text)[:300]
                    ld = {
                        'direction': direction, 'kind': 'request',
                        'name': (fn_ or 'Автор сообщения') + ' - ' + quote[:60],
                        'region': region or 'Telegram', 'source': link, 'contact': contact,
                        'date': msg.date.strftime('%d.%m.%Y') if msg.date else '',
                        'quote': quote, 'note': f'Чат: {title}', 'hook': '', '_region': region,
                    }
                    leads.append(ld)
                    alerts.append(alert_text(ld, title))
                    by_dir[direction] = by_dir.get(direction, 0) + 1
                    got += 1
            except NoAccess as e:
                print('')
                print('СТОП: ' + str(e))
                try:
                    os.remove(TOKEN_FILE)
                except Exception:
                    pass
                await client.disconnect()
                return
            except FloodWaitError as e:
                print(f'  Telegram просит паузу {e.seconds}с - жду.')
                await asyncio.sleep(min(e.seconds, 900))
                continue
            except Exception as e:
                print(f'  [{title}] ошибка чтения: {e}')
                continue
            st[str(chat_id)] = newest_id
            cs = stats.setdefault(chat_username or str(chat_id), {'runs': 0, 'found': 0, 'last_found': ''})
            cs['found'] = int(cs.get('found', 0)) + got
            cs['title'] = title
            if got:
                cs['last_found'] = datetime.now(timezone.utc).strftime('%d.%m.%Y')
                if tg['kind'] == 'auto':
                    tg['auto']['found'] = int(tg['auto'].get('found', 0)) + got
                    tg['auto']['last_found'] = cs['last_found']
            await asyncio.sleep(random.uniform(2, 4))
        save_state(st)
        save_stats(stats)
        save_auto(auto)

        stamp = datetime.now().strftime('%H:%M')
        if alerts:
            # уведомления: до 5 человек в одном сообщении, чтобы не засыпать чат
            for i in range(0, len(alerts), 5):
                try:
                    await client.send_message(notify_peer, '\n\n- - -\n\n'.join(alerts[i:i + 5]), link_preview=False)
                except Exception as e:
                    print('  Уведомление не ушло:', e)
                await asyncio.sleep(2)
            stored = send_to_pool(cfg, leads, by_dir, quiet=True) if cfg['live_to_pool'] else 0
            print(f'{stamp}  найдено {len(leads)}: ' + ', '.join('%s %d' % (DIR_TITLES[d], n) for d, n in by_dir.items())
                  + (f'  | в копилку новых: {stored}' if cfg['live_to_pool'] else ''))
        else:
            print(f'{stamp}  новых ищущих нет')
        await asyncio.sleep(cfg['live_minutes'] * 60)


if __name__ == '__main__':
    try:
        asyncio.run(live() if LIVE else harvest())
    except KeyboardInterrupt:
        print('Остановлено.')
    except SystemExit:
        pass
    except Exception as e:      # v3.2: в установленной программе окно не должно молча закрыться
        print()
        print('Ошибка: %s' % e)
        print('Сфотографируйте это окно и пришлите тому, кто дал вам программу.')
    if FROZEN:
        try:
            input('\nНажмите Enter, чтобы закрыть окно.')
        except Exception:
            pass
