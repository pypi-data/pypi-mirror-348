--- data/input/sample1.py	2025-05-08 10:08:35
+++ data/input/sample1_modified1.py	2025-05-08 10:09:21
@@ -24,12 +24,26 @@
     """
     return a - b
 
+def calculate_product(a, b):
+    """
+    Calculate the product of two numbers.
+    
+    Args:
+        a: First number
+        b: Second number
+        
+    Returns:
+        Product of a and b
+    """
+    return a * b
+
 def main():
     x = 10
     y = 5
     
     print(f"Sum of {x} and {y} is {calculate_sum(x, y)}")
     print(f"Difference between {x} and {y} is {calculate_difference(x, y)}")
+    print(f"Product of {x} and {y} is {calculate_product(x, y)}")
 
 if __name__ == "__main__":
     main()
