import socket
import multiprocessing
import time
import sqlite3

def getServerInfo(hostId, duration): # Функция для пуолчения результата от запроса к серверу. Первое значение - начало отсчета. Второе значение - длительность отсчпета
    active = "Активен"
    conn = sqlite3.connect(f'nordvpnTests_join{hostId}.db') # Создание временной БД для возможности реализации многопоточности
    req = conn.cursor()

    req.execute(f"""CREATE TABLE IF NOT EXISTS caServers{hostId}( 
    serverId INT PRIMARY KEY, 
    serverIp TEXT, 
    serverName TEXT, 
    serverStatus TEXT); 
    """)

    for i in range (duration): # Прогон от hostId до duration всех серверов
        siteName = 'ca' + str(i + hostId + 1) + '.nordvpn.com' # "Впихивание" сайта в отдельную переменную
        try:
            ips = socket.gethostbyname(siteName)
        except socket.gaierror:
            ips = []
        if ips != []:
            active = "Активен"
        else:
            active = "Не активен"
        
        req.execute(f"""INSERT INTO caServers{hostId}(serverId, serverIp, serverName, serverStatus) VALUES({i}, '{ips}', '{siteName}', '{active}'); 
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

    timer = time.time()

    req = conn.cursor()
    servertestNumber = 10000 # Количество прогонов в одном потоке
    multiprocNumber = 20 # Количество потоков

    mpDuration = servertestNumber // multiprocNumber # Вычисление, сколько серверов обработает один поток
    stream = [0] * multiprocNumber
    for i in range(multiprocNumber):
        stream[i] = multiprocessing.Process(target=getServerInfo, args=(1 + mpDuration * i, mpDuration,))
        stream[i].start()

    for i in range(multiprocNumber):
        stream[i].join()

    for i in range (multiprocNumber): # Объединение временных БД в одну итоговуювуукава
        req.execute(f"""ATTACH 'nordvpnTests_join{1 + mpDuration * i}.db' as db;""")
        req.execute(f"INSERT INTO caServers (serverId, serverIp, serverName, serverStatus) SELECT serverId + {1 + mpDuration * i}, serverIp, serverName, serverStatus FROM caServers{1 + mpDuration * i};")
        conn.commit()
        req.execute(f"""DETACH db;""")


    print("--- %s секунд ---" % (time.time() - timer)) # Проверка быстродействия программы
