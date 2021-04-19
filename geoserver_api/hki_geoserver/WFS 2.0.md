# WFS 2.0 with owslib
For Web Feature Service, owslib is used.

However, in WFS 2.0 implementation there is a bug preventing filtering from working.
Until filtering in owslib is improved, a manual fix needs to be made `owslib/feature/__init__.py`.

Diff:
```diff
--- owslib/feature/__init__.py-orig     2020-11-27 14:14:05.374027100 +0200
+++ owslib/feature/__init__.py  2020-11-30 16:16:42.864930900 +0200
@@ -173,7 +173,10 @@
         elif bbox:
             request["bbox"] = self.getBBOXKVP(bbox, typename)
         elif filter:
-            request["query"] = str(filter)
+            if self.version == '2.0.0':
+                request["filter"] = str(filter)
+            else:
+                request["query"] = str(filter)
         if typename:
             typename = (
                 [typename] if isinstance(typename, str) else typename
```