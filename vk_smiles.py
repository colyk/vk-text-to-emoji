import time
import json
import vk_api
import pymorphy2

Login, Password = 'PUT_LOGIN', 'PUT_PASSWORD'
values = {'out': 0, 'count': 100, 'time_offset': 60}
signs = ['.', ',', '!', '?', '(', ')', ';', ':', '"']

morph = pymorphy2.MorphAnalyzer()
vk = vk_api.VkApi(Login, Password)

try:
    vk.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)
    exit()


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message})


def get_key(dic, key):
    for i, j in dic.items():
        if key in j.split():
            return i
    return -1

with open('json_out.txt', 'r', encoding='utf-8-sig') as file:
    data = json.load(file)


while True:
    response = vk.method('messages.get', values)
    vk.method('account.setOnline')  # 'account.setOffline'

    # if someone sent message to bot
    if response['items']:
        user_text = ''
        result = []

        values['last_message_id'] = response['items'][0]['id']
        raw_text = response['items'][0]['body']
        # print('User text: ', raw_text)

        for letter in raw_text:
            if(letter in signs):
                user_text += ' '
            user_text += letter

        for word in user_text.split():
            p = morph.parse(word)[0]
            norm_form = p.normal_form
            if(get_key(data, norm_form.lower()) != -1):
                result.append(get_key(data, norm_form.lower()))
            elif(word.isdigit()):
                for i in word:
                    result.append(get_key(data, i))
            elif(get_key(data, word.lower()) != -1):
                result.append(get_key(data, word.lower()))
            else:
                result.append(word)
        answer_text = ' '.join(result)

        write_msg(response['items'][0][u'user_id'], answer_text)
    time.sleep(1)
