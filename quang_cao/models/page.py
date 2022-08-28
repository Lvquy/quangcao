import time
import datetime
import pandas as pd
from ecommercetools import seo


df = seo.get_serps("quang cao mtk", pages=5)

print(df.head(15))