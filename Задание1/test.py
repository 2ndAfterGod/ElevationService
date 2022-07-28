import rasterio
from flask import Flask, request

point = [[160, 55.],] 
elevation = 'srtm_N55E160.tif'

app = Flask (__name__)

@app.route('/elevation')
def query_example():
    
    x = float(request.args.get('x'))
    y = float(request.args.get('y'))
    point[0][0],point[0][1]= x,y

    with rasterio.open(elevation) as src:
        z, = src.sample(point)

    return '''<h1> Полученая точка ({}, {}, {})</h1>'''.format(x,y,z[0])

@app.route('/')

def hello():
    return '<h1>Введите в адрес координаты точки<h1>'  

if __name__ == '__main__':
    app.run(debug=True)
