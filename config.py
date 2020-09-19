import os
import sys


# secret_path = os.path.join(os.path.dirname(__file__), "secrets.json")
# try:
#     with open(secret_path, "r") as file_:
#         secrets = json.load(file_)
# except FileNotFoundError as e:
#     raise FileNotFoundError(
#         "\n * Secret file:" +
#         f"\n\t{secret_path}\n   does not exist.") from e
#
# keys = ("secret", "db_pswd")
# if not secrets or not all([key in secrets for key in keys]):
#     raise ValueError(
#         "\n * Secret file:" +
#         f"\n\t{secret_path}\n   is not complete.")


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False



class ProductionConfig(Config):
    db_user = "marcdw87"
    db_pswd = "db_pswd"
    db_host = os.environ.get("PORTFOLIO_DB") or "localhost"
    db_name = "portfolio"
    SQLALCHEMY_DATABASE_URI = f"mysql://{db_user}:{db_pswd}@{db_host}/{db_user}${db_name}"
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 280
