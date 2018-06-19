#!/usr/bin/env python3

import connexion
from swagger_server.utitl.meter_date_insert import meter
from swagger_server.utitl.source_date_insert import source
import multiprocessing


def app_run():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.add_api('swagger.yaml', arguments={'title': '孝感电力系统'})
    app.run(host='0.0.0.0', port=7009)
    # app.run(host='0.0.0.0', port=91)

if __name__ == '__main__':
    p = multiprocessing.Process(target=app_run)
    p.start()
    # app = connexion.App(__name__, specification_dir='./swagger/')
    # app.add_api('swagger.yaml', arguments={'title': '孝感电力系统'})
    # app.run(host='0.0.0.0', port=7002)
    # meter.insert_data()
    source.source_insert_data()

