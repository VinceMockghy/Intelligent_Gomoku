#发送棋盘点移动


from periphery import Serial
import json
import time
#yello gnd
#green G19
#blue G18
serial = Serial('/dev/ttyTHS1', 115200)


init={
    0:{"set":0,"0":600,"1":697,"2":565,"3":516,"4":389,"5":504},
    1:{"set":1,"0":580,"1":697,"2":565,"3":515,"4":370,"5":504},
    2:{"set":2,"0":565,"1":697,"2":565,"3":516,"4":360,"5":504},
    3:{"set":3,"0":545,"1":671,"2":565,"3":516,"4":377,"5":504},
    4:{"set":4,"0":530,"1":671,"2":565,"3":515,"4":363,"5":504},
    5:{"set":5,"0":500,"1":671,"2":565,"3":516,"4":377,"5":504},
    6:{"set":6,"0":470,"1":671,"2":565,"3":515,"4":377,"5":504},
    7:{"set":7,"0":453,"1":698,"2":565,"3":516,"4":378,"5":504},
    8:{"set":8,"0":437,"1":698,"2":565,"3":516,"4":390,"5":504},
    9:{"set":10,"0":606,"1":649,"2":540,"3":514,"4":391,"5":504},
    10:{"set":11,"0":587,"1":646,"2":540,"3":515,"4":376,"5":504},
    11:{"set":12,"0":567,"1":647,"2":540,"3":515,"4":351,"5":504},
    12:{"set":13,"0":546,"1":646,"2":540,"3":516,"4":351,"5":504},
    13:{"set":14,"0":525,"1":646,"2":540,"3":516,"4":335,"5":504},
    14:{"set":15,"0":493,"1":646,"2":540,"3":516,"4":344,"5":504},
    15:{"set":16,"0":470,"1":647,"2":540,"3":516,"4":355,"5":504},
    16:{"set":17,"0":450,"1":647,"2":540,"3":515,"4":370,"5":504},
    17:{"set":18,"0":432,"1":647,"2":540,"3":514,"4":382,"5":504},
    18:{"set":20,"0":610,"1":600,"2":518,"3":516,"4":422,"5":504},
    19:{"set":21,"0":593,"1":591,"2":519,"3":516,"4":390,"5":504},
    20:{"set":22,"0":564,"1":591,"2":519,"3":516,"4":375,"5":504},
    21:{"set":23,"0":545,"1":591,"2":519,"3":515,"4":356,"5":504},
    22:{"set":24,"0":525,"1":579,"2":516,"3":516,"4":376,"5":504},
    23:{"set":25,"0":490,"1":579,"2":516,"3":516,"4":395,"5":504},
    24:{"set":26,"0":467,"1":579,"2":516,"3":515,"4":396,"5":504},
    25:{"set":27,"0":448,"1":579,"2":516,"3":516,"4":414,"5":504},
    26:{"set":28,"0":427,"1":595,"2":516,"3":515,"4":427,"5":504},
    27:{"set":30,"0":618,"1":549,"2":497,"3":515,"4":427,"5":504},
    28:{"set":31,"0":596,"1":549,"2":497,"3":515,"4":400,"5":504},
    29:{"set":32,"0":569,"1":549,"2":496,"3":516,"4":376,"5":504},
    30:{"set":33,"0":548,"1":549,"2":498,"3":515,"4":360,"5":504},
    31:{"set":34,"0":523,"1":549,"2":498,"3":516,"4":360,"5":504},
    32:{"set":35,"0":492,"1":549,"2":498,"3":516,"4":360,"5":504},
    33:{"set":36,"0":467,"1":549,"2":504,"3":515,"4":360,"5":504},
    34:{"set":37,"0":442,"1":549,"2":504,"3":515,"4":376,"5":504},
    35:{"set":38,"0":422,"1":563,"2":505,"3":515,"4":394,"5":504},
    36:{"set":40,"0":624,"1":513,"2":486,"3":515,"4":411,"5":504},
    37:{"set":41,"0":602,"1":513,"2":486,"3":515,"4":377,"5":504},
    38:{"set":42,"0":577,"1":513,"2":486,"3":514,"4":355,"5":504},
    39:{"set":43,"0":550,"1":474,"2":486,"3":516,"4":404,"5":504},
    40:{"set":44,"0":525,"1":474,"2":486,"3":516,"4":390,"5":504},
    41:{"set":45,"0":497,"1":474,"2":486,"3":514,"4":360,"5":504},
    42:{"set":46,"0":465,"1":492,"2":488,"3":515,"4":381,"5":504},
    43:{"set":47,"0":434,"1":492,"2":488,"3":514,"4":402,"5":504},
    44:{"set":48,"0":412,"1":514,"2":488,"3":515,"4":402,"5":504},
    45:{"set":50,"0":634,"1":471,"2":478,"3":515,"4":408,"5":504},
    46:{"set":51,"0":613,"1":471,"2":478,"3":515,"4":381,"5":504},
    47:{"set":52,"0":582,"1":424,"2":479,"3":515,"4":400,"5":504},
    48:{"set":53,"0":552,"1":424,"2":478,"3":516,"4":407,"5":504},
    49:{"set":54,"0":521,"1":424,"2":478,"3":516,"4":370,"5":504},
    50:{"set":55,"0":480,"1":424,"2":478,"3":516,"4":370,"5":504},
    51:{"set":56,"0":450,"1":424,"2":478,"3":516,"4":380,"5":504},
    52:{"set":57,"0":430,"1":442,"2":478,"3":515,"4":421,"5":504},
    53:{"set":58,"0":400,"1":471,"2":479,"3":514,"4":403,"5":504},
    54:{"set":60,"0":649,"1":423,"2":479,"3":515,"4":370,"5":504},
    55:{"set":61,"0":622,"1":423,"2":479,"3":515,"4":350,"5":504},
    56:{"set":62,"0":591,"1":373,"2":480,"3":515,"4":400,"5":504},
    57:{"set":63,"0":559,"1":373,"2":480,"3":515,"4":390,"5":504},
    58:{"set":64,"0":522,"1":373,"2":480,"3":516,"4":390,"5":504},
    59:{"set":65,"0":486,"1":373,"2":480,"3":516,"4":390,"5":504},
    60:{"set":66,"0":445,"1":373,"2":480,"3":515,"4":424,"5":504},
    61:{"set":67,"0":415,"1":373,"2":480,"3":515,"4":447,"5":504},
    62:{"set":68,"0":380,"1":431,"2":479,"3":516,"4":360,"5":504},
    63:{"set":70,"0":665,"1":379,"2":480,"3":516,"4":404,"5":504},
    64:{"set":71,"0":640,"1":339,"2":493,"3":515,"4":403,"5":504},
    65:{"set":72,"0":610,"1":339,"2":493,"3":516,"4":368,"5":504},
    66:{"set":73,"0":570,"1":339,"2":493,"3":515,"4":352,"5":504},
    67:{"set":74,"0":530,"1":339,"2":493,"3":515,"4":340,"5":504},
    68:{"set":75,"0":483,"1":339,"2":493,"3":515,"4":335,"5":504},
    69:{"set":76,"0":440,"1":339,"2":493,"3":515,"4":335,"5":504},
    70:{"set":77,"0":409,"1":339,"2":493,"3":516,"4":380,"5":504},
    71:{"set":78,"0":375,"1":356,"2":493,"3":515,"4":405,"5":504},
    72:{"set":80,"0":685,"1":297,"2":515,"3":514,"4":405,"5":504},
    73:{"set":81,"0":651,"1":256,"2":529,"3":515,"4":375,"5":504},
    74:{"set":82,"0":615,"1":256,"2":529,"3":516,"4":348,"5":504},
    75:{"set":83,"0":575,"1":256,"2":529,"3":514,"4":322,"5":504},
    76:{"set":84,"0":530,"1":256,"2":529,"3":515,"4":314,"5":504},
    77:{"set":85,"0":475,"1":256,"2":529,"3":515,"4":318,"5":504},
    78:{"set":86,"0":434,"1":256,"2":529,"3":515,"4":335,"5":504},
    79:{"set":87,"0":393,"1":256,"2":529,"3":515,"4":378,"5":504},
    80:{"set":88,"0":360,"1":278,"2":524,"3":515,"4":380,"5":504}}



def send(a,b):
    m=int(b*9+a)
#     move={"set":m}
    print(bytes(json.dumps(init[m]),encoding="utf8"))
#     print(bytes(json.dumps(init[move]), encoding="utf8"))
    serial.write(bytes(json.dumps(init[m]), encoding="utf8"))
    print("done!")

if __name__ == '__main__':
    while (1):
        a= int(input("输入x："))
        b= int(input("输入y："))
        send(a,b)


