import rasterio
from flask import Flask, request
from geomet import wkt

cords = [[160, 55],] 
elevation = 'srtm_N55E160.tif'

app = Flask (__name__)

@app.route('/elevation')
def query_example():
    wkt_req = request.args.get('WKT')
    print(wkt_req)
    ls = wkt.loads(wkt_req)
    print(ls)
    cords = []
    if ls['type'] == 'LineString':
        for i in range (len(ls['coordinates'])):
            if len(ls['coordinates'][i]) == 2:
                point = ls['coordinates'][i]
                if 160 <= point[0] <= 161 and 55 <= point[1] <= 56:    
                    buff = [[0,0],]
                    buff[0][0],buff[0][1] = point[0],point[1]
                    with rasterio.open(elevation) as src:
                        heigh, = src.sample(buff)
                    point.append(heigh[0])
                
                    cords.append(point)
                else:
                     return '<h1>Введенные координаты выходят за пределы рабочей области программы <h1>'
            else:
                return '<h1>Данные введены с ошибкой <h1>'    
        return '<h1>Полученные координаты точек: {}<h1>'.format(cords)
            
            

    elif ls['type'] == 'Point':
        if len(ls['coordinates']) == 2:    
            point = ls['coordinates']
            if 160 <= point[0] <= 161 and 55 <= point[1] <= 56:
                buff = [[0,0],]
                buff[0][0],buff[0][1] = point[0],point[1]
                with rasterio.open(elevation) as src:
                    heigh, = src.sample(buff)
                point.append(heigh[0])
            else:
                     return '<h1>Введенные координаты выходят за пределы рабочей области программы <h1>'
            return '<h1>Координаты полученной точки: {} <h1>'.format(point)
        else:
            return '<h1>Точка указана неверно  <h1>'  
   
@app.route('/')

def hello():

    return '<h1>Введите в адрес координаты точки в формате POINT(x y) или несколько точек в формате LINESTRING(x y, x y, x y...)  <h1>'  

if __name__ == '__main__':
    app.run(debug=True)
