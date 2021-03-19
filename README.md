# EPF-RUDN-Alpacas-Project
This project allows to know where is the best place to breed alpacas in Europe

This project developed for the Geospatial Programming class of beginning of of 2021, an international collaboration between two universities, EPF of France (https://www.epf.fr/ ) and RUDN of Russia (http://www.rudn.ru).
We are Hugo and Manon, two engineering students at the EPF and we made this program under the supervision of Naci Dilekli (https://github.com/ndilekli/). 
Our project aims to determine the best areas in Europe to set up an alpaca farm. To do this we take into account the living conditions necessary for alpacas such as temperature, presence of grass, altitude. Then the user can enter the importance of other criteria such as the price of the land, the amount of rainfall and the amount of population present.
Here you can see the workflow which illustrate how we proceeded with the analysis : 
![Work FlowChart](https://github.com/Hugorudn/EPF-RUDN-Alpacas-Project/tree/main/Image/Image5.png)

And here how work our ![Code](https://github.com/Hugorudn/EPF-RUDN-Alpacas-Project/tree/main/Image/Image2.png)
 
The project is useful for anyone looking for a place to keep alapagas in Europe
To run the code the module arcpy must be installed. Therefore, ArcGIS should probably be installed on your computer if you want see the results. Furthermore, you shall run Jupyter notebook from ArcGIS directory to access arcpy.
When you have downloaded the file, open the .py file in your Jupyter notebook and run the different functions. Before executing the last function, be sure to change the path to the one where you downloaded all the files. Be careful to use "/" to delimit your path and not "\".
When you run the last function, you will need to enter the importance of your criteria. Enter a number between 0 and 1. 
When the function has finished running (it may take more than 10 minutes the first time), the name of your file containing the results will be shown. You can then launch ArcGIS PRO, create a path to the folder where you downloaded your files. You will see all your data displayed. Open the file Final_results, where you will find the files containing the results maps. Just right click on them and add them to your map. 
For exemple you can see here an exemple of result. 
![Map between 0 and 100](https://github.com/Hugorudn/EPF-RUDN-Alpacas-Project/tree/main/Image/Image3.png)
![Map between 70 and 100](https://github.com/Hugorudn/EPF-RUDN-Alpacas-Project/tree/main/Image/Image4.png)
More the points are red more suitable the place is. 

The data for the minimum and the maximum temperature are there (2.5min): https://www.worldclim.org/data/worldclim21.html
If you are any issues or question feel free to contact us: manon.salles@epfedu.fr hugo.chevalier@epfedu.fr 
