from flask_restful import Resource
from models.site import SiteModel

class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}

class Site(Resource):
        def get(self, url):
            site = SiteModel.find_sites(url)
            if site:
                return site.json()
            return {'message': 'Site not found.'}, 404 #Not Found

        def post(self, url):
            if SiteModel.find_sites(url):
                return {'message': f"The site '{url}' already exists."}, 400 # bad request
            site = SiteModel(url)
            site.save_site()
            return site.json()
            try:
                site.save_site()
            except:
                return {'message': 'An internal error ocurred trying to create a new site.'}, 500

        def delete(self, url):
            site = SiteModel.find_sites(url)
            if site:
                site.delete_site()
                return {'message': 'Site deleted.'}
            return {'message': 'Site not found.'}, 404
