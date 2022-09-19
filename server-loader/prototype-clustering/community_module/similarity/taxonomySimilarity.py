# Authors: José Ángel Sánchez Martín

import networkx as nx
from community_module.similarity.similarity import Similarity
from community_module.similarity.taxonomies.taxonomy import Taxonomy

class TaxonomySimilarity(Similarity):
    
    def __init__(self, data):
        """Construct of TaxonomySimilarity objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of taxonomy member and
            values contain the number of times that a taxonomy member is in an element.
        """
        super().__init__(data)
        self.taxonomy = Taxonomy(self.data.columns.name)
        
    def getGraph():
        return self.taxonomy.getGraph()

    def elemLayer(self,elem):
        return self.taxonomy.getGraph().nodes[elem]['layer']
    
    def dominantCountry(self, countries, size=1):
        countries = countries.loc[~(countries==0)]
        countries = countries.sort_values(ascending=False).index[:size].values
        return countries
    
    def taxonomySimilarity(self,elemA,elemB):
        """Method to obtain the distance between two taxonomy members.

        Parameters
        ----------
        elemA : object
            Id of first element. This id should be in self.data.
        elemB : object
            Id of second element. This id should be in self.data.

        Returns
        -------
        double
            Similarity between the two taxonomy members.
        """
        commonAncestor = nx.lowest_common_ancestor(self.taxonomy.getGraph(),elemA,elemB)
        return self.elemLayer(commonAncestor) / max(self.elemLayer(elemA), self.elemLayer(elemB))

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
        return 1 - self.similarity(elemA,elemB)

    def similarity(self, elemA, elemB, numElements = 3):
        """Method to obtain the similarity between two element.

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
        countriesA = self.dominantCountry(self.data.loc[elemA], numElements)
        countriesB = self.dominantCountry(self.data.loc[elemB], numElements)
        numElements = min(numElements,countriesA.size,countriesB.size)
        
        distance = 0
        for i in range(numElements):
            distance += self.taxonomySimilarity(countriesA[i], countriesB[i])

        return distance / numElements
    