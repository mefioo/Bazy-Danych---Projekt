# import mysql.connector
# # def connection():
# #     conn = MySQLdb.connect(host="localhost",
# #                            user = "root",
# #                            passwd = "tugot",
# #                            db = "pythonprogramming")
# #     c = conn.cursor()
# #
# #     return c, conn
# def connection():
#     config = {
#         'user': 'root',
#         'password': 'root',
#         'host': 'localhost',
#         'port': '3306',
#         'database': 'xdieta',
#         'raise_on_warnings': True,
#     }
#
#     connection = mysql.connector.connect(**config)
#     cursor = connection.cursor()
#     return cursor, connection
import mysql.connector
import random
import time
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '3306',
    'database': 'xdieta',
    'raise_on_warnings': True,
}

connection = mysql.connector.connect(**config)
cursor = connection.cursor()
def clear_database():
    sql_query = "DELETE FROM wiersze_posilkow WHERE id_posilku>0"
    cursor.execute(sql_query)
    sql_query  = "DELETE FROM posilki WHERE id_posilku>0"
    cursor.execute(sql_query)
    sql_query = "DELETE FROM produkty WHERE id_produktu>0"
    cursor.execute(sql_query)
    sql_query = "ALTER TABLE produkty AUTO_INCREMENT = 1"
    cursor.execute(sql_query)
    sql_query = "ALTER TABLE posilki AUTO_INCREMENT = 1"
    cursor.execute(sql_query)
    connection.commit()
def select_all_test(database_name):
    cursor.execute("SELECT * FROM " + database_name)
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchall()
    return result, row_headers

def select_all_test_for_login(database_name, login):
    cursor.execute("SELECT * FROM " + database_name + " WHERE login = \'"+login+"\'")
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchall()
    return result, row_headers

def select_diet_view(name, surname):
    # SELECT * FROM
    # `dieta`
    # WHERE
    # dieta.Imie = 'Konrad' and dieta.Nazwisko = 'Budzyński'
    cursor.execute("SELECT * FROM dieta WHERE Imie = \'"+name+"\' AND Nazwisko = \'"+surname+"\'")
    row_headers = [x[0] for x in cursor.description]
    result = cursor.fetchall()
    return result, row_headers

def update_user_data(login, data):
    sql_query = "UPDATE uzytkownicy SET Imie = '{}', Nazwisko='{}', wiek = '{}', waga = '{}', wzrost = '{}'," \
                " plec = '{}' WHERE Login = '{}'".format(*data, login)
    try:
        cursor.execute(sql_query)
        connection.commit()
        print("success")
    except Exception as e:
        print(e)
        pass

def update_permission(login, permission):
    sql_query = "UPDATE konta SET uprawnienia = '{}' WHERE Login = '{}'".format(permission, login)
    try:
        cursor.execute(sql_query)
        connection.commit()
        print("success")
    except Exception as e:
        print(e)
        pass


def update_user_password(login, password):
    sql_query = "UPDATE konta SET haslo = '{}' WHERE Login = '{}'".format(password, login)
    try:
        cursor.execute(sql_query)
        connection.commit()
        print("success")
    except Exception as e:
        print(e)
        pass

def find_for_algorithm(login):
    cursor.execute("SELECT Imie, Nazwisko, wiek, waga, wzrost, plec FROM uzytkownicy WHERE login='{}'".format(login))
    result = cursor.fetchall()
    try:
        return result
    except Exception as e:
        print(e)
        pass

def find_activity_name(activity_id):
    cursor.execute("SELECT nazwa_aktywnosci FROM aktywnosci WHERE id_aktywnosci='{}'".format(activity_id))
    result = cursor.fetchall()
    try:
        return result[0][0]
    except Exception as e:
        print(e)
        pass

def find_activity_id(activity_name):
    cursor.execute("SELECT id_aktywnosci FROM aktywnosci WHERE nazwa_aktywnosci='{}'".format(activity_name))
    result = cursor.fetchall()
    try:
        return result[0][0]
    except Exception as e:
        print(e)
        pass

def find_user_login_by_name_and_surname(name, surname):
    cursor.execute("SELECT Login FROM uzytkownicy WHERE Imie='{}' AND Nazwisko='{}'".format(name, surname))
    result = cursor.fetchall()
    try:
        return result[0][0]
    except Exception as e:
        print(e)
        pass

def find_product_name(id):
    cursor.execute("SELECT nazwa FROM produkty WHERE id_produktu='{}'".format(id))
    result = cursor.fetchall()
    try:
        return result[0][0]
    except Exception as e:
        print(e)
        pass

def find_product_id(name):
    cursor.execute("SELECT id_produktu FROM produkty WHERE nazwa='{}'".format(name))
    result = cursor.fetchall()
    try:
        return result[0][0]
    except Exception as e:
        print(e)
        pass

def find_user_login_by_id(id):
    cursor.execute("SELECT Login FROM konta WHERE id_uzytkownika='{}'".format(id))
    result = cursor.fetchall()
    try:
        return result[0][0]
    except Exception as e:
        print(e)
        pass
def find_user_by_login(login):
    cursor.execute("SELECT * FROM uzytkownicy WHERE login='{}'".format(login))
    result = cursor.fetchall()
    try:
        return result[0]
    except Exception as e:
        print(e)
        pass

def find_accountdata_by_login(login):
    cursor.execute("SELECT * FROM konta WHERE login='{}'".format(login))
    result = cursor.fetchall()
    try:
        return result[0]
    except Exception as e:
        print(e)
        pass
def find_meal_name(id):
    cursor.execute("SELECT nazwa FROM posilki WHERE id_posilku='{}'".format(id))
    result = cursor.fetchall()
    try:
        return result[0][0]
    except Exception as e:
        print(e)
        pass

def find_account_by_login(login):
    cursor.execute("SELECT id_uzytkownika FROM konta WHERE Login='{}'".format(login))
    result = cursor.fetchall()
    try:
        return result[0][0]
    except Exception as e:
        print(e)
        pass

def find_account_by_id(id):
    cursor.execute("SELECT login FROM konta WHERE id_uzytkownika='{}'".format(id))
    result = cursor.fetchall()
    try:
        return result[0][0]
    except Exception as e:
        print(e)
        pass

def find_weekly_diet_by_login_and_day(login, day=None):
    if day == None:
        cursor.execute("SELECT id_diety FROM tygodniowe_diety WHERE Login = '{}'".format(login))
        return cursor.fetchall()
    else:
        cursor.execute("SELECT id_diety FROM tygodniowe_diety WHERE Login = '{}' AND day = {}".format(login, day))
    result = cursor.fetchall()
    try:
        return result[0][0]
    except Exception as e:
        print(e)
        pass

def find_meal_id(name):
    cursor.execute("SELECT id_posilku FROM posilki WHERE nazwa='{}'".format(name))
    result = cursor.fetchall()
    try:
        return result[0][0]
    except Exception as e:
        print(e)
        pass

def find_row_meal_by_id(id):
    cursor.execute("SELECT id_produktu FROM wiersze_posilkow WHERE id_posilku='{}'".format(id))
    result = cursor.fetchall()
    tab=[]
    for i in range(len(result)):
        tab.append(result[i][0])
    try:
        return tab
    except Exception as e:
        print(e)
        pass

def find_activity_id_and_time_per_week_by_login(login):
    cursor.execute("SELECT id_aktywnosci, Liczba_godzin_w_tygodniu FROM wiersze_aktywnosci WHERE Login='{}'".format(login))
    result = cursor.fetchall()
    try:
        return result
    except Exception as e:
        print(e)
        pass

def find_activity_name_and_time_per_week_by_login(login):
    cursor.execute("SELECT id_aktywnosci, Liczba_godzin_w_tygodniu FROM wiersze_aktywnosci WHERE Login='{}'".format(login))
    result = cursor.fetchall()
    try:
        return result
    except Exception as e:
        print(e)
        pass

def find_energy_by_id(id):
    cursor.execute("SELECT spalana_energia FROM aktywnosci WHERE id_aktywnosci='{}'".format(id))
    result = cursor.fetchall()
    try:
        return result[0][0]
    except Exception as e:
        print(e)
        pass

def calculate_burned_calories(login):
    tab = find_activity_id_and_time_per_week_by_login(login)
    sum = 0
    for i in range(len(tab)):
        sum = sum + find_energy_by_id(tab[i][0]) * tab[i][1]
    return sum


def insert_user(data):
    sql_query = "INSERT INTO uzytkownicy (Login, Imie, Nazwisko, wiek, waga, wzrost, plec) " \
                "VALUES ('{}', 'name', 'surname', '20', '60', '170', 'K')".format(data[0])
    try:
        cursor.execute(sql_query)
    except Exception as e:
        print(e)
        pass


def insert_account(data):
    if data[2] != 0 and data[2] != 1 and data[2] != 2:
        print("Wrong permission number")
        return
    sql_transcription = "INSERT INTO konta (Login, haslo, uprawnienia) VALUES ('{}', '{}', '{}')".format(data[0],
                                                                                                             data[1],
                                                                                                             data[2])
    try:
        cursor.execute(sql_transcription)
        insert_user(data)
        connection.commit()
    except Exception as e:
        print(e)
        pass


def insert_activity(data):
    sql_transcription = "INSERT INTO aktywnosci (id_aktywnosci, nazwa_aktywnosci, spalana_energia) VALUES " \
                        "(NULL, '{}', '{}')".format(data[0], data[1])
    try:
        cursor.execute(sql_transcription)
        connection.commit()
    except Exception as e:
        print(e)
        pass


# def insert_activity_row(data):
#     sql_transcription = "INSERT INTO wiersze_aktywnosci (Login, id_aktywnosci, Liczba_godzin_w_tygodniu) VALUES " \
#                        "('{}', '{}', '{}')".format(*data)
#     try:
#         cursor.execute(sql_transcription.replace('//', ''))
#         connection.commit()
#     except Exception as e:
#         print(e)
#         pass

def insert_activity_row(data):
    sql_transcription = "INSERT INTO wiersze_aktywnosci (Login, id_aktywnosci, Liczba_godzin_w_tygodniu) VALUES ('{}', '{}', '{}')".format(*data)
    try:
        cursor.execute(sql_transcription.replace('//', ''))
        connection.commit()
    except Exception as e:
        print(e)
        pass


def insert_diet(data):
    sql_query = "INSERT INTO diety (id_diety, posilek_1, posilek_2, posilek_3, posilek_4, posilek_5) " \
                "VALUES (NULL, '{}', '{}', '{}', '{}', '{}')".format(data[0], data[1], data[2], data[3], data[4])
    sql_query2 = "SELECT id_diety FROM diety WHERE posilek_1 = '{}' AND posilek_2 = '{}' AND posilek_3 = '{}' AND" \
                " posilek_4 = '{}' AND posilek_5 = '{}'".format(data[0], data[1], data[2], data[3], data[4])
    try:
        cursor.execute(sql_query)
        connection.commit()
        return cursor._insert_id
    except Exception as e:
        print(e)
        pass

def find_diet_id_by_meals(data):
    sql_query = "SELECT id_diety FROM diety WHERE posilek_1 = '{}' AND posilek_2 = '{}' AND posilek_3 = '{}' AND" \
                " posilek_4 = '{}' AND posilek_5 = '{}'".format(data[0], data[1], data[2], data[3], data[4])
    try:
        cursor.execute(sql_query)
        connection.commit()
    except Exception as e:
        print(e)
        pass


def insesrt_week_diet(data):
    sql_query = "INSERT INTO tygodniowe_diety (Login, id_diety, dzien_tygodnia) " \
                "VALUES ('{}', '{}', '{}')".format(data[0], data[1], data[2])
    try:
        cursor.execute(sql_query)
        connection.commit()
    except Exception as e:
        print(e)
        pass
    # INSERT INTO `tygodniowe_diety` (`Login`, `id_diety`, `dzien_tygodnia`) VALUES ('Logge', '5', '3');


def insert_meal_row(meal_id, product_name, amount):
    product_id = find_product_id(product_name)
    sql_query = "INSERT INTO wiersze_posilkow (id_posilku, id_produktu, waga_w_gramach) " \
                "VALUES ('{}', '{}', '{}')".format(meal_id, product_id, amount)
    try:
        cursor.execute(sql_query)
        connection.commit()
    except:
        pass
    # INSERT INTO `wiersze_posilkow` (`id_posilku`, `id_produktu`, `waga_w_gramach`) VALUES ('3', '7', '200');


def insert_product(data, meal_id=0):
    try:
        insert_meal_row(meal_id, data[0], data[4])
    except:
        pass
    sql_query = "INSERT INTO produkty (id_produktu, nazwa, bialko_w_100g, tluszcze_w_100g, wegle_w_100g) " \
                "VALUES (NULL, '{}', '{}', '{}', '{}')".format(data[0], data[1], data[2], data[3])
    try:
        cursor.execute(sql_query)
        connection.commit()
    except Exception as e:
        print(e)

    # INSERT INTO `produkty` (`id_produktu`, `nazwa`, `typ`, `bialko_w_100g`, `tluszcze_w_100g`, `wegle_w_100g`) VALUES (NULL, 'Lulz', 'Removeable', '0', '10', '0');

def insert_meal(meal_name, products):
    sql_query = "INSERT INTO posilki (id_posilku, nazwa) VALUES (NULL, '{}')".format(meal_name)
    try:
        meal_id = find_meal_id(meal_name)
        for product in products:
            insert_product(product, meal_id)
    except Exception as e:
        print(e)
        pass
    try:
        cursor.execute(sql_query)
        connection.commit()
        meal_id = find_meal_id(meal_name)
        for product in products:
            insert_product(product, meal_id)
    except Exception as e:
        print(e)
        pass

    # INSERT INTO `posilki` (`id_posilku`, `nazwa`) VALUES (NULL, 'ciasteki');


def edit_user(login, data):
    sql_query = "UPDATE uzytkownicy SET Imie = '{}', Nazwisko = '{}', wiek = '{}', waga = '{}', wzrost = '{}'," \
                " plec ={} WHERE Login = '{}'".format(data[0], data[1], data[2], data[3], data[4], data[5], login)
    try:
        cursor.execute(sql_query)
        connection.commit()
    except Exception as e:
        print(e)
        pass


def delete_user(login):
    sql_query = "DELETE FROM uzytkownicy WHERE Login = '{}'".format(login)
    try:
        delete_activities_row(login)
        delete_week_diet_by_login(login)
        cursor.execute(sql_query)
        connection.commit()
    except Exception as e:
        print(e)
        pass


def delete_activities_row(login, activity_id=None):
    if activity_id == None:
        sql_query = "DELETE FROM wiersze_aktywnosci WHERE Login = '{}'".format(login)
    else:
        sql_query = "DELETE FROM wiersze_aktywnosci WHERE Login = '{}' AND id_aktywnosci = {}".format(login,
                                                                                                      activity_id)
    try:
        cursor.execute(sql_query)
        connection.commit()
    except Exception as e:
        print(e)
        pass


def delete_week_diet_by_login(login):
    sql_query = "DELETE FROM tygodniowe_diety WHERE Login = '{}'".format(login)
    try:
        cursor.execute(sql_query)
        connection.commit()
    except Exception as e:
        print(e)
        pass


def delete_account(id):
    try:
        user_login = find_user_login_by_id(id)
        delete_user(user_login)
    except Exception as e:
        print(e)
        pass
    sql_query = "DELETE FROM konta WHERE id_uzytkownika = '{}'".format(id)
    try:
        cursor.execute(sql_query)
        connection.commit()
    except Exception as e:
        print(e)
        pass

def delete_meal_row(meal_id, product_id=None):
    if product_id == None:
        sql_query = "DELETE FROM wiersze_posilkow WHERE id_posilku = '{}'".format(meal_id)
    else:
        sql_query = "DELETE FROM wiersze_posilkow WHERE id_posilku = '{}' AND id_produktu = {}".format(meal_id,
                                                                                                      product_id)
    try:
        cursor.execute(sql_query)
        connection.commit()
    except Exception as e:
        print(e)
        pass


def delete_unused_meal(id):
    sql_query = "DELETE FROM posilki WHERE id_posilku = '{}'".format(id)
    try:
        delete_meal_row(id)
        cursor.execute(sql_query)
        connection.commit()
    except Exception as e:
        print(e)
        pass

    #"DELETE FROM `wiersze_posilkow` WHERE `wiersze_posilkow`.`id_posilku` = 10 AND `wiersze_posilkow`.`id_produktu` = 20"

# # insert_account(('diver', 'xd', 4))
# # find_product_id('PythonProduct')
# ## OGÓLNIE JAK TO DZIAŁA ( dodawanie posiłku )
# ## Dodajecie meal name ( potrzebny do nazwy posiłku w tabeli posiłków w fukncji insert_meal)
# ## Następnie dodajecie produkty. A produkty to tuplety składające się z: nazwy produktu, typu, białka, tłuszczy, węgli,
# ## oraz ilości danego produkty w posiłku. Jak korzystacie z insert_product, to nie uzupełniacie meal_name i się nie martwicie.
# ## Reszte chyba sami wykminicie.
# # insert_product(('PythonProduct', 'Sweets', 10, 12, 14, 100), 1)
#
#
# # insert_product(('GreatProduct', 'Victory', 20, 30, 40, 50))
# products = [('PythonProduct', 'Sweets', 10, 12, 14, 300), ('PythonTest', 'Spice', 13, 17, 19, 100),
#             (('MojproduktPosilkowy', 'Typposilku', 13, 17, 19, 160))]
# # insert_meal('Nowy_posilek', products)
# # print(find_product_id('PythonProduct'))
#
# # delete_unused_meal(10)

def find_wfc_by_id(id):
    cursor.execute(
        "SELECT bialko_w_100g, tluszcze_w_100g, wegle_w_100g FROM produkty WHERE id_produktu='{}'".format(id))
    result = cursor.fetchall()
    try:
        return result
    except Exception as e:
        print(e)
        pass

def return_calories_from_ingredients(data):
    return data[0][0]*4 + data[0][1]*9 + data[0][2]*4

def count_calories_in_product_by_productid(id):
    makros = find_wfc_by_id(id)
    return return_calories_from_ingredients(makros)

def count_calories_in_meal_by_mealid(id):
    ingredients = find_row_meal_by_id(id)
    sum = 0
    for ingredient in ingredients:
        sum = sum + count_calories_in_product_by_productid(ingredient)
    return sum



def return_wfc_from_meal(id):
    ingredients = find_row_meal_by_id(id)
    w = f = c = 0
    arr = []
    for ingredient in ingredients:
        data = find_wfc_by_id(ingredient)
        w = w + data[0][0]
        f = f + data[0][1]
        c = c + data[0][2]
    arr.append(w, f, c)
    return arr

def set_diet(login):
    personal_data = find_for_algorithm(login)
    #Weekly energy
    activities = find_activity_id_and_time_per_week_by_login(login)
    calories = 0
    for activity, hours in activities:
        calories = calories + int(find_energy_by_id(activity) * hours)

    #Regular energy
    sex_factor = -161 if personal_data[0][5] == 'K' else 5
    daily_energy = 9.99*personal_data[0][3] + 6.25*personal_data[0][4] - 4.92*personal_data[0][2] + sex_factor
    whole_daily_energy = daily_energy + calories/7
    energy_per_meal = whole_daily_energy/5

    #Meals
    meals_ids = []
    factors = []
    for i in range(5):
        meals_ids.append(random.randint(2, 973)) #chooses random index in range of our meals in database
        meal_calories = count_calories_in_meal_by_mealid(meals_ids[i])
        factors.append(energy_per_meal/meal_calories) #adds factors which tells about how much products should be added
                                                      #to meal

    insert_diet(meals_ids)
    # for i in meals_ids:
    #     print(find_meal_name(i), " ")
    return meals_ids


if __name__ == '__main__':
    # update_user_data('Janek', ("Jan", "Nowak", 25, 75, 170, "M"))
    all_lines = []
    products = []
    my_number = 0
    meal_name = '"Makaron" z cukinii'
    clear_database()

    file = open("pierwszaobrobka.txt.", encoding='utf8')
    # for line in file:
    #     if(line=="content_copy\n"):
    #         print(line)
    #     else:
    #         print(line)
    for line in file:
        all_lines.append(line)
        print(line)
        if (line == "content_copy\n"):
            print(reminder)
            insert_meal(meal_name, products)
            meal_name = all_lines[my_number - 1]
            products = []
        words = line.split('\t')
        for word, number in zip(words, range(len(words))):
            word = word.split(' ')
            if len(word)>1:
                print(word[0], word[1])
                if word[1] == "g":
                    try:
                        amount = float(word[0].replace(',', '.'))
                        products.append((words[0], float(words[number + 3].replace(',', '.'))/amount*100,
                                         float(words[number + 4].replace(',', '.'))/amount*100,
                                         float(words[number + 5].replace(',', '.'))/amount*100,
                                         amount))
                    except:
                        pass
        reminder = line
        my_number+=1
        # print(len(line))
    print('done')
    #
    # products = [('PythonProduct', 'Sweets', 10, 12, 14, 300), ('PythonTest', 'Spice', 13, 17, 19, 100),
    #             (('MojproduktPosilkowy', 'Typposilku', 13, 17, 19, 160))]
    #
    #
    # ## testy na prawa dostępu
    # ## usuniecie z kluczem obcym/
    # ## Jak stworzono tabele, widoki, indeksy, prawa dostępu,
    # ## dopisać, że poziomy dostępu zrealizowane będą w aplikacji, a baza połączona beędzie z rootem.
    # ##
    #
    #
    # ###################TESTY###################
    #
    # #Wyszukiwanie w krotkiej tabeli 7 rekordow
    # # start = timeit.timeit()
    # # find_user_login_by_name_and_surname("Jans", "Kowalski")
    # # end = timeit.timeit()
    # # print(end - start)
    #
    # #Wyszukiwanie w krotkiej tabeli 70 rekordow
    # # start = timeit.timeit()
    # # find_meal_name('142')
    # # end = timeit.timeit()
    # # print(end - start)
    #
    #
    #
    # #Unique
    # #insert_account(("Test","password",1))
    #
    # #String zamiast inta
    # #insert_activity(('trucht','string'))
    #
    # #Za dlugie dane
    # #insert_account(("loginloginloginloginloginlogin",'passwd',1))
    #
    # #NULL
    # #insert_diet((None, 1, 1, 1, 1))
    #
    # #Wyszukiwanie w dlugiej tabeli 587 rekordow
    # # start = timeit.timeit()
    # # find_meal_name('593')
    # # end = timeit.timeit()
    # # print(end - start)
