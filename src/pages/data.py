from base import BasePage
from django.utils import simplejson
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from model import DeviceCountries, DeviceCarriers, DeviceVersions, \
    UnknownVersions
import re

class CarrierPage(BasePage):
    def json(self):
        json = simplejson.dumps(DeviceCarriers.generateGraphData())
        self.response.out.write(json)

    def html(self):
        self.render({
            'carrier_data_len': len(DeviceCarriers.generateGraphData()),
            'carrier_data': DeviceCarriers.generateGraphData()
        })

    def get(self):
        match = re.match(r"^/data/carriers\.(json|html)$", self.request.path)
        if match:
            if match.groups()[0] == 'json':
                self.json()
            elif match.groups()[0] == 'html':
                self.html()
        else:
            self.html()

class CountryPage(BasePage):
    def json(self):
        json = simplejson.dumps(DeviceCountries.generateGraphData())
        self.response.out.write(json)

    def html(self):
        self.render({
            'country_data': DeviceCountries.generateGraphData()
        })

    def get(self):
        match = re.match(r"^/data/countries\.(json|html)$", self.request.path)
        if match:
            if match.groups()[0] == 'json':
                self.json()
            elif match.groups()[0] == 'html':
                self.html()
        else:
            self.html()

class VersionPage(BasePage):
    def json(self):
        json = simplejson.dumps(DeviceVersions.generateGraphData())
        self.response.out.write(json)

    def html(self):
        self.render({
            'version_data': DeviceVersions.generateGraphData(),
            'unknown_version_data': UnknownVersions.generateGraphData(),
            'version_table_data': DeviceVersions.generateGraphData() + UnknownVersions.generateGraphData(),
        })

    def get(self):
        match = re.match(r"^/data/versions\.(json|html)$", self.request.path)
        if match:
            if match.groups()[0] == 'json':
                self.json()
            elif match.groups()[0] == 'html':
                self.html()
        else:
            self.html()

application = webapp.WSGIApplication(
        [('/data/carriers.*', CarrierPage),
         ('/data/countries.*', CountryPage),
         ('/data/versions.*', VersionPage)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
