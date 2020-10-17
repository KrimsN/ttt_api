from serializers.serializer_factory import SerializerFactory, SerializerTypes as ST
from parsers.parser_factory import ParserFactory, ParserTypes as PT

from datetime import datetime
from pprint import pprint


from flask import Flask
from flask_restful import Resource, Api

ttt_app = Flask(__name__)
ttt_api = Api(ttt_app)


class TTT(Resource):
    def __init__(self):
        pf = ParserFactory()
        self.parser = pf.createParser(PT.TTT)
        self.ser = SerializerFactory().create(ST.JSON)

    def get(self, nFac, nGroup, date):
        day = datetime.strptime(date, '%d-%m-%y')
        week_num = self.parser.get_week_num(day)
        url = self.parser.create_url_link(nGroup, nFac, week_num)
        self.parser.parse(url)

        result = self.parser.serialize(self.ser)
        self.parser.clear_cash()
        self.ser.clear_cash()
        response = ttt_app.response_class(
            response=result,
            status=200,
            mimetype='application/json'
        )
        return response

class Ping(Resource):

    def get(self):
        return 'pong', 200

def old_main():
    import sys
    sys.path.append("..")

    pf = ParserFactory()    
    parser = pf.createParser(PT.TTT)
    week_num = parser.get_week_num(datetime.now())
    url = parser.create_url_link( '437-2','fsu', week_num)
    # print(url)
    parser.parse(url)


    sf = SerializerFactory()
    ser = sf.create(ST.XML)

    with open('out/1.xml', 'w') as f:
        parser.serialize_dump(ser, f)
    
    parser.parse(url)
    ser = sf.create(ST.JSON)

    
    with open('out/1.json', 'w') as f:
        parser.serialize_dump(ser, f)

ttt_api.add_resource(TTT, '/<string:nFac>/<string:nGroup>/<string:date>')
ttt_api.add_resource(Ping, '/ping')

if __name__ == "__main__":
    # old_main()
    ttt_app.run(debug=True)

