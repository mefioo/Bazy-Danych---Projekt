import datetime

def get_data(table_name):
    data = [{
      "username": str(datetime.datetime.now()),
      "email": "10",
      "tracking": "122",
      "uid": "An extended Bootstrap table"
    },
     {
      "name": "multiple-select",
      "commits": "288",
      "attention": "20",
      "uneven": "A jQuery plugin"
    }, {
      "name": "Testing",
      "commits": "340",
      "attention": "20",
      "uneven": "For test"
    }]

    # c, conn = connection()
    #
    # query = ("SELECT * FROM  %s;"  %table_name)
    #
    # with conn.cursor(MySQLdb.cursors.DictCursor) as cursor:
    #     cursor.execute(query)
    #     row_headers = [x[0] for x in cursor.description]
    #     data = cursor.fetchall()
    #
    #     data = list(data)

    user_columns = [
        {
            "field": "email",  # which is the field's name of data key
            "title": "email",  # display as the table header's name
            "sortable": True,
        },
        {
            "field": "username",
            "title": "username",
            "sortable": True,
        },
        {
            "field": "tracking",
            "title": "tracking",
            "sortable": True,
        },
        {
            "field": "uid",
            "title": "uid",
            "sortable": True,
        }
    ]


    cars_columns = [
    {
        "field": "plate",  # which is the field's name of data key
        "title": "Plate",  # display as the table header's name
        "sortable": True,
    },
    {
        "field": "owner",
        "title": "Owner",
        "sortable": True,
    },
    {
        "field": "permission",
        "title": "Permission",
        "sortable": True,
    },
    {
        "field": "arrival_time",
        "title": "Arrival_time",
        "sortable": True,
    }
    ]

    # if table_name == "users":
    #     columns = user_columns
    # else:
    #     columns = cars_columns


    return data, user_columns


def get_columns():
    columns = [
        {
            "field": "name",  # which is the field's name of data key
            "title": "name",  # display as the table header's name
            "sortable": True,
        },
        {
            "field": "commits",
            "title": "commits",
            "sortable": True,
        },
        {
            "field": "attention",
            "title": "attention",
            "sortable": True,
        },
        {
            "field": "uneven",
            "title": "uneven",
            "sortable": True,
        }
    ]

    columns = [
        {
            "field": "email",  # which is the field's name of data key
            "title": "email",  # display as the table header's name
            "sortable": True,
        },
        {
            "field": "username",
            "title": "username",
            "sortable": True,
        },
        {
            "field": "tracking",
            "title": "tracking",
            "sortable": True,
        },
        {
            "field": "uid",
            "title": "uid",
            "sortable": True,
        }
    ]

    return columns

def get_columns2():
    columns = [
        {
            "field": "plate",  # which is the field's name of data key
            "title": "Plate",  # display as the table header's name
            "sortable": True,
        },
        {
            "field": "owner",
            "title": "Owner",
            "sortable": True,
        },
        {
            "field": "permission",
            "title": "Permission",
            "sortable": True,
        },
        {
            "field": "arrival_time",
            "title": "Arrival_time",
            "sortable": True,
        }
    ]
    return columns


def prepare_correct_format(data, row_columns):
    for record, rec_numb in zip(data, range(len(data))):
        new_record = {}
        for i in range(len(row_columns)):
            new_record[row_columns[i]] = record[i]
        data[rec_numb] = new_record

    for i in range(len(row_columns)):
        row_columns[i] = {"field": row_columns[i], "title": row_columns[i], "sortable": True}
    #data = [data, row_columns]
    return data, row_columns

def prepare_correct_format_rows(data, data2, data3):
    for record, rec_numb in zip(data, range(len(data))):
        new_record = {}
        try:
            new_record['Nazwa_posilku'] = data2[record[0]]
            new_record['Nazwa_produktu'] = data3[record[1]]
            new_record['Ilosc_w_gramach'] = record[2]
            data[rec_numb] = new_record
        except Exception as e:
            print(e)
        # data[rec_numb][]
    # for i in range(len(row_columns)):
    #     row_columns[i] = {"field": row_columns[i], "title": row_columns[i], "sortable": True}
    row_columns = []
    row_columns.append({"field": "Nazwa_posilku", "title": "Nazwa_posilku", "sortable": True})
    row_columns.append({"field": "Nazwa_produktu", "title": "Nazwa_produktu", "sortable": True})
    row_columns.append({"field": "Ilosc_w_gramach", "title": "Ilosc_w_gramach", "sortable": True})
    #data = [data, row_columns]
    return data, row_columns

def make_dict_from_tuple_lists(data):
    my_dict = {}
    for i in range(len(data)):
        key = data[i][0]
        my_dict[key] = data[i][1]
    return my_dict