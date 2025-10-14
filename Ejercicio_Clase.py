from math import sqrt, asin, acos, pi

class Point:
   def __init__(self, x: float, y: float) -> None:
      self._x = x
      self._y = y

class Line(Point):
   def __init__(self, start: Point, end: Point ) -> None:
      super().__init__(start._x, start._y)
      self._start = start
      self._end = end

   def compute_length(self) -> float:
      length = ((self._end._x - self._start._x) ** 2 + (self._end._y - self._start._y) ** 2) ** 0.5
      return length
    
   def compute_slope(self):
      # Vertical line
      if (self._end._x - self._start._x) == 0:
         return None  
      slope: float = (self._end._y - self._start._y) / (self._end._x - self._start._x)
      return slope
    
   def compute_vertical_crossing(self):
      # Intersection with y-axis (x=0)
      slope = self.compute_slope()
      if slope is None:
         return None
      crossing = self._start._y - (slope * self._start._x)  # y = mx + b  =>  b = y - mx
      return crossing

   def compute_horizontal_crossing(self):
      # Intersection with x-axis (y=0)
      slope = self.compute_slope()
      if slope == 0:
         return None  # Horizontal line has no crossing with x-axis
      if slope is None:
         return None  # Vertical line has no crossing with x-axis
      crossing = -(self._start._y - (slope * self._start._x)) / slope  # y = mx + b  =>  x = (y - b) / m
      return crossing
    
   def __str__(self) -> str:
      slope = self.compute_slope()
      slope_str = f"{slope:.2f}"
      v_cross = self.compute_vertical_crossing()
      h_cross = self.compute_horizontal_crossing()
      return (
         f"Length: {self.compute_length():.2f}, "
         f"Slope: {slope_str}, "
         f"Vertical crossing: {v_cross}, "
         f"Horizontal crossing: {h_cross}"
        )

class Shape():
   def __init__(self, is_regular: bool):
      self.is_regular = is_regular
      self.vetices: list = []
      self.edges: list = []
        
   def compute_area(self):
      return 0
    
   def compute_perimeter(self):
      if not self.edges:
            return 0
      else:
         for edge in self.edges:
            perimeter = sum(edge.compute_length() for edge in self.edges)
         return perimeter
    
   def inner_angle(self, sides: int) -> float:
      if sides < 3:
            return 0
      return (sides - 2) * 180 / sides # Average inner angle in degrees
    
   def compute_inner_angles(self):
        sides = len(self.vertices)
        if sides < 3:
            return 0
        return (sides-2) * 180

class Rectangle(Shape):
   def __init__(self, method: int, *args):
      super().__init__(is_regular = False)

      if method == 1:
         # Method 1: Bottom-left + width + height
         bottom_left, width, height = args
         self.width = width
         self.height = height
         self.center = Point(bottom_left._x + width/2, bottom_left._y + height/2)
      elif method == 2:
         # Method 2: Center + width + height
         center, width, height = args
         self.width = width
         self.height = height
         self.center = center
      elif method == 3:
         # Method 3: Two opposite points
         p1, p2 = args
         self.width = abs(p2._x - p1._x)
         self.height = abs(p2._y - p1._y)
         self.center = Point((p1._x + p2._x)/2, (p1._y + p2._y)/2)

      elif method == 4:
         # Method 4: Four lines (composition)
         l1, l2, l3, l4 = args
         lines = [l1, l2, l3, l4]

         points = []
         for line in lines:
            points.append(line._start)
            points.append(line._end)

         xs = []
         ys = []
         for p in points:
            xs.append(p._x)
            ys.append(p._y)

         min_x = min(xs)
         max_x = max(xs)
         min_y = min(ys)
         max_y = max(ys)

         self.width = max_x - min_x
         self.height = max_y - min_y
         self.center = Point((min_x + max_x) / 2, (min_y + max_y) / 2)

      else:
         return "Error: Invalid method"

   def compute_area(self):
         return self.width * self.height

   def compute_perimeter(self):
         return 2 * (self.width + self.height)

   def compute_interference_point(self, point: Point) -> bool:
        x_min = self.center._x - self.width/2
        x_max = self.center._x + self.width/2
        y_min = self.center._y - self.height/2
        y_max = self.center._y + self.height/2
        return x_min <= point._x <= x_max and y_min <= point._y <= y_max

class Square(Rectangle):
      def __init__(self, method: int, *args):
         if method == 1:
            # Method 1: Bottom-left + side
            bottom_left, side = args
            super().__init__(1, bottom_left, side, side)
         elif method == 2:
            # Method 2: Center + side
            center, side = args
            super().__init__(2, center, side, side)
         elif method == 3:
            # Method 3: Two opposite points
            p1, p2 = args
            side = max(abs(p2._x - p1._x), abs(p2._y - p1._y))
            super().__init__(2, Point((p1._x + p2._x) / 2, (p1._y + p2._y) / 2), side, side)
         else:
            raise ValueError("Error: Invalid method")
        
class Triangle(Shape):
      def __init__(self, p1: Point, p2: Point, p3: Point):
        super().__init__(is_regular=False)
        self.vertices = [p1, p2, p3]
        self.edges = [Line(p1, p2), Line(p2, p3), Line(p3, p1)]
        self.center = Point((p1._x + p2._x + p3._x) / 3, (p1._y + p2._y + p3._y) / 3)
      def compute_perimeter(self):
        return super().compute_perimeter()
    
      def compute_area(self):
        a = self.edges[0].compute_length()
        b = self.edges[1].compute_length()
        c = self.edges[2].compute_length()
        s = (a + b + c) / 2  # Semi-perimeter
        area = (s * (s - a) * (s - b) * (s - c)) ** 0.5  # Heron's formula
        return area
    
class IsoscelesTriangle(Triangle):
   def __init__(self, base_point1: Point, base_point2: Point, apex_point: Point):
      self.is_regular = False
      super().__init__(base_point1, base_point2, apex_point)
      if not (self.edges[0].compute_length() == self.edges[1].compute_length() or
               self.edges[1].compute_length() == self.edges[2].compute_length() or
               self.edges[0].compute_length() == self.edges[2].compute_length()):
            raise ValueError("Error: The provided points do not form an isosceles triangle")
    
   def compute_area(self):
      return super().compute_area()
    
   def compute_perimeter(self):
      return super().compute_perimeter()
    
   def compute_inner_angles(self):
      if self.edges[0].compute_length() == self.edges[1].compute_length():
            a = self.edges[0].compute_length()
            b = self.edges[2].compute_length()
      elif self.edges[1].compute_length() == self.edges[2].compute_length():
            a = self.edges[1].compute_length()
            b = self.edges[0].compute_length() 
      else:
            a = self.edges[0].compute_length()
            b = self.edges[1].compute_length()

      test = (b/2)/a
      angle1 = acos(test) * (180 / pi)  # Convert to degrees
      angle2 = angle1
      angle3 = 180 - 2 * angle1
      return angle1, angle2, angle3
    
class Equilateral(Triangle):
   def __init__(self, p_e1: Point, p_e2: Point, p_e3: Point):
      self.is_regular = True
      super().__init__(p_e1, p_e2, p_e3)
    
   def compute_area(self):
      return super().compute_area()
    
   def compute_perimeter(self):
      return super().compute_perimeter()
    
   def compute_inner_angles(self):
      return 60, 60, 60
        
class Scalene(Triangle):
   def __init__(self, p_s1: Point, p_s2: Point, p_s3: Point):
      self.is_regular = False
      super().__init__(p_s1, p_s2, p_s3)
      if (self.edges[0].compute_length() == self.edges[1].compute_length() or
         self.edges[1].compute_length() == self.edges[2].compute_length() or
         self.edges[0].compute_length() == self.edges[2].compute_length()):
         raise ValueError("Error: The provided points do not form a scalene triangle")
    
   def compute_area(self):
      return super().compute_area()
    
   def compute_perimeter(self):
      return super().compute_perimeter()
    
   def compute_inner_angles(self):
      a = self.edges[0].compute_length()
      b = self.edges[1].compute_length()
      c = self.edges[2].compute_length()

      angle1 = acos((b**2 + c**2 - a**2) / (2 * b * c)) * (180 / pi)  # Convert to degrees
      angle2 = acos((a**2 + c**2 - b**2) / (2 * a * c)) * (180 / pi)
      angle3 = 180 - angle1 - angle2
      return angle1, angle2, angle3

if __name__ == "__main__":
   p1 = Point(1, 1)
   p2 = Point(4, 8)
   p3 = Point(5, 4)
   p4 = Point(0, 4)
   base_point1 = Point(0, 0)
   base_point2 = Point(4, 0)
   apex_point = Point(2, 3)
   p_e1 = Point(0, 0)
   p_e2 = Point(4, 0)
   p_e3 = Point(2, (4 * (3 ** 0.5)) / 2)  # Height of equilateral triangle with side 4
   p_s1 = Point(0, 0)
   p_s2 = Point(4, 0)
   p_s3 = Point(3, 5)

   # Create 4 lines that form a rectangle
   l1 = Line(p1, p2)
   l2 = Line(p2, p3)
   l3 = Line(p3, p4)
   l4 = Line(p4, p1)

   print("Test Rectangle")

   # Method 1: Bottom-left + width + height
   rect1 = Rectangle(1, Point(0, 0), 4, 3)
   print("Method 1 -> Area:", rect1.compute_area(), 
      "Perimeter:", rect1.compute_perimeter(), 
      "Center:", (rect1.center._x, rect1.center._y), 
      "inner Angle:", rect1.inner_angle(4))

   # Method 2: Center + width + height
   rect2 = Rectangle(2, Point(2, 1.5), 4, 3)
   print("Method 2 -> Area:", rect2.compute_area(), 
      "Perimeter:", rect2.compute_perimeter(), 
      "Center:", (rect2.center._x, rect2.center._y), 
      "Inner Angle:", rect2.inner_angle(4))

   # Method 3: Two opposite points
   rect3 = Rectangle(3, Point(0, 0), Point(4, 3))
   print("Method 3 -> Area:", rect3.compute_area(), 
      "Perimeter:", rect3.compute_perimeter(), 
      "Center:", (rect3.center._x, rect3.center._y), 
      "inner Angle:", rect3.inner_angle(4))

   # Method 4: Four lines
   rect4 = Rectangle(4, l1, l2, l3, l4)
   print("Method 4 -> Area:", rect4.compute_area(), 
      "Perimeter:", rect4.compute_perimeter(), 
      "Center:", (rect4.center._x, rect4.center._y), 
      "Inner Angle:", rect4.inner_angle(4))

   # Test point interference
   inside = Point(2, 2)
   outside = Point(5, 5)
   print("Point (2,2) inside rect4?", rect4.compute_interference_point(inside))
   print("Point (5,5) inside rect4?", rect4.compute_interference_point(outside))


   print("\nTest Square")

   # Method 1: Bottom-left + side
   sq1 = Square(1, Point(0, 0), 4)
   print("Square Method 1 -> Area:", sq1.compute_area(), 
      "Perimeter:", sq1.compute_perimeter(), 
      "Center:", (sq1.center._x, sq1.center._y),
      "Inner Angle:", sq1.inner_angle(4))

   # Method 2: Center + side
   sq2 = Square(2, Point(2, 2), 4)
   print("Square Method 2 -> Area:", sq2.compute_area(), 
      "Perimeter:", sq2.compute_perimeter(), 
      "Center:", (sq2.center._x, sq2.center._y), 
      "Inner Angle:", sq2.inner_angle(4))

   # Method 3: Two opposite points (will adjust to square)
   sq3 = Square(3, Point(0, 0), Point(4, 2))
   print("Square Method 3 -> Area:", sq3.compute_area(), 
      "Perimeter:", sq3.compute_perimeter(), 
      "Center:", (sq3.center._x, sq3.center._y), 
      "Inner Angle:", sq3.inner_angle(4))


   print("\nTest Isosceles Triangle")
   iso_tri = IsoscelesTriangle(base_point1, base_point2, apex_point)
   print(f"Isosceles Triangle -> Area: {iso_tri.compute_area():.2f} Perimeter: {iso_tri.compute_perimeter():.2f}")
   angles = iso_tri.compute_inner_angles()
   angles_str = ", ".join(f"{angle:.2f}°" for angle in angles)
   print(f"Center: {(iso_tri.center._x, iso_tri.center._y)} Inner Angles: {angles_str}")

   print("\nTest Equilateral Triangle")
   eq_tri = Equilateral(p_e1, p_e2, p_e3)
   print(f"Equilateral Triangle -> Area: {eq_tri.compute_area():.2f} Perimeter: {eq_tri.compute_perimeter():.2f}")
   angles_eq = eq_tri.compute_inner_angles()
   angles_eq_str = ", ".join(f"{angle:.2f}°" for angle in angles_eq)
   print(f"Center: {(eq_tri.center._x, eq_tri.center._y)} Inner Angles: {angles_eq_str}")

   print("\nTest Scalene Triangle")
   scal_tri = Scalene(p_s1, p_s2, p_s3)
   print(f"Scalene Triangle -> Area: {scal_tri.compute_area():.2f} Perimeter: {scal_tri.compute_perimeter():.2f}")
   angles_sc = scal_tri.compute_inner_angles()
   angles_sc_str = ", ".join(f"{angle:.2f}°" for angle in angles_sc)
   print(f"Center: {(scal_tri.center._x, scal_tri.center._y)} Inner Angles: {angles_sc_str}")
