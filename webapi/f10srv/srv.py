#!/usr/bin/env python

import sphinxapi
from flask import Flask
from flask import request
from flask import Response
import json
import ctypes
import zlib
import config

app = Flask(__name__)


@app.route('/search', methods=['GET'])
def search():
    keyword  = request.args.get('keyword', '')
    category = request.args.get('category', '')
    if len(keyword) == 0:
        retdata = {'message': "Less keyword!"}
    else:
        retdata = matchRecords(keyword, category)
    return Response(json.dumps(retdata), mimetype='application/json')


def matchRecords(keyword, category=''):
    spc = sphinxapi.SphinxClient()
    spc.SetServer(config.sphinx_host, config.sphinx_port)
    spc.SetMatchMode(sphinxapi.SPH_MATCH_ALL)
    spc.SetLimits(0, 30000, 30000, 0)
    if category != '':
        assert (type(category) is unicode)
        spc.SetFilter('ctgry_crc', [CRC32(category.encode('utf-8'))])

    spc.SetGroupBy('stockcode', sphinxapi.SPH_GROUPBY_ATTR)
    res = spc.Query(keyword)
    costtime = '{} secs'.format(res['time'])
    codes = [i['attrs']['stockcode'] for i in res['matches']]
    return {'messages': 'Success', 'costtime': costtime, 'matches': codes}


def CRC32(inputStr):
    return ctypes.c_uint32(zlib.crc32(inputStr)).value


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.srv_port, threaded=True)
