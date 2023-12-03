import requests

from gym_bot_project.functions import get_user_role


class GPTRequest:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key

    def send_gpt_request(self, message, bot):
        user_id = message.from_user.id
        if get_user_role(user_id) == "Тренер":
            bot.send_message(user_id, "Введите ваш запрос для GPT:")
            bot.register_next_step_handler(message, self.process_gpt_request, bot)
        else:
            bot.send_message(user_id, "Эта опция доступна только тренерам.")

    def process_gpt_request(self, message, bot):
        user_id = message.from_user.id
        request = message.text

        url = "https://api.openai.com/v1/engines/text-davinci-003/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.openai_api_key}',
        }
        data = {
            'prompt': request,
            'max_tokens': 400
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            choices = response.json()['choices'][0]["text"].strip("\n \t")

            bot.send_message(user_id, f"Ответ от OpenAI GPT-3.5:\n{choices}")

        except requests.exceptions.RequestException as e:
            bot.send_message(user_id, f"Ошибка при запросе к OpenAI GPT-3.5: {str(e)}")
