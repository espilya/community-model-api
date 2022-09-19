#   José Ángel Sánchez Martín

from itertools import product
import numpy as np

from community_module.similarity.similarity import Similarity


"""
Similarity between users based on collected/interacted artwork's similarity
"""

class UserArtworkSimilarity(Similarity):
    """Class to define the functions to be implemented to calculate
    the similarity between elements.
    """
    
    def __init__(self,data,artworkDistanceMatrix):
        """Construct of Similarity objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements (column: user, column: artwork)
        
        """
        self.data = data
        self.artworkDistanceMatrix = artworkDistanceMatrix
    
    def interactedArtworks(self, artworks):
        artworks = artworks.loc[~(artworks==0)].index
        #artworks = artworks.sort_values(ascending=False).index  #.index[:size].values
        return artworks
        
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
        
        artworksA = self.interactedArtworks(self.data.loc[elemA])
        artworksB = self.interactedArtworks(self.data.loc[elemB])
        
        print(artworksA)
        print(artworksB)
        
        
        # Gets pairs between artworksA, artworksB
        # Ex: artworkA (1); artworkB (1) |  artworkA (1); artworkB (2) | artworkA (1); artworkB (n)
        pairs = product(artworksA,artworksB)
        # Divide by the number of pairs
        distance = 0
        numberPairs = 0
        for p in pairs:
            # columns is type: pandas index object
            index0 = self.data.columns.get_loc(p[0])
            index1 = self.data.columns.get_loc(p[1])
            
            print(p[0])
            print(str(index0))
            print("distance: " + str(self.artworkDistanceMatrix[index0][index1]))
            distance += self.artworkDistanceMatrix[index0][index1]
            numberPairs += 1
        
        # Divide by the number of pairs
        distance = distance / (max(numberPairs,0))
        
        return distance

        


       # print(artworksA)
        #print(artworksB)
        
        """
        for p in pairs:
            print(p)

            
            print("\n")
            print(p[0])
            print(p[1])
            print("\n")
            
        
        print("\n\n")
        """


    
    