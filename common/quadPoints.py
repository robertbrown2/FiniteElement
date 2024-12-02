from math import sqrt
class quadPoints:

  def __init__(self, geom='triangle', precision=2):
    '''
    Creates and stores the quadrature points and weights for a given quadrature.
    Contains the following attributes:
      points - list of lists: 
        [[x1, y1],
         [x2, y2],
         ...,
         [xN, yN]]
      weights - list:
         [w1, w2, ... wN]
      order - number of points in the list (integer)
      precision - accuracy of method (integer)
      
    Triangle References:

    Jarle Berntsen, Terje Espelid,
    Algorithm 706, ACM Transactions on Mathematical Software,
    Volume 18, Number 3, September 1992, pages 329-342.

    Elise deDoncker, Ian Robinson,
    Algorithm 612, ACM Transactions on Mathematical Software,
    Volume 10, Number 1, March 1984, pages 17-22.

    Dirk Laurie,
    Algorithm 584, ACM Transactions on Mathematical Software,
    Volume 8, Number 2, 1982, pages 210-218.

    Gilbert Strang, George Fix,
    An Analysis of the Finite Element Method,
    Cambridge, 1973,
    ISBN: 096140888X,
    LC: TA335.S77.

    Olgierd Zienkiewicz,
    The Finite Element Method,
    Sixth Edition,
    Butterworth-Heinemann, 2005,
    ISBN: 0750663200,
    LC: TA640.2.Z54
    
    Line/Quad References:
    Wikipedia: "Gaussian Quadrature"
    '''

    # Triangle quadrature
    if geom == 'triangle':
      if precision == 1:
        # from Zienkiewicz (1)
        self.points = [[1/3, 1/3]]
        self.weights = [1]
        self.order = 1
      elif precision == 2:
        # from Zienkiewicz (2)
        self.points = [[.5, 0], [0, .5], [.5, .5]]
        self.weights = [1/3, 1/3, 1/3]
        self.order = 3
      elif precision == 3:
        # from Zienkiewicz (3)
        self.points = [ [1/3, 1/3], 
                        [3/5, 1/5], [1/5, 3/5], [1/5, 1/5]]
        self.weights = [-27/48, 25/48, 25/48, 25/48]
        self.order = 4
      elif precision == 4:
        # Strang and Fix (5)
        
        a = 0.816847572980459
        b = 0.091576213509771
        c = 0.108103018168070
        d = 0.445948490915965
        v = 0.109951743655322
        w = 0.223381589678011
        
        self.points = [[a, b], [b, a], [b, b],
                       [c, d], [d, c], [d, d]]
        self.weights = [v, v, v, w, w, w]
        self.order = 6
      elif precision == 5:
        # from Zienkiewicz (4)
        
        a = 1 / 3
        b = (9 + 2*sqrt(15)) / 21
        c = (6 -   sqrt(15)) / 21
        d = (9 - 2*sqrt(15)) / 21
        e = (6 +   sqrt(15)) / 21
        u = 0.225
        v = (155 - sqrt(15)) / 1200
        w = (155 + sqrt(15)) / 1200

        self.points = [[a, a],
                       [b, c], [c, b], [c, c],
                       [d, e], [e, d], [e, e]]
        self.weights = [u, v, v, v, w, w, w]
        self.order = 7
      elif precision == 6:
        # Strang and Fix (8)
        a = 0.124949503233232
        b = 0.437525248383384
        c = 0.797112651860071
        d = 0.165409927389841
        e = 0.037477420750088

        u = 0.205950504760887
        v = 0.063691414286223

        self.points = [[a, b], [b, a], [b, b],
                       [c, d], [c, e], [d, c], [d, e], [e, c], [e, d]]
        self.weights = [u, u, u, v, v, v, v, v, v]
        self.order = 9
      elif precision == 7:
        # Strang and Fix (10)
        h = 1 / 3
        a = 0.479308067841923
        b = 0.260345966079038
        c = 0.869739794195568
        d = 0.065130102902216
        e = 0.638444188569809
        f = 0.312865496004875
        g = 0.048690315425316

        w = -0.149570044467670
        t =  0.175615257433204
        u =  0.053347235608839
        v =  0.077113760890257

        self.points = [[h, h],
                       [a, b], [b, a], [b, b],
                       [c, d], [d, c], [d, d],
                       [e, f], [e, g], [f, e], [f, g], [g, e], [g, f]]
        self.weights = [w, t, t, t, u, u, u, v, v, v, v, v, v]
        self.order = 13
      #elif precision == 8:
      #  # from CUBTRI ACM TOMS 584
      #  self.points = 
      #  self.weights = 
      #  self.order = 19
      #elif precision == 9:
      #  # from TRIEX ACM TOMS 612
      #  self.points = 
      #  self.weights = 
      #  self.order = 19
      #elif precision == 11:
      #  # from TRIEX ACM TOMS 612
      #  self.points = 
      #  self.weights = 
      #  self.order = 28
      #elif precision == 13:
      #  # from ACM TOMS 706
      #  self.points = 
      #  self.weights = 
      #  self.order = 37
      else:
        raise Exception('Error in quadPoints: precision not supported for triangle geometry.')
    elif geom == 'quad':
      raise Exception('Error in quadPoints: precision not supported for quad geometry.')
    elif geom == 'line':
      if precision == 1:
        self.points = [0.5]
        self.weights = [1]
        self.order = 1
      elif precision == 3:
        a = 0.5/sqrt(3)
        self.points = [0.5 - a, 0.5 + a]
        self.weights = [0.5, 0.5]
        self.order = 2
      elif precision == 5:
        a = 0.5*(1 - sqrt(3/5))
        b = 0.5*(1 + sqrt(3/5))
        v = 4/9
        w = 5/18
        
        self.points = [a, 0.5, b]
        self.weights = [w, v, w]
      elif precision == 7:
        a = 0.5*sqrt(3/7 - 2/7*sqrt(6/5))
        b = 0.5*sqrt(3/7 + 2/7*sqrt(6/5))
        w = (18 + sqrt(30))/72
        v = (18 - sqrt(30))/72
        self.points = [0.5 - b, 0.5 - a, 0.5 + a, 0.5 + b]
        self.weights = [v, w, w, v]
      elif precision == 9:
        a = 1/6 * sqrt(5 - 2*sqrt(10/7))
        b = 1/6 * sqrt(5 + 2*sqrt(10/7))
        w = 128 / 450
        v = (322 + 13*sqrt(70))/1800
        u = (322 - 13*sqrt(70))/1800
        self.points = [0.5 - b, 0.5 - a, 0.5, 0.5 + a, 0.5 + b]
        self.weights = [u, v, w, v, u]
      else:
        raise Exception('Error in quadPoints: precision not supported for line geometry (only odd).')