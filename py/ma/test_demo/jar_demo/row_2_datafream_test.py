
import ast
import pandas as pd
import numpy as np
import time
import json
import os

str = """[{"BFIC_3001_F03_MV_o":60.0,"BFIC0302_F03_o":4.595848999999999,"BFIC_3003_F03_MV_o":54.969469999999994,"BPIA0303_F03_o":50.40293,"BTIR0302_F03_o":56.813190000000006,"PIA0302_F03_o":361.1721,"BTIR0304_F03_o":51.904759999999996,"BPIA0304_F03_o":164.8352,"BPIR0305_F03_o":0.0,"BTI0301_F03_o":235.7509,"BTIR0303_F03_o":56.996340000000004,"BTIR0305_F03_o":547.9854,"BTIR0306_F03_o":139.8779,"FEED_SK04_F03_o":6.397954,"SETPOINT04_F03_o":6.4,"BFIC_3002_F03_MV_o":59.365080000000006,"gw_id":10,"BFIC_3001_F03_MV":86.49,"BFIC0302_F03":3.6948,"BFIC_3003_F03_MV":48.5,"BPIA0303_F03":211.06,"BTIR0302_F03":57.99,"PIA0302_F03":469.93,"BTIR0304_F03":53.39,"BPIA0304_F03":163.6,"BPIR0305_F03":53.27,"BTI0301_F03":201.39,"BTIR0303_F03":78.47,"BTIR0305_F03":541.39,"BTIR0306_F03":230.41,"FEED_SK04_F03":4.0471,"SETPOINT04_F03":5.7208,"BFIC_3002_F03_MV":61.45,"CZ3_OP1":0.691,"CZ3_OP2":0.974,"CZ3_OP3":6.956,"op":-0.1687,"time":1578108780}, {"BFIC_3001_F03_MV_o":60.0,"BFIC0302_F03_o":4.561661,"BFIC_3003_F03_MV_o":54.969469999999994,"BPIA0303_F03_o":51.28205,"BTIR0302_F03_o":56.996340000000004,"PIA0302_F03_o":361.4652,"BTIR0304_F03_o":52.08791,"BPIA0304_F03_o":167.033,"BPIR0305_F03_o":0.0,"BTI0301_F03_o":234.8718,"BTIR0303_F03_o":56.813190000000006,"BTIR0305_F03_o":547.6923,"BTIR0306_F03_o":139.6825,"FEED_SK04_F03_o":6.388799,"SETPOINT04_F03_o":6.4,"BFIC_3002_F03_MV_o":62.344319999999996,"gw_id":10,"BFIC_3001_F03_MV":86.49,"BFIC0302_F03":3.6948,"BFIC_3003_F03_MV":48.5,"BPIA0303_F03":211.06,"BTIR0302_F03":57.99,"PIA0302_F03":469.93,"BTIR0304_F03":53.39,"BPIA0304_F03":163.6,"BPIR0305_F03":53.27,"BTI0301_F03":201.39,"BTIR0303_F03":78.47,"BTIR0305_F03":541.39,"BTIR0306_F03":230.41,"FEED_SK04_F03":4.0471,"SETPOINT04_F03":5.7208,"BFIC_3002_F03_MV":61.45,"CZ3_OP1":0.691,"CZ3_OP2":0.974,"CZ3_OP3":6.956,"op":-0.1687,"time":1578108600}, {"BFIC_3001_F03_MV_o":60.0,"BFIC0302_F03_o":4.510378,"BFIC_3003_F03_MV_o":54.969469999999994,"BPIA0303_F03_o":50.40293,"BTIR0302_F03_o":56.59341,"PIA0302_F03_o":357.9487,"BTIR0304_F03_o":51.684979999999996,"BPIA0304_F03_o":162.8816,"BPIR0305_F03_o":0.0,"BTI0301_F03_o":234.8718,"BTIR0303_F03_o":57.17949,"BTIR0305_F03_o":550.3297,"BTIR0306_F03_o":141.8315,"FEED_SK04_F03_o":6.393622,"SETPOINT04_F03_o":6.4,"BFIC_3002_F03_MV_o":60.75702,"gw_id":10,"BFIC_3001_F03_MV":86.49,"BFIC0302_F03":3.6948,"BFIC_3003_F03_MV":48.5,"BPIA0303_F03":211.06,"BTIR0302_F03":57.99,"PIA0302_F03":469.93,"BTIR0304_F03":53.39,"BPIA0304_F03":163.6,"BPIR0305_F03":53.27,"BTI0301_F03":201.39,"BTIR0303_F03":78.47,"BTIR0305_F03":541.39,"BTIR0306_F03":230.41,"FEED_SK04_F03":4.0471,"SETPOINT04_F03":5.7208,"BFIC_3002_F03_MV":61.45,"CZ3_OP1":0.691,"CZ3_OP2":0.974,"CZ3_OP3":6.956,"op":-0.1687,"time":1578109140}, {"BFIC_3001_F03_MV_o":60.0,"BFIC0302_F03_o":4.510378,"BFIC_3003_F03_MV_o":54.969469999999994,"BPIA0303_F03_o":49.81685,"BTIR0302_F03_o":56.813190000000006,"PIA0302_F03_o":359.4139,"BTIR0304_F03_o":51.75824,"BPIA0304_F03_o":163.6142,"BPIR0305_F03_o":0.0,"BTI0301_F03_o":235.6777,"BTIR0303_F03_o":56.996340000000004,"BTIR0305_F03_o":549.7436,"BTIR0306_F03_o":141.8315,"FEED_SK04_F03_o":6.402611,"SETPOINT04_F03_o":6.4,"BFIC_3002_F03_MV_o":60.0,"gw_id":10,"BFIC_3001_F03_MV":86.49,"BFIC0302_F03":3.6948,"BFIC_3003_F03_MV":48.5,"BPIA0303_F03":211.06,"BTIR0302_F03":57.99,"PIA0302_F03":469.93,"BTIR0304_F03":53.39,"BPIA0304_F03":163.6,"BPIR0305_F03":53.27,"BTI0301_F03":201.39,"BTIR0303_F03":78.47,"BTIR0305_F03":541.39,"BTIR0306_F03":230.41,"FEED_SK04_F03":4.0471,"SETPOINT04_F03":5.7208,"BFIC_3002_F03_MV":61.45,"CZ3_OP1":0.691,"CZ3_OP2":0.974,"CZ3_OP3":6.956,"op":-0.1687,"time":1578108960}]
"""
str1 = """[{"BFIC_3001_F03_MV_o":62.490840000000006,"BFIC0302_F03_o":4.473749,"BFIC_3003_F03_MV_o":54.969469999999994,"BPIA0303_F03_o":56.41026,"BTIR0302_F03_o":56.88645,"PIA0302_F03_o":370.1099,"BTIR0304_F03_o":51.8315,"BPIA0304_F03_o":165.2015,"BPIR0305_F03_o":0.0,"BTI0301_F03_o":236.8498,"BTIR0303_F03_o":56.88645,"BTIR0305_F03_o":292.1612,"BTIR0306_F03_o":83.22344,"FEED_SK04_F03_o":6.387466000000001,"SETPOINT04_F03_o":6.4,"BFIC_3002_F03_MV_o":60.7326,"gw_id":10,"BFIC_3001_F03_MV":86.49,"BFIC0302_F03":3.6948,"BFIC_3003_F03_MV":48.5,"BPIA0303_F03":211.06,"BTIR0302_F03":57.99,"PIA0302_F03":469.93,"BTIR0304_F03":53.39,"BPIA0304_F03":163.6,"BPIR0305_F03":53.27,"BTI0301_F03":201.39,"BTIR0303_F03":78.47,"BTIR0305_F03":541.39,"BTIR0306_F03":230.41,"FEED_SK04_F03":4.0471,"SETPOINT04_F03":5.7208,"BFIC_3002_F03_MV":61.45,"CZ3_OP1":0.691,"CZ3_OP2":0.974,"CZ3_OP3":6.956,"op":-0.1687,"time":1578103560}, {"BFIC_3001_F03_MV_o":62.490840000000006,"BFIC0302_F03_o":4.556776999999999,"BFIC_3003_F03_MV_o":54.969469999999994,"BPIA0303_F03_o":59.48718,"BTIR0302_F03_o":56.666669999999996,"PIA0302_F03_o":378.7546,"BTIR0304_F03_o":51.4652,"BPIA0304_F03_o":164.1026,"BPIR0305_F03_o":0.0,"BTI0301_F03_o":236.4103,"BTIR0303_F03_o":56.996340000000004,"BTIR0305_F03_o":292.4542,"BTIR0306_F03_o":83.61417,"FEED_SK04_F03_o":6.383888,"SETPOINT04_F03_o":6.4,"BFIC_3002_F03_MV_o":58.778999999999996,"gw_id":10,"BFIC_3001_F03_MV":86.49,"BFIC0302_F03":3.6948,"BFIC_3003_F03_MV":48.5,"BPIA0303_F03":211.06,"BTIR0302_F03":57.99,"PIA0302_F03":469.93,"BTIR0304_F03":53.39,"BPIA0304_F03":163.6,"BPIR0305_F03":53.27,"BTI0301_F03":201.39,"BTIR0303_F03":78.47,"BTIR0305_F03":541.39,"BTIR0306_F03":230.41,"FEED_SK04_F03":4.0471,"SETPOINT04_F03":5.7208,"BFIC_3002_F03_MV":61.45,"CZ3_OP1":0.691,"CZ3_OP2":0.974,"CZ3_OP3":6.956,"op":-0.1687,"time":1578103380}, {"BFIC_3001_F03_MV_o":62.490840000000006,"BFIC0302_F03_o":4.466423000000001,"BFIC_3003_F03_MV_o":54.969469999999994,"BPIA0303_F03_o":60.07326,"BTIR0302_F03_o":56.996340000000004,"PIA0302_F03_o":382.8571,"BTIR0304_F03_o":51.8315,"BPIA0304_F03_o":165.9341,"BPIR0305_F03_o":0.0,"BTI0301_F03_o":237.1429,"BTIR0303_F03_o":56.813190000000006,"BTIR0305_F03_o":291.8681,"BTIR0306_F03_o":82.24664,"FEED_SK04_F03_o":6.4037809999999995,"SETPOINT04_F03_o":6.4,"BFIC_3002_F03_MV_o":63.76068000000001,"gw_id":10,"BFIC_3001_F03_MV":86.49,"BFIC0302_F03":3.6948,"BFIC_3003_F03_MV":48.5,"BPIA0303_F03":211.06,"BTIR0302_F03":57.99,"PIA0302_F03":469.93,"BTIR0304_F03":53.39,"BPIA0304_F03":163.6,"BPIR0305_F03":53.27,"BTI0301_F03":201.39,"BTIR0303_F03":78.47,"BTIR0305_F03":541.39,"BTIR0306_F03":230.41,"FEED_SK04_F03":4.0471,"SETPOINT04_F03":5.7208,"BFIC_3002_F03_MV":61.45,"CZ3_OP1":0.691,"CZ3_OP2":0.974,"CZ3_OP3":6.956,"op":-0.1687,"time":1578103740}, {"BFIC_3001_F03_MV_o":62.490840000000006,"BFIC0302_F03_o":4.576313,"BFIC_3003_F03_MV_o":54.969469999999994,"BPIA0303_F03_o":51.86813,"BTIR0302_F03_o":56.813190000000006,"PIA0302_F03_o":359.5604,"BTIR0304_F03_o":51.75824,"BPIA0304_F03_o":162.8816,"BPIR0305_F03_o":0.0,"BTI0301_F03_o":238.6081,"BTIR0303_F03_o":56.813190000000006,"BTIR0305_F03_o":293.6264,"BTIR0306_F03_o":83.22344,"FEED_SK04_F03_o":6.376784,"SETPOINT04_F03_o":6.4,"BFIC_3002_F03_MV_o":62.85714,"gw_id":10,"BFIC_3001_F03_MV":86.49,"BFIC0302_F03":3.6948,"BFIC_3003_F03_MV":48.5,"BPIA0303_F03":211.06,"BTIR0302_F03":57.99,"PIA0302_F03":469.93,"BTIR0304_F03":53.39,"BPIA0304_F03":163.6,"BPIR0305_F03":53.27,"BTI0301_F03":201.39,"BTIR0303_F03":78.47,"BTIR0305_F03":541.39,"BTIR0306_F03":230.41,"FEED_SK04_F03":4.0471,"SETPOINT04_F03":5.7208,"BFIC_3002_F03_MV":61.45,"CZ3_OP1":0.691,"CZ3_OP2":0.974,"CZ3_OP3":6.956,"op":-0.1687,"time":1578103020}, {"BFIC_3001_F03_MV_o":62.490840000000006,"BFIC0302_F03_o":4.576313,"BFIC_3003_F03_MV_o":54.969469999999994,"BPIA0303_F03_o":58.1685,"BTIR0302_F03_o":56.59341,"PIA0302_F03_o":376.2637,"BTIR0304_F03_o":51.4652,"BPIA0304_F03_o":162.149,"BPIR0305_F03_o":0.0,"BTI0301_F03_o":238.02200000000002,"BTIR0303_F03_o":56.996340000000004,"BTIR0305_F03_o":293.3333,"BTIR0306_F03_o":83.80951999999999,"FEED_SK04_F03_o":6.387176999999999,"SETPOINT04_F03_o":6.4,"BFIC_3002_F03_MV_o":60.43956,"gw_id":10,"BFIC_3001_F03_MV":86.49,"BFIC0302_F03":3.6948,"BFIC_3003_F03_MV":48.5,"BPIA0303_F03":211.06,"BTIR0302_F03":57.99,"PIA0302_F03":469.93,"BTIR0304_F03":53.39,"BPIA0304_F03":163.6,"BPIR0305_F03":53.27,"BTI0301_F03":201.39,"BTIR0303_F03":78.47,"BTIR0305_F03":541.39,"BTIR0306_F03":230.41,"FEED_SK04_F03":4.0471,"SETPOINT04_F03":5.7208,"BFIC_3002_F03_MV":61.45,"CZ3_OP1":0.691,"CZ3_OP2":0.974,"CZ3_OP3":6.956,"op":-0.1687,"time":1578103200}]##{"BFIC_3021_F03_MV": {"cnCode": "2#\u70892#\u7f57\u8328\u98ce\u673a\u51fa\u53e3\u98ce\u91cf\u8c03\u9600", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "BFIC0304_F03": {"cnCode": "\u4e00\u6b21\u98ce\u673a\u6d41\u91cf", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "BMII_C301_F03": {"cnCode": "1#\u7a7a\u6c14\u98ce\u673a\u7535\u6d41", "belongCate": "observedCol/decisionCol", "enUnit": "A"}, "BFIC0305_F03": {"cnCode": "\u4e8c\u6b21\u98ce\u673a\u6d41\u91cf", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "BMIC_C301_F03_MV": {"cnCode": "1#\u7a7a\u6c14\u98ce\u673a\u8f6c\u901f\u63a7\u5236", "belongCate": "observedCol/decisionCol", "enUnit": "rpm"}, "BFIC_3020_F03_MV": {"cnCode": "2#\u70891#\u7f57\u8328\u98ce\u673a\u51fa\u53e3\u98ce\u91cf\u8c03\u9600", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "BFIC_3005_F03_MV": {"cnCode": "1#\u7f57\u8328\u98ce\u673a\u51fa\u98ce\u91cf\u8c03", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "BFIC_3001_F03_MV": {"cnCode": "\u8fdbAHF\u6362\u70ed\u5668\u84b8\u6c7d\u8c03\u8282", "belongCate": "observedCol/decisionCol", "enUnit": "t/h"}, "BFIC0302_F03": {"cnCode": "AHF\u6362\u70ed\u5668\u8fdb\u53e3AHF\u6d41\u91cf", "belongCate": "observedCol/decisionCol", "enUnit": "t/h"}, "BFIC_3003_F03_MV": {"cnCode": "AHF\u6362\u70ed\u5668\u51fa\u53e3HF\u538b\u8c03", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BFIC_3007_F03_MV": {"cnCode": "\u8fdb\u4e0b\u6599\u65cb\u8f6c\u9600\u51b7\u5374\u6c34\u8c03", "belongCate": "observedCol/decisionCol", "enUnit": ""}, "BFIQ0306_F03": {"cnCode": "\u8fdb\u4e0b\u6599\u65cb\u8f6c\u9600\u51b7\u5374\u6c34F", "belongCate": "observedCol/decisionCol", "enUnit": ""}, "BMIC_L303_F03_MV": {"cnCode": "\u6c1f\u5316\u94dd\u4e0b\u6599\u56de\u8f6c\u9600\u901f\u63a7", "belongCate": "observedCol/decisionCol", "enUnit": ""}, "BPIA0303_F03": {"cnCode": "AHF\u6362\u70ed\u5668\u8fdb\u53e3\u84b8\u6c7d\u538b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BMII_C302_F03": {"cnCode": "2#\u7a7a\u6c14\u98ce\u673a\u7535\u6d41\u6307\u793a", "belongCate": "observedCol/decisionCol", "enUnit": "A"}, "BTIR0302_F03": {"cnCode": "AHF\u6362\u70ed\u5668\u51fa\u53e3HF\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "PIA0302_F03": {"cnCode": "\u84b8\u6c7d\u51cf\u538b\u9600\u540e\u538b\u529b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BPIA0308_F03": {"cnCode": "2#\u7a7a\u6c14\u98ce\u673a\u51fa\u53e3\u538b\u529b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BFIC_3006_F03_MV": {"cnCode": "2#\u7f57\u8328\u98ce\u673a\u51fa\u98ce\u91cf\u8c03", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "BTIR0304_F03": {"cnCode": "AHF\u6362\u70ed\u5668\u5e95\u90e8\u9178\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "BMIC_C302_F03_MV": {"cnCode": "2#\u7a7a\u6c14\u98ce\u673a\u8f6c\u901f\u63a7\u5236", "belongCate": "observedCol/decisionCol", "enUnit": ""}, "BMIIL303_F03": {"cnCode": "\u4e0b\u6599\u56de\u8f6c\u9600\u7535\u6d41", "belongCate": "observedCol/decisionCol", "enUnit": "A"}, "BPIA0304_F03": {"cnCode": "AHF\u6362\u70ed\u5668\u51fa\u53e3HF\u538b\u529b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BPIA0307_F03": {"cnCode": "1#\u7a7a\u6c14\u98ce\u673a\u51fa\u53e3\u538b\u529b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BPIR0305_F03": {"cnCode": "\u6df7\u5408\u4e09\u901a\u8fdb\u53e3HF\u538b\u529b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BPIR0321_F03": {"cnCode": "2\u7ea7\u9664\u5c18\u5668\u8fdb\u53e3\u538b\u529b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BPIRA0311_F03": {"cnCode": "\u786b\u5316\u5e8a\u5e95\u90e8\u538b\u529b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BPIRA0312_F03": {"cnCode": "\u786b\u5316\u5e8a\u4e2d\u90e8\u538b\u529b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BPIRA0314_F03": {"cnCode": "\u4e00\u7ea7\u6c14\u6d41\u53cd\u5e94\u5668\u8fdb\u53e3\u538b", "belongCate": "observedCol/decisionCol", "enUnit": "Kpa"}, "BTI0301_F03": {"cnCode": "\u8fdbAHF\u6362\u70ed\u5668\u84b8\u6c7d\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "BTI0319_F03": {"cnCode": "\u4e0b\u6599\u56de\u8f6c\u9600\u51b7\u5374\u56de\u6c34\u6e29", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "BTI0320_F03": {"cnCode": "\u6c1f\u5316\u94dd\u8fdb\u51b7\u5374\u7089\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "BTI0321_F03": {"cnCode": "\u6c1f\u5316\u94dd\u51fa\u51b7\u5374\u7089\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "BTIR0303_F03": {"cnCode": "\u6df7\u5408\u4e09\u901a\u8fdb\u53e3HF\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "BTIR0305_F03": {"cnCode": "\u81a8\u80c0\u5f2f\u5934\u70ed\u6c14\u4f53\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "BTIR0306_F03": {"cnCode": "\u6df7\u5408\u4e09\u901a\u6df7\u5408\u6c14\u4f53\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "BTIR0307_F03": {"cnCode": "\u786b\u5316\u5e8a\u4e0b\u90e8\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "BTIR0308_F03": {"cnCode": "\u786b\u5316\u5e8a\u4e0a\u90e8\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "BTIR0309_F03": {"cnCode": "\u4e00\u7ea7\u6c14\u6d41\u53cd\u5e94\u5668\u51fa\u53e3\u6e29", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "BTIR0310_F03": {"cnCode": "\u4e8c\u7ea7\u6c14\u6d41\u53cd\u5e94\u5668\u4e0b\u53e3\u6e29", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "BTIR0311_F03": {"cnCode": "\u4e09\u7ea7\u6c14\u6d41\u53cd\u5e94\u5668\u51fa\u53e3\u6e29", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "BTIR0316_F03": {"cnCode": "2\u7ea7\u9664\u5c18\u5668\u4e0b\u53e3\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "BTIR0313_F03": {"cnCode": "\u56db\u7ea7\u6c14\u6d41\u53cd\u5e94\u5668\u51fa\u53e3\u6c14", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "BTIR0314_F03": {"cnCode": "\u56db\u7ea7\u6c14\u6d41\u53cd\u5e94\u5668\u4e0b\u53e3\u6e29", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "BTIR0315_F03": {"cnCode": "2\u7ea7\u9664\u5c18\u5668\u51fa\u53e3\u6c14\u4f53\u6e29", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "BTIR0312_F03": {"cnCode": "\u4e09\u7ea7\u6c14\u6d41\u53cd\u5e94\u5668\u4e0b\u53e3\u6e29", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "FEED_SK04_F03": {"cnCode": "\u6d41\u91cf\u5b9e\u9645\u503c", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "TI0318_F03": {"cnCode": "\u51b7\u5374\u6c34\u4e3b\u7ba1\u6e29\u5ea6", "belongCate": "observedCol/decisionCol", "enUnit": "\u2103"}, "SETPOINT04_F03": {"cnCode": "\u6d41\u91cf\u8bbe\u5b9a", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "BFIC_3002_F03_MV": {"cnCode": "\u8fdbAHF\u6362\u70ed\u5668AHF\u8c03\u8282", "belongCate": "observedCol/decisionCol", "enUnit": "Nm3/h"}, "CZ3_OP1": {"cnCode": "AHF\u5b9e\u9645\u5355\u8017", "belongCate": "optCol", "enUnit": "", "maxvalue": "nan", "minvalue": "nan"}, "CZ3_OP2": {"cnCode": "\u6c22\u94dd\u5b9e\u9645\u5355\u8017", "belongCate": "optCol", "enUnit": "", "maxvalue": "nan", "minvalue": "nan"}, "CZ3_OP3": {"cnCode": "\u5929\u7136\u6c14\u5b9e\u9645\u5355\u8017", "belongCate": "optCol", "enUnit": "", "maxvalue": "nan", "minvalue": "nan"}}
"""

# # 转成列表
# resList = ast.literal_eval(str)
#
# df = pd.DataFrame(resList)
# # print(df)
#
# # 获取列信息
# columns = list(df)
#
# # # 过滤出原始数据列名
# srcColumns = list(filter(lambda n: n[-2:] == "_o", columns))
#
# resColumns = [i for i in columns if i not in srcColumns]
# print("result")
# resdf = df[resColumns]
# print(resdf)
# resdf.to_csv("result.csv", index=False)
#
# srcColumns.append('time')
# print(srcColumns)
#
# # # 过滤出原始数据
# srcdf = df[srcColumns]
# # print("原始数据")
# # print(srcdf)
# # srcdf.to_csv("原始数据.csv", index=False)
# #
# # 去掉列名后缀
# srcColumnsnew = list(map(lambda x: x[:-2] if x[-2:] == "_o" else x, srcColumns))
# #
# # # 去掉原始数据列名后缀
# srcdf.columns = srcColumnsnew
# print("去掉原始数据列名后缀")
# print(srcdf)
# srcdf.to_csv("去掉原始数据列名后缀.csv", index=False)


def opt_compute_fetch_predict_result(row):
    """
        预测结果、输入结果，规整格式，返回给前端.
    """
    value = row.split("##")

    data = value[0]
    paramOriJson = value[1]

    dataList = ast.literal_eval(data)
    df = pd.DataFrame(dataList)

    # 获取列信息
    columns = list(df)

    # 过滤出src数据列名
    srcColumns = list(filter(lambda n: n[-2:] == "_o", columns))
    # 结果datafream列名
    resColumns = [i for i in columns if i not in srcColumns]
    # 结果datafream
    dfOutput = df[resColumns]
    # print(dfOutput)
    # print("*" * 100)

    srcColumns.append('time')
    # # 过滤出原始数据
    dfInput = df[srcColumns]

    # 去掉列名后缀
    srcColumnsnew = list(map(lambda x: x[:-2] if x[-2:] == "_o" else x, srcColumns))
    #
    # # 去掉原始数据列名后缀
    dfInput.columns = srcColumnsnew
    # print(dfInput)
    # print("*" * 100)

    print("paramOriJson...{}".format(paramOriJson))
    oriParamDict = json.loads(paramOriJson)

    # merge，结果、输入文件.
    vResultList = []
    # 逐行处理.
    for index, oRow in dfOutput.iterrows():
        # 取结果文件[time]关键字.
        # print("2222222222222...oRow...", oRow)
        # print("time", oRow['time'])
        oTime = oRow['time']
        # print(oRow)

        # 按time索引，过滤匹配input记录.
        iRow = dfInput[dfInput['time'] == oTime]
        # print("2222222222222...iRow...", iRow)

        if len(iRow) > 0:
            iRow = iRow.iloc[0]  # 只取第1行.
            vResultItemDict = {
                "time": None,
                "gw_id": None,
                "optCol": [],
                "paramCol": [],
            }
            # 逐列计算.
            for oClmnName in dfOutput.columns:
                # print("2222222222222...{} | {} | {}".format(oClmnName, oRow.get(oClmnName), iRow.get(oClmnName)))
                if oClmnName == "time":  # 时间参数.
                    vResultItemDict["time"] = {
                        "resultValue": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(oRow.get(oClmnName)))),
                        "inValue": oRow.get(oClmnName),
                    }
                elif oClmnName == "gw_id":  # 工况变量.
                    vResultItemDict["gw_id"] = {
                        "resultValue": int(oRow.get(oClmnName)),
                    }
                elif oClmnName == "op":  # .
                    vResultItemDict["op"] = {
                        "resultValue": int(oRow.get(oClmnName)),
                    }
                elif oClmnName in ["CZ3_OP1", "CZ3_OP2", "CZ3_OP3"]:
                    v = oriParamDict.get(oClmnName, None)
                    if v is None:
                        continue
                    # 目标列，插入列表.
                    if v["belongCate"] == "optCol":
                        vResultItemDict["optCol"].append({
                            "enCode": oClmnName,
                            "cnCode": v["cnCode"],
                            "unit": v["enUnit"],
                            "resultValue": "%.4f" % (float(oRow.get(oClmnName))),
                        })

                # elif oRow.get(oClmnName) and iRow.get(oClmnName):
                else:
                    v = oriParamDict.get(oClmnName, None)
                    if v is None:
                        continue

                    # 参数列，插入列表.
                    if v["belongCate"].find("observedCol") >= 0:
                        vResultItemDict["paramCol"].append({
                            "enCode": oClmnName,
                            "cnCode": v["cnCode"],
                            "unit": v["enUnit"],
                            "resultValue": "%.4f" % (float(oRow.get(oClmnName))),
                            "inputValue": "%.4f" % (float(iRow.get(oClmnName))),
                            "diffValue": "%.4f" % (float(oRow.get(oClmnName)) - float(iRow.get(oClmnName)))
                        })

            # print("2222222222222...{}".format(json.dumps(vResultItemDict)))

            # 插入, 结果集列表.
            if vResultItemDict['time']:
                vResultList.append(vResultItemDict)
        # break

    # print("2222222222222...vResultList_len={}".format(len(vResultList)))
    return vResultList


if __name__ == '__main__':
    predictResult = opt_compute_fetch_predict_result(str1)

    resjson = {"predictResult": predictResult}
    print(json.dumps(resjson))



