import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from utils import polygon_intersection
import matplotlib.pyplot as plt

class BoundedVoronoi():
    def __init__(self, points, bounding_polygon):
        
        dummy_poitns = np.array([[-100, -100], [100, -100], [100, 100], [-100, 100]])
        self.points = points
        vor = Voronoi(np.vstack((points, dummy_poitns)))
        self.regions = []
        for i, region in enumerate(vor.point_region[0:-4]):
            new_vor_region = polygon_intersection(vor.vertices[vor.regions[region]],
                                                  bounding_polygon)
            if new_vor_region is not None:
                self.regions.append(new_vor_region)


    def plot(self, axis = None):
      if axis is None:
          for i, region in enumerate(self.regions):
              for ridge in ridges(region):
                  plt.plot(ridge[:,0], ridge[:,1], color = f'C{i}')
              plt.scatter(points[i][0], points[i][1], color = f'C{i}')
              # plt.show()
      else: 
          for i, region in enumerate(self.regions):
              for ridge in ridges(region):
                  axis.plot(ridge[:,0], ridge[:,1], color = f'C{i}')
              axis.scatter(self.points[i][0], self.points[i][1], color = f'C{i}')


if __name__ == '__main__':
# generates distorted pentagon
    bounding_polygon = np.array([[-1, -1], [1, -1], [1.2, 1], [0, 1.2], [-1.2, 1]])+0.5+np.random.rand(5,2)*0.4

    # n random points 
    n = 5
    points = np.random.rand(5,2)

    vor = BoundedVoronoi(points, bounding_polygon)
    vor.plot()
    plt.show()
