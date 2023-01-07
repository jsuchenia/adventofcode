#!/usr/local/bin/python3
import io
import math

def parseHex(hexdata):
    s = io.StringIO()
    for c in hexdata:
        s.write('{:04b}'.format(int(c, 16)))
    s.seek(0)

    return s

def getPacket(s):
    ver = s.read(3)
    type = s.read(3)
    if len(ver) < 3 or len(type) < 3:
        return None

    ver = int(ver, 2)

    p = {
        'ver': ver,
        'type': int(type, 2)
    }

    if p['type'] == 4:
        val = ""
        while True:
            x = s.read(5)
            val += x[1:]
            if x[0] == '0': break
        p['val'] = int(val, 2)
    else:
        ltype = s.read(1)
        p['ltype'] = ltype
        if ltype == '0':
            bitdata = s.read(15)
            if len(bitdata) < 15:
                return None
            bitsize = int(bitdata, 2)
            subpackets = []
            bitposition = s.tell() + bitsize
            while s.tell() < bitposition:
                subpackets.append(getPacket(s))
            p['subpackets'] = subpackets
        elif ltype == '1':
            packets = int(s.read(11), 2)
            p['subpackets'] = [getPacket(s) for x in range(packets)]

    return p

def getVersionSum(p):
    result = p['ver']

    if 'subpackets' in p:
        for sub in p['subpackets']:
            result += getVersionSum(sub)
    return result

def checkVersions(hexdata):
    s = parseHex(hexdata)
    result = 0;

    while True:
        p = getPacket(s)
        if p is None: break
        result += getVersionSum(p)

    print("Versions sum", result)
    return result

def getPacketValue(p):
    type = p['type']

    if type == 4:
        return p['val']
    values = [getPacketValue(sub) for sub in p['subpackets']]

    if type == 0:
        return sum(values)
    elif type == 1:
        return math.prod(values)
    elif type == 2:
        return min(values)
    elif type == 3:
        return max(values)
    elif type == 5:
        return 1 if values[0] > values[1] else 0
    elif type == 6:
        return 1 if values[0] < values[1] else 0
    elif type == 7:
        return 1 if values[0] == values[1] else 0

    return -1

def getHexValue(hexdata):
    s = parseHex(hexdata)
    p = getPacket(s)
    val = getPacketValue(p)

    print("Packet value: ", val)
    return val

def test_decoder_versions_example():
    assert checkVersions('D2FE28') == 6
    assert checkVersions('38006F45291200') == 9
    assert checkVersions('EE00D40C823060') == 14
    assert checkVersions('8A004A801A8002F478') == 16
    assert checkVersions('620080001611562C8802118E34') == 12
    assert checkVersions('C0015000016115A2E0802F182340') == 23
    assert checkVersions('A0016C880162017C3686B18A3D4780') == 31

def test_decoder_versions_data():
    data = open("data.txt", "r").read()
    assert checkVersions(data) == 897

def test_decoder_hex_example():
    assert getHexValue('C200B40A82') == 3
    assert getHexValue('04005AC33890') == 54
    assert getHexValue('880086C3E88112') == 7
    assert getHexValue('CE00C43D881120') == 9
    assert getHexValue('D8005AC2A8F0') == 1
    assert getHexValue('F600BC2D8F') == 0
    assert getHexValue('9C005AC2F8F0') == 0
    assert getHexValue('9C0141080250320F1802104A08') == 1

def test_decoder_hex_data():
    data = open("data.txt", "r").read()
    assert getHexValue(data) == 9485076995911
