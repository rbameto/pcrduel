import asyncio
import base64
import os
import random
import sqlite3
import math
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image
from hoshino import Service, priv
from hoshino.modules.priconne import _pcr_data
from hoshino.modules.priconne import duel_chara as chara
from hoshino.typing import CQEvent
from hoshino.util import DailyNumberLimiter
import copy
import json

sv = Service('pcr-duel', enable_on_default=True)
from .CECounter import *
from .ScoreCounter import *
from .DuelCounter import *
#贵族决斗主体
from .zhuti import *
#战斗力系统调用
from .comateffectiveness import *
