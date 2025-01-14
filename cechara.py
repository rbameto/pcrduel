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
from hoshino.config import NICKNAME
import copy
import json
from . import sv

@sv.on_prefix(['女友信息'])
async def my_fashion_info(bot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    gid = ev.group_id
    uid = ev.user_id
    if not args:
        await bot.send(ev, '请输入我的女友+pcr角色名。', at_sender=True)
        return
    name = args[0]
    cid = chara.name2id(name)
    if cid == 1000:
        await bot.send(ev, '请输入正确的pcr角色名。', at_sender=True)
        return
    duel = DuelCounter()
    score_counter = ScoreCounter2()
    c = chara.fromid(cid)
    nvmes = get_nv_icon(cid)
    lh_msg = ''
    fashioninfo = get_fashion(cid)
    up_icon=''
    up_info = duel._get_fashionup(gid,uid,cid,0)
    jishu=0
    up_name=''
    if fashioninfo:
        for fashion in fashioninfo:
            buy_info = duel._get_fashionbuy(gid,uid,cid,fashion['fid'])
            if up_info == fashion['fid']:
                up_icon = fashion['icon']
                up_name = fashion['name']
            if buy_info:
                if up_info != fashion['fid']:
                    jishu=jishu+1
                    if jishu<3:
                        lh_msg =lh_msg+f"\n{fashion['icon']}\n{fashion['name']}"
    owner = duel._get_card_owner(gid, cid)
    if uid!=owner:
        msg = f'{c.name}现在正在\n[CQ:at,qq={owner}]的身边哦，您无法查询哦。'
        await bot.send(ev, msg)
        return
    if owner == 0:
        await bot.send(ev, f'{c.name}现在还是单身哦，快去约到她吧。{nvmes}', at_sender=True)
        return
    if uid==owner:
        queen_msg=''
        if duel._get_queen_owner(gid,cid) !=0:
            queen_msg=f'现在是您的妻子\n'
        if duel._get_favor(gid,uid,cid)== None:
            duel._set_favor(gid,uid,cid,0)
        favor= duel._get_favor(gid,uid,cid)
        relationship,text = get_relationship(favor)
        if up_icon:
            nvmes=up_icon
        up_msg=''
        if up_name:
            up_msg=f"\n目前穿戴的时装是{up_name}\n"
        if lh_msg:
            lh_msg = f"\n您为{c.name}购买的时装有(只显示未穿的2件)："+lh_msg
        msg = f'\n{c.name}{queen_msg}对你的好感是{favor}\n你们的关系是{relationship}\n“{text}”{up_msg}{nvmes}{lh_msg}'
        tas_list=[]
        data = {
            "type": "node",
            "data": {
                "name": str(NICKNAME[0]),
                "uin": str(ev.self_id),
                "content":msg
                    }
                }
        tas_list.append(data)
        await bot.send_group_forward_msg(group_id=ev['group_id'], messages=tas_list)
