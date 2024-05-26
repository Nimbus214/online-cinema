from concurrent import futures
import random
import json

import grpc

from cinema_library_pb2 import (
    FilmGenre,
    Film,
    RecommendationResponse,
)

import cinema_library_pb2_grpc


class RecommendationService(cinema_library_pb2_grpc.RecommendationsServicer):

    def Recommend(self, request, context):
        if request.category == FilmGenre.ALL:
            return RecommendationResponse(recommendations=FILMS)
        films_for_category = []
        for film in FILMS:
            if request.category in film.categoryes:
                films_for_category.append(film)
        films_to_recommend = random.sample(films_for_category)

        return RecommendationResponse(recommendations=films_to_recommend)
    
    def GetFilm(self, request, context):
        for film in FILMS:
            if film['id'] == request.id:
                return Film(
                    id=film['id'], 
                    title=film['title'],
                    categoryes=film['categoryes'],
                    small_description=film['small_description'],
                    description=film['description']
                )
        context.abort(grpc.StatusCode.NOT_FOUND, "Film not found")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cinema_library_pb2_grpc.add_RecommendationsServicer_to_server(RecommendationService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    with open("data/films.json") as file:
        FILMS = json.load(file)
    serve()
