"""Create dotenv template module"""

import logging
from pathlib import Path


def build_env(env_path=".env", template_path=".env.template") -> None:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("envBuilder")
    env_file = Path(env_path)
    template_file = Path(template_path)
    logger.info("Start building .env")
    if not env_file.exists():
        logger.info(f"File {env_path} not exists...")
        logger.info("Creating...")
        env_file.write_text("", encoding="utf-8")
    else:
        logger.info(f"File {env_path} already exists...")
    lines = env_file.read_text(encoding="utf-8").splitlines()
    template_lines: list[str] = [
        "BOT_NAME=#FILLME",
        "API_ID=#FILLME",
        "API_HASH=#FILLME",
        "BOT_TOKEN=#FILLME",
    ]

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            template_lines.append(line)
        elif "=" in line:
            key = line.split("=")[0]
            template_lines.append(f"{key}=")

    template_file.write_text("\n".join(template_lines), encoding="utf-8")
    logger.info(f"dotenv template created in {template_path}")


def run():
    build_env()
