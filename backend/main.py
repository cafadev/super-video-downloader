from flask import Flask, Response, request
from flask_restful import Resource, Api
from flask_cors import CORS
import json
import downloader

app = Flask(__name__)
CORS(app)
api = Api(app)

class Download(Resource):

    def ranking(self, response):
        """
        Update and return ranking downloads list
        Args:
            response (dict): Dictionary with video information

        Returns:
            list: updated ranking list

        """

        with open('./ranking.json', 'r') as ranking_file:
            # Decode json file
            rank = json.load(ranking_file)

            # To detect if list was updated
            change = False

            # New item to positionate in the ranking list
            b = {'title': response['title'], 'position': 'up'}

            if len(rank) > 1:
                for (index, item) in enumerate(rank):

                    if (item['title'] == response['title']) and index == 0:
                        change = True
                        break
                        
                    elif item['title'] == response['title']:
                        d = rank[0:index]
                        
                        c = rank[index:]
                        d[-1]['position'] = 'down'

                        d[-1], c[0] = b, d[-1]
                        rank = d + c
                        change = True
                        break

            if not change:
                if len(rank) < 10:
                    rank.append(b)
                else:
                    rank[-1] = b

            ranking_file.close()

        json.dump(rank, open('./ranking.json', 'w'))
        return rank

    def get(self):
        url = request.args.get('url')
        response = downloader.get_urls(url)
        response['ranking'] = self.ranking(response)

        response = json.dumps(response)
        return response


class Ranking(Resource):

    def get(self):
        return open('./ranking.json', 'r').read()

api.add_resource(Download, '/api/v1/download')
api.add_resource(Ranking, '/api/v1/ranking')

if __name__ == '__main__':
    app.run(debug=True)
