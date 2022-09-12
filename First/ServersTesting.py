import socket
import multiprocessing
import time
import sqlite3

def getInfo(host, duration): # Функция для пуолчения результата от запроса к серверу. Первое значение - начало отсчета. Второе значение - длительность отсчпета
    active = "Активен"
    conn = sqlite3.connect(f'nordvpnTests_join{host}.db') # Создание временной БД для возможности реализации многопоточности
    req = conn.cursor()

    req.execute(f"""CREATE TABLE IF NOT EXISTS caServers{host}( 
    serverId INT PRIMARY KEY, 
    serverIp TEXT, 
    serverName TEXT, 
    serverStatus TEXT); 
    """)

    for i in range (duration): # Прогон от host до duration всех серверов
        siteName = 'ca' + str(i + host + 1) + '.nordvpn.com' # "Впихивание" сайта в отдельную переменную
        try:
            ips = socket.gethostbyname(siteName)
        except socket.gaierror:
            ips = []
        if ips != []:
            active = "Активен"
        else:
            active = "Не активен"
        
        req.execute(f"""INSERT INTO caServers{host}(serverId, serverIp, serverName, serverStatus) VALUES({i}, '{ips}', '{siteName}', '{active}'); 
            """) # Ввод данных в таблицу. Счетчик - i. ips - результат поиска. active - вычисляется по наличию ips выше
    conn.commit()

if __name__ == '__main__':

    conn = sqlite3.connect(f'nordvpnTests.db') # Создание итоговой БД
    req = conn.cursor()
    req.execute(f"""CREATE TABLE IF NOT EXISTS caServers( 
    serverId INT PRIMARY KEY, 
    serverIp TEXT, 
    serverName TEXT, 
    serverStatus TEXT); 
    """)

    req = conn.cursor()

    timer = time.time()

    duration = 2500 # Количество прогонов в одном потоке

    # Потоки
    p1 = multiprocessing.Process(target=getInfo, args=(1, duration,))
    p1.start()

    p2 = multiprocessing.Process(target=getInfo, args=(2501, duration,))
    p2.start()

    p3 = multiprocessing.Process(target=getInfo, args=(5001, duration,))
    p3.start()

    p4 = multiprocessing.Process(target=getInfo, args=(7501, duration,))
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    for i in range (4): # Объединение временных БД в одну итоговуювуукава
        req.execute(f"""ATTACH 'nordvpnTests_join{1 + 2500 * i}.db' as db;""")
        req.execute(f"INSERT INTO caServers (serverId, serverIp, serverName, serverStatus) SELECT serverId + {1 + 2500 * i}, serverIp, serverName, serverStatus FROM caServers{1 + 2500 * i};")
        conn.commit()
        req.execute(f"""DETACH db;""")


    print("--- %s секунд ---" % (time.time() - timer)) # Проверка быстродействия программы
