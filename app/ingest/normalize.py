import re

def normalize(txt: str) -> str:
    txt = txt.replace("\u00a0", " ")
    txt = re.sub(r"[\r\t]", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt
