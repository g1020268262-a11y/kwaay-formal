import zipfile
from pathlib import Path
from PIL import Image
from lxml import etree
OUT=Path(__file__).resolve().parent.parent
QA=OUT/'qa/figure-title-display';QA.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(OUT/'K-Waay-AROCMAG-submission-working.docx') as z:
    for n in (1,2,3):
        name=f'word/media/kwaay-confirmed-figure{n}.png'
        target=QA/f'original-embedded-figure{n}.png'
        target.write_bytes(z.read(name))
        with Image.open(target) as im:print(n,im.size,str(target))
