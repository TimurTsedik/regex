import re


# читаем адресную книгу в формате CSV в список contacts_list
import csv

with (open("phonebook_raw.csv", encoding="utf-8") as f):
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    # pprint(contacts_list)

    # TODO 1: выполните пункты 1-3 ДЗ
    # ваш код
    pattern = r"(\+7|8)*\s*\(*(\d\d\d)\)*[\s-]*(\d{3})[\s-]*(\d\d)[\s-]*(\d\d)\s*\(*(доб\.)*\)*\s*(\d\d\d\d)*\)*"
    subst_pattern = r"+7(\2)\3-\4-\5 \6\7"
    contact_dict = {}
    new_contacts_list = []
    name_occured = False
    for _i, contact in enumerate(contacts_list):
        if _i == 0:
            contact_dict.setdefault("last_name", contact[0])
            contact_dict.setdefault("middle_name", contact[1])
            contact_dict.setdefault("last_name", contact[2])
            contact_dict.setdefault("organization", contact[3])
            contact_dict.setdefault("position", contact[4])
            contact_dict.setdefault("phone", contact[5])
            contact_dict.setdefault("email", contact[6])
            new_contacts_list.append(contact_dict)
            contact_dict = {}
            continue
        if len(contact[0].split(' ')) == 1:
            if not any(contact[0].split(' ')[0] in d.values() for d in new_contacts_list):
                contact_dict.setdefault("last_name", contact[0].split(' ')[0])
                if len(contact[1].split(' ')) == 1:
                    contact_dict.setdefault("middle_name", contact[1].split(' ')[0])
                else:
                    contact_dict.setdefault("name", contact[1].split(' ')[0])
                    contact_dict.setdefault("middle_name", contact[1].split(' ')[1])
            else:
                name_occured = True
        elif len(contact[0].split(' ')) == 2:
            if not any(contact[0].split(' ')[0] in d.values() for d in new_contacts_list) and not any(contact[0].split(' ')[1] in d.values() for d in new_contacts_list):
                contact_dict.setdefault("last_name", contact[0].split(' ')[0])
                contact_dict.setdefault("name", contact[0].split(' ')[1])
                contact_dict.setdefault("middle_name", contact[2])
            else:
                name_occured = True
        elif len(contact[0].split(' ')) == 3:
            if not any(contact[0].split(' ')[0] in d.values() for d in new_contacts_list) and not any(contact[0].split(' ')[1] in d.values() for d in new_contacts_list):
                contact_dict.setdefault("last_name", contact[0].split(' ')[0])
                contact_dict.setdefault("middle_name", contact[0].split(' ')[1])
                contact_dict.setdefault("name", contact[0].split(' ')[2])
            else:
                name_occured = True
        if not name_occured:
            contact_dict.setdefault("organization", contact[3])
            contact_dict.setdefault("position", contact[4])
            contact_dict.setdefault("phone", re.sub(pattern, subst_pattern, contact[5]))
            contact_dict.setdefault("email", contact[6])
        else:
            for entered_contact in new_contacts_list:
                if entered_contact["last_name"] == contact[0].split(' ')[0]:
                    if entered_contact["organization"] == '':
                        entered_contact["organization"] = contact[3]
                    if entered_contact["position"] == '':
                        entered_contact["position"] = contact[4]
                    if entered_contact["phone"] == '':
                        entered_contact["phone"] = re.sub(pattern, subst_pattern, contact[5])
                    if entered_contact["email"] == '':
                        entered_contact["email"] = contact[6]
                    break
        if not name_occured:
            new_contacts_list.append(contact_dict)
        else:
            name_occured = False
        contact_dict = {}

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    for row in new_contacts_list:
        datawriter.writerow(row.values())
