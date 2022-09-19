# Authors: José Ángel Sánchez Martín

from community_module.similarity.similarity import Similarity

class ComplexSimilarity(Similarity):

    def __init__(self, data,similarityDict):
        """Construct of EmotionSimilarity objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of similarity features of that element and
            values contain the value for that similarity feature.
            
            e.g. (artworks): country, material, dominant color
            e.g. (users): genre, nationality, age
            e.g. (users-artworks): opinion, emotion...
        
        similarityDict: dictionary
            key: similarityMeasure class.
                e.g:  genreSimilarity, nationalitySimilarity, ageSimilarity
            value: weight assigned to the similarity measure. Combined they total 1
        """
        self.data = data
        self.similarityDict = similarityDict
        #print(self.data)
        
    def distance(self,elemA, elemB):
        """Method to obtain the distance between two element.

        Parameters
        ----------
        elemA : int
            Id of first element. This id should be in self.data.
        elemB : int
            Id of second element. This id should be in self.data.

        Returns
        -------
        double
            Distance between the two elements.
        """
        complexSimilarityDistance = 0
        for key,value in self.similarityDict.items():
            elemSimilarityDistance = key(self.data).distance(elemA,elemB) * value
            complexSimilarityDistance += elemSimilarityDistance
        
        complexSimilarityDistance = complexSimilarityDistance / len(self.similarityDict)
        
        return complexSimilarityDistance
    
