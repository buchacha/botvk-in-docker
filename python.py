import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json
import datetime
import os

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
RESOURSE_DIR = os.path.join(BASE_FOLDER, 'resources')

with open('.secure_data.json') as json_file:
	token = json.load(json_file)['token']

session = requests.Session()
vk_session = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

# attachments = []
upload = VkUpload(vk_session)
# image_url = 'http://pngimg.com/uploads/hello/hello_PNG22.png'
# image = session.get(image_url, stream=True)
# attachments.append(
#	'photo{}_{}'.format(photo['owner_id'], photo['id'])

keyboard = VkKeyboard(one_time=True)

whiteBtn = 'Белая кнопка'
greenBtn = 'Зелёная кнопка'

keyboard.add_button(whiteBtn, color=VkKeyboardColor.DEFAULT)
keyboard.add_button(greenBtn, color=VkKeyboardColor.POSITIVE)

keyboard.add_line()  # Переход на вторую строку
keyboard.add_button('Еще одна кнопка')
keyboard.add_button('Время скажи')


textDict = ['Привет', 'привет', 'Hello', 'hello']
helloMessage = 'Hello! Привет!'
emptyMessage = ''
warnMessage = 'Не понял вас!!!'

for event in longpoll.listen():
	if event.type ==  VkEventType.MESSAGE_NEW and event.to_me and event.text:
		if event.text in textDict:
			if event.from_user:
				imagePath = 'images/hello.png'
				photo = upload.photo_messages(photos=imagePath)[0]
				attachment = 'photo{}_{}'.format(photo['owner_id'], photo['id'])
				vk.messages.send(
					user_id=event.user_id,
					message=helloMessage,
					attachment=attachment,
					random_id=get_random_id(),
					keyboard=keyboard.get_keyboard()
				)

		elif event.text == whiteBtn:
			imagePath = 'images/white.jpg'
			photo = upload.photo_messages(photos=imagePath)[0]
			attachment = 'photo{}_{}'.format(photo['owner_id'], photo['id'])
			vk.messages.send(
					user_id=event.user_id,
					message=emptyMessage,
					attachment=attachment,
					random_id=get_random_id(),
					keyboard=keyboard.get_keyboard()
				)

		elif event.text == greenBtn:
			imagePath = 'images/green.jpg'
			photo = upload.photo_messages(photos=imagePath)[0]
			attachment = 'photo{}_{}'.format(photo['owner_id'], photo['id'])
			vk.messages.send(
					user_id=event.user_id,
					message=emptyMessage,
					attachment=attachment,
					random_id=get_random_id(),
					keyboard=keyboard.get_keyboard()
					)
		elif event.text == 'Время скажи':
			with open(os.path.join(RESOURSE_DIR, 'response.json')) as f:
				msg = '{} - {}'.format(json.loads(f.read()).get('msg'), datetime.datetime.now().strftime('%d-%B-%Y'))
			vk.messages.send(
					user_id=event.user_id,
					message=msg,
					random_id=get_random_id(),
					keyboard=keyboard.get_keyboard()
				)
		else:
			vk.messages.send(
					user_id=event.user_id,
					message=warnMessage,
					random_id=get_random_id(),
					keyboard=keyboard.get_keyboard()
				)


