import requests
from .user_roles import get_user_role
deepai_api_key = '7ec4f233-4340-4975-b3c8-bcd00df7fe9d'


class GPTRequest:
    def send_gpt_request(self, message, bot):
        user_id = message.from_user.id
        if get_user_role(user_id) == "Тренер":
            bot.send_message(user_id, "Введите ваш запрос для GPT:")
            bot.register_next_step_handler(message, self.process_gpt_request, bot)
        else:
            bot.send_message(user_id, "Эта опция доступна только тренерам.")

    @staticmethod
    def process_gpt_request(message, bot):
        user_id = message.from_user.id
        request = message.text

        response = requests.post(
            "https://api.deepai.org/api/text-generator",
            data={'text': request},
            headers={'api-key': deepai_api_key}
        )

        if response.status_code == 200:
            generated_text = response.json()['output']
            bot.send_message(user_id, f"Аналог упражнения, созданный deepai.org: {generated_text}")
        else:
            bot.send_message(user_id, f"Ошибка при запросе к deepai.org: {response.text}")
