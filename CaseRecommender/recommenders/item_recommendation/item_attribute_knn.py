# coding=utf-8
"""
© 2016. Case Recommender All Rights Reserved (License GPL3)

Item Based Collaborative Filtering Recommender with Attributes

    Its philosophy is as follows: in order to determine the rating of User u on Movie m, we can find other movies that
    are similar to Movie m, and based on User u’s ratings on those similar movies we infer his rating on Movie m.
    However, instead of traditional ItemKNN, this approach uses a pre-computed similarity matrix.

    Literature:
        http://cs229.stanford.edu/proj2008/Wen-RecommendationSystemBasedOnCollaborativeFiltering.pdf

Parameters
-----------
    - train_file: string
    - test_file: string
    - ranking_file: string
        file to write final ranking
    - similarity_matrix_file: file
        Pairwise metric to compute the similarity between the users based on a set of attributes.
        Format file:
        Distances separated by \t, where the users should be ordering. E g.:
        distance1\tdistance2\tdistance3\n
        distance1\tdistance2\tdistance3\n
        distance1\tdistance2\tdistance3\n
    - neighbors: int
        The number of user candidates strategy that you can choose for selecting the possible items to recommend.
"""
from CaseRecommender.recommenders.item_recommendation.itemknn import ItemKNN
from CaseRecommender.utils.extra_functions import timed
from CaseRecommender.utils.read_file import ReadFile

__author__ = "Arthur Fortes"


class ItemAttributeKNN(ItemKNN):
    def __init__(self, train_file, similarity_matrix_file, test_file=None, ranking_file=None, neighbors=30):
        ItemKNN.__init__(self, train_file, test_file=test_file, ranking_file=ranking_file, neighbors=neighbors)
        self.similarity_matrix_file = similarity_matrix_file

    def read_matrix(self):
        self.si_matrix = ReadFile(self.similarity_matrix_file).read_matrix()

    def execute(self):
        print("[Case Recommender: Item Recommendation > Item Attribute KNN Algorithm]\n")
        print("training data:: " + str(len(self.train_set["map_user"])) + " users and " + str(len(
            self.train_set["map_item"])) + " items and " + str(self.train_set["number_interactions"]) + " interactions")
        if self.test_file is not None:
            test_set = ReadFile(self.test_file).return_matrix()
            print("test data:: " + str(len(test_set["map_user"])) + " users and " + str(len(test_set["map_item"])) +
                  " items and " + str(test_set["number_interactions"]) + " interactions")
            del test_set
        print("training time:: " + str(timed(self.read_matrix))) + " sec"
        print("prediction_time:: " + str(timed(self.predict))) + " sec\n"
        if self.test_file is not None:
            self.evaluate()
