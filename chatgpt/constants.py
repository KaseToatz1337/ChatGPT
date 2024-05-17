import re

BASE_URL = "https://chatgpt.com/"
BASE_URL_REGEX = re.compile(r"https:\/\/chatgpt\.com.*")
HISTORY_REGEX = re.compile(r"https:\/\/chatgpt\.com\/c\/([a-z0-9]{8}-([a-z0-9]{4}-){3}[a-z0-9]{12}).*")
LOGIN_URL_REGEX = re.compile(r"https:\/\/chatgpt\.com\/auth\/login.*")

LOGIN_BUTTON_SELECTOR = "[data-testid=\"login-button\"]"
EMAIL_INPUT_SELECTOR = "#email-input"
CONTINUE_BUTTON_SELECTOR = ".continue-btn"
PASSWORD_INPUT_SELECTOR = "#password"
CONFIRM_LOGIN_BUTTON_SELECTOR = "[data-action-button-primary=\"true\"]"

MESSAGE_SELECTOR = "[data-message-author-role=\"assistant\"]"
MESSAGE_ID_ATTRIBUTE = "data-message-id"
PROMPT_INPUT_SELECTOR = "#prompt-textarea"
REACTION_BUTTONS_SELECTOR = ".juice\:-ml-3"