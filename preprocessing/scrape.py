# Copyright 2021 Moonsik Park

import requests
import json


headers = {'accept': "application/json, text/javascript, */*; q=0.01", "accept-language": "en-US,en;q=0.9,ko;q=0.8",
    "x-requested-with": "XMLHttpRequest", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36", "Host": "www.encar.com"}


def scrape(car_id):
    response = requests.get(f"http://www.encar.com/dc/dc_cardetailview.do?method=ajaxInspectView&rgsid={car_id}&sdFlag=N", headers=headers)
    if '[{"msg":"SUCCESS","' in response.text:
        data = json.loads(response.text)
        
        gen = data[0]["inspect"]["carSaleDto"]["modelNm"]
        year = data[0]["inspect"]["carSaleDto"]["formYear"]
        km = data[0]["inspect"]["carSaleDto"]["mileage"]
        trim = ""
        if "badgeDetailNm" in data[0]["inspect"]["carSaleDto"]:
            trim = data[0]["inspect"]["carSaleDto"]["badgeDetailNm"]
        if not trim:
            trim = data[0]["inspect"]["carSaleDto"]["badgeNm"]
        color = data[0]["inspect"]["carSaleDto"]["color"]

        accident = False
        if data[0]["inspect"]["direct"]:
            if data[0]["inspect"]["direct"]["outer"]:
                for item in data[0]["inspect"]["direct"]["outer"]:
                    if data[0]["inspect"]["direct"]["outer"][item]:
                        if len(data[0]["inspect"]["direct"]["outer"][item]) > 0:
                            accident = True

        price = data[0]["inspect"]["carSaleDto"]["price"]


        displaydata = dict(gen=gen, trim=trim, year=year, km=km, color=color, accident=accident, price=price)

        if color in ["흰색"]:
            color = "1"
        elif color in ["검정색", "은색", "명은색", "은회색", "쥐색"]:
            color = "2"
        else:
            color = "3"

        if accident:
            accident = 1
        else:
            accident = 0

        if gen == "아반떼 AD":
            gen = "3"
            if trim == "1.6 GDI 스타일":
                trim = "0"
            if trim == "1.6 GDI 밸류 플러스":
                trim = "1"
            if trim == "1.6 GDI 스마트":
                trim = "1"
            if trim == "1.6 GDI 모던":
                trim = "2"
            if trim == "1.6 GDI 프리미엄":
                trim = "2"
        if gen == "아반떼 (CN7)":
            gen = "5"
            if trim == "스마트":
                trim = "0"
            if trim == "모던":
                trim = "1"
            if trim == "인스퍼레이션":
                trim = "2"
        if gen == "아반떼 HD":
            gen = "0"
            if trim == "밸류":
                trim = "0"
            if trim == "디럭스":
                trim = "0"
            if trim == "럭셔리":
                trim = "1"
            if trim == "파이브 밀리언":
                trim = "2"
            if trim == "프리미어":
                trim = "2"
            if trim == "엘레강스 스페셜":
                trim = "2"
            if trim == "럭셔리 블랙":
                trim = "2"
            if trim == "럭셔리 어드밴스팩":
                trim = "2"
            if trim == "월드컵 스페셜 에디션":
                trim = "2"
        if gen == "아반떼 MD":
            gen = "1"
            if trim == "M16 GDI 디럭스":
                trim = "0"
            if trim == "M16 GDI 스타일":
                trim = "0"
            if trim == "M16 GDI 럭셔리":
                trim = "1"
            if trim == "M16 GDI 스마트":
                trim = "1"
            if trim == "M16 GDI 블루세이버":
                trim = "1"
            if trim == "M16 GDI 에비뉴":
                trim = "1"
            if trim == "M16 GDI 모던":
                trim = "2"
            if trim == "M16 GDI 탑":
                trim = "2"
            if trim == "M16 GDI 프리미어":
                trim = "2"
            if trim == "M16 GDI 프리미엄":
                trim = "2"
        if gen == "더 뉴 아반떼":
            gen = "2"
            if trim == "1.6 GDi 스타일":
                trim = "0"
            if trim == "1.6 GDi 스마트":
                trim = "1"
            if trim == "1.6 GDi 월드컵 에디션":
                trim = "1"
            if trim == "1.6 GDi 모던":
                trim = "1"
            if trim == "M16 GDI 텐밀리언 리미티드":
                trim = "2"
            if trim == "M16 GDI 프리미엄":
                trim = "2"
        if gen == "더 뉴 아반떼 AD":
            gen = "4"
            if trim == "스타일":
                trim = "0"
            if trim == "스마트 초이스":
                trim = "0"
            if trim == "스마트":
                trim = "1"
            if trim == "프리미엄":
                trim = "2"
            if trim == "모던":
                trim = "2"
        traindata = dict(gen=gen, trim=trim, year=year, km=km, color=color, accident=accident, price=price)

        return dict(displaydata=displaydata, traindata=traindata)
    else:
        return False

