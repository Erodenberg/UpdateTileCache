<<<<<<< HEAD
This sample provides an example of how to enable feature class change detection and use the results to update tiles in cache based only on changes. This will allow caches to be updated quickly without rebuilding the entire cache, which is time consuming, and resource intensive. At the ArcGIS 10.2 release, this model has works with one of two geoprocessing tools. [Compare two feature classes in a file Geodatabase](http://esristl.maps.arcgis.com/home/item.html?id=23651608afe1405cad4a22eba6d86a8e) or [Show Edits since Reconcile Geoprocessing Tool](http://www.arcgis.com/home/item.html?id=b75fc9edf166438c82d66f4982e4e031). Compare two feature classes in a file geodatabase will create a feature class of changes features based on geometry and or attributes that have changed since the last update. The Show Edits since Reconcile geoprocessing tool generates a feature class of all the edits for a single feature class between versions in a multi-user geodatabase. Both tools can be used in this workflow to rebuild areas of a map cache where the underlying features have been edited.

===============
UpdateTileCache
===============

This sample provides an example of how to enable feature class change detection and use the results to 
update tiles in cache based only on changes. This will allow caches to be updated quickly without 
rebuilding the entire cache, which is time consuming, and resource intensive. At the ArcGIS 10.2 
release, this model has works with one of two geoprocessing tools. Compare two feature classes in a 
file geodatabase or Show Edits since Reconcile Geoprocessing Tool. Compare two feature classes in a 
file geodatabase will create a feature class of changes features based on geometry and or attributes that 
have changed since the last update. The Show Edits since Reconcile geoprocessing tool generates a 
feature class of all the edits for a single feature class between versions in a multi-user geodatabase. 
Both tools can be used in this workflow to rebuild areas of a map cache where the underlying features 
have been edited. 
This sample was written to provide a business partner with the ability to accept a Shapefile or 
Geodatabase Feature Class uploaded over the internet or FTP to a directory. The new Shapefile or 
Geodatabase Feature Class is copied to a file geodatabase or SDE Geodatabase where it is compared to 
the old feature class. The output changes feature are then buffered by 2500 feet. This will insure that 
he changes are picked up by all scale levels within the Cache Map service and all tiles are correctly 
updated. This distance can be modified higher or lower based on user testing. Once the buffered 
feature class is created this tool stops the map service of the cache that needs to be updated and 
overwrites the published feature class and the “old” feature class as well. This ensures that the 
published feature class has the latest attributes and the tiles are updated correctly. Additionally the tool 
copies the “new” feature class as the “old” so the model is ready to run the next time the new updates 
are uploaded. Finally, the service is restarted and the cache tile buffer is passed into the Manage Map 
Server Cache Tiles. This force the Cache to only be updated where underlying features have changed. 
***Install Note*** 
This download includes sample data so you can see how the workflow needs to be configured before 
you wire up and connect your own data. 
>>>>>>> e70ebafbb47cd8d9609c2f297ffaa5dd6c8a71fe
