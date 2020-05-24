import ast


def convert_json_table(data):
    ad1 = []
    ad2 = []
    for row in data:
        ad1.append(ast.literal_eval(row['ad1']))
        ad2.append(ast.literal_eval(row['ad2']))

    return ad1, ad2
