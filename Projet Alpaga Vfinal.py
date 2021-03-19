#!/usr/bin/env python
# coding: utf-8

# In[1]:


import arcpy


# In[7]:


# Create a new file
def New_file(root,rgdb):
    root = root
    rgdb = rgdb
    raster_gdb = root + "/"+ rgdb
    if arcpy.Exists(raster_gdb):
        arcpy.Delete_management(raster_gdb)
        arcpy.CreateFileGDB_management(root, rgdb)
    else : 
        arcpy.CreateFileGDB_management(root, rgdb)
    return raster_gdb 


# In[8]:


# Transform .tif in raster with specific name 
def TransformTif_raster(current_env,name_tif,output_env) : 
    arcpy.env.workspace = current_env
    name_raster = name_tif +".tif"
    raster = arcpy.Raster(name_raster)
    arcpy.env.workspace = output_env
    name_1 =output_env +"/"+name_tif 
    raster_name =  name_1
    raster.save(raster_name)


# In[9]:


# Extract data on a raster in a specific aera
def Extract_by_Mask(current_env,name_raster,name_mask,output_env):
    arcpy.env.workspace = current_env
    raster = arcpy.Raster(name_raster)
    outExtractByMask = arcpy.sa.ExtractByMask(raster, name_mask)
    name_output = output_env +"/"+name_raster +"_Europe"
    outExtractByMask.save(name_output)


# In[16]:


# Main function
def AlpacaRegion(path) :
    import arcpy
    # Permit to the user to inter his criteria importance
    a = float(input("Enter the level of importance you want for the precipitation (between 0 and 1) : "))
    b = float(input("Enter the level of importance you want for the GPD (between 0 and 1) : "))
    c = float(input("Enter the level of importance you want for the density (between 0 and 1) : "))
    # See if rasters are already create
    arcpy.env.workspace = path + "/outraster_project_Final_Result.gdb"
    print(arcpy.Exists(arcpy.env.workspace))
    if not arcpy.Exists(arcpy.env.workspace) : 
        # Part one
        # Fist step map temperature min 
        arcpy.env.workspace = path + "/Min Temperature"
        root = path 
        rgdb = "outraster_project_temp.gdb"
        raster_gdb = New_file(root,rgdb)
        arcpy.env.workspace = path + "/Min Temperature"
        # Get and print a list of .tif from the workspace
        map_temp = arcpy.ListRasters("*", "TIF")
        i=1
        # Convert .tif in raster
        for raster in map_temp:
            raster = arcpy.Raster(raster)
            name_1 = "/map_raster" + str(i)
            raster_name = raster_gdb + name_1
            raster.save(raster_name)
            i+=1
        arcpy.env.workspace = path + "/outraster_project_temp.gdb"
        rasters = arcpy.ListRasters("*", "GRID")
        for raster in rasters:
            raster
        minraster = raster
        i=1
        for raster in rasters:
            name_raster = "map_raster" + str(i)
            if(raster==name_raster):
                raster = arcpy.Raster(raster)
                minraster = arcpy.sa.Con(raster<minraster, raster, minraster)
                name_2 = "/min_temp_" + str(i)
                minraster = arcpy.Raster(minraster)
                raster_min_name = raster_gdb + name_2
                minraster.save(raster_min_name)
                i+=1
        #map temperature max 
        arcpy.env.workspace = path + "/Max Temperature"
        map_temp = arcpy.ListRasters("*", "TIF")
        i=1
        for raster in map_temp:
            raster = arcpy.Raster(raster)
            name_1 = "/map_raster_max" + str(i)
            raster_name = raster_gdb + name_1
            raster.save(raster_name)
            i+=1
        arcpy.env.workspace = path + "/outraster_project_temp.gdb"
        rasters = arcpy.ListRasters("*", "GRID")
        for raster in rasters:
            raster
        maxraster = raster
        i=1
        for raster in rasters:
            name_raster = "map_raster_max" + str(i)
            if(raster==name_raster):
                i+=1
        maxraster = raster
        i=1
        for raster in rasters:
            name_raster = "map_raster_max" + str(i)
            if(raster==name_raster):
                raster = arcpy.Raster(raster)
                maxraster = arcpy.sa.Con(raster>maxraster , raster, maxraster )
                name_3 = "/max_temp_" + str(i)
                raster_max_name = raster_gdb + name_3
                maxraster.save(raster_max_name)
                i+=1
        # Create a binary map for the temperature max and min
        arcpy.env.workspace = path + "/outraster_project_temp.gdb"
        raster1 = arcpy.Raster("max_temp_12")
        raster2 = arcpy.Raster("min_temp_12")
        raster_temp_final_max = arcpy.sa.Con(raster1<30,1,2)
        raster_temp_final_min = arcpy.sa.Con(raster2>-15,1,0)
        somme_raster = raster_temp_final_max + raster_temp_final_min
        raster_final_temp = arcpy.sa.Con(somme_raster==2,1,0)
        name_4 = "/temp_final" 
        raster_fianl_name = raster_gdb + name_4
        raster_final_temp.save(raster_fianl_name)
        root = "D:/Programme/Alpaga Project(2)/Alpaga Project"
        rgdb = "outraster_project_firststep.gdb"
        raster_gdb = New_file(root,rgdb)
        arcpy.env.workspace = path + "/outraster_project_firststep.gdb"
        name_4 = "/temp_final" 
        raster_fianl_name = raster_gdb + name_4
        raster_final_temp.save(raster_fianl_name)
        # Second step : add landcover and global elevation to the binary map
        output_env = path + "/outraster_project_firststep.gdb"
        TransformTif_raster(path + "/Land_Cover_Europe","Land_Cover_Europe",output_env)
        TransformTif_raster(path + "/Global_Elevation","Global_Elevation",output_env)
        root = path 
        rgdb = "outraster_project_secondstep.gdb"
        raster_gdb = New_file(root,rgdb)
        arcpy.env.workspace = path + "/outraster_project_firststep.gdb"
        raster1 = arcpy.Raster("temp_final")
        raster2 = arcpy.Raster("Land_Cover_Europe")
        raster3 = arcpy.Raster("Global_Elevation")
        raster2_final = arcpy.sa.Con(raster2==13,1,)
        raster3bis = arcpy.sa.Con(raster3>0,raster3,)
        raster3_final = arcpy.sa.Con(raster3bis<4880,1,)
        raster_fianl_name = raster_gdb  + "/"+ "temp_final"
        raster1.save(raster_fianl_name)
        raster_fianl_name = raster_gdb  + "/"+ "Land_Cover_final"
        raster2_final.save(raster_fianl_name)
        raster_fianl_name = raster_gdb  + "/"+ "Global_Elevation_final"
        raster3_final.save(raster_fianl_name)
        # STEP 3 extraction on europe
        root = path 
        rgdb = "outraster_project_extraction.gdb"
        raster_gdb = New_file(root,rgdb)
        arcpy.env.workspace = path + "/Europe"
        arcpy.CopyFeatures_management("Europe.shp", path + "/outraster_project_secondstep.gdb/Europe")
        current_env = path + "/outraster_project_secondstep.gdb"
        output_env = path + "/outraster_project_extraction.gdb"
        name_mask = "Europe.shp"
        Extract_by_Mask(current_env,"temp_final",name_mask,output_env)
        Extract_by_Mask(current_env,"Global_Elevation_final",name_mask,output_env)
        Extract_by_Mask(current_env,"Land_Cover_final",name_mask,output_env)
        arcpy.env.workspace = path + "/outraster_project_extraction.gdb"
        root = path 
        rgdb = "outraster_project_thirdstep.gdb"
        raster_gdb = New_file(root,rgdb)
        raster1 = arcpy.Raster("temp_final_Europe")
        raster2 = arcpy.Raster("Global_Elevation_final_Europe")
        raster3 = arcpy.Raster("Land_Cover_final_Europe")
        # STEP 4 Combine the 3 bianary maps into one
        somme_raster = raster1+raster2+raster3
        raster_final = arcpy.sa.Con(somme_raster==3,1,0)
        raster_fianl_name = raster_gdb + "/finalstep"
        raster_final.save(raster_fianl_name)
        # END PART I
        
        # START PART II
        # Fist step map precipitation min 
        root = path 
        rgdb = "outraster_project_prec.gdb"
        raster_gdb = New_file(root,rgdb)
        arcpy.env.workspace = path + "/Precipitation"
        map_prec = arcpy.ListRasters("*", "TIF")
        i=1
        for raster in map_prec:
            raster = arcpy.Raster(raster)
            name_1 = "/map_raster_prec" + str(i)
            raster_name = raster_gdb + name_1
            raster.save(raster_name)
            i+=1
        arcpy.env.workspace = path + "/outraster_project_prec.gdb"
        rasters = arcpy.ListRasters("*", "GRID")
        for raster in rasters:
            raster
        precraster = raster
        i=1
        for raster in rasters:
            name_raster = "map_raster_prec" + str(i)
            if(raster==name_raster):
                raster = arcpy.Raster(raster)
                precraster = arcpy.sa.Con(raster<precraster, raster, precraster)
                name_2 = "/min_prec_" + str(i)
                precraster = arcpy.Raster(precraster)
                raster_min_name = raster_gdb + name_2
                precraster.save(raster_min_name)
                i+=1
        #Transformation of density population and GPD maps into raster maps
        root = path 
        rgdb = "outraster_project_density.gdb"
        raster_gdb = New_file(root,rgdb)
        root = path 
        rgdb = "outraster_project_GPD.gdb"
        raster_gdb = New_file(root,rgdb)
        root = path 
        rgdb = "outraster_project_fourstep.gdb"
        raster_gdb = New_file(root,rgdb)
        arcpy.env.workspace = path + "/outraster_project_prec.gdb"
        raster1 = arcpy.Raster("min_prec_12")
        raster1.save(raster_gdb + "/prec")
        arcpy.env.workspace = path + "/outraster_project_thirdstep.gdb"
        raster1 = arcpy.Raster("finalstep")
        raster1.save(raster_gdb + "/finalstep")
        arcpy.env.workspace = path + "/Population Density"
        output_env = path + "/outraster_project_density.gdb"
        TransformTif_raster(arcpy.env.workspace,"population_density",output_env)
        raster1 = arcpy.Raster("population_density")
        raster1.save(raster_gdb + "/population_density")
        arcpy.env.workspace =path + "/GDP Per Capita"
        output_env = path + "/outraster_project_GPD.gdb"
        TransformTif_raster(arcpy.env.workspace,"GDP_per_capita_PPP_Layer",output_env)
        raster1 = arcpy.Raster("GDP_per_capita_PPP_Layer")
        raster1.save(raster_gdb + "/GDP_per_capita_PPP_Layer")
        current_env =path + "/outraster_project_fourstep.gdb"
        output_env = path + "/outraster_project_fourstep.gdb"
        name_mask = "finalstep"
        # Extraction by mask of density, GPD and precipitation
        Extract_by_Mask(current_env,"prec",name_mask,output_env)
        Extract_by_Mask(current_env,"population_density",name_mask,output_env)
        Extract_by_Mask(current_env,"GDP_per_capita_PPP_Layer",name_mask,output_env)
        root = path 
        rgdb = "outraster_project_fourstep.gdb"
        raster_gdb = root + "/"+ rgdb
        #classify precipitation to 1 to 100 
        arcpy.env.workspace = path + "/outraster_project_fourstep.gdb"
        raster1 = arcpy.Raster("prec_Europe")
        out_classify = (raster1 - raster1.minimum)/(raster1.maximum-raster1.minimum)*100
        out_classify.save(raster_gdb + "/prec_classify")
        #classify population density 1 to 100 
        raster1 = arcpy.Raster("population_density_Europe")
        out_classify = (raster1 - raster1.minimum)/(raster1.maximum-raster1.minimum)*100
        out_classify = (out_classify -100)*(-1)
        out_classify.save(raster_gdb + "/density_classify")
        #classify GPD 1 to 100 
        raster1 = arcpy.Raster("GDP_per_capita_PPP_Layer_Europe")
        out_classify = (raster1 - raster1.minimum)/(raster1.maximum-raster1.minimum)*100
        out_classify = (out_classify -100)*(-1)
        out_classify.save(raster_gdb + "/gpd_classify")
        root = path 
        rgdb = "outraster_project_Final_Result.gdb"
        raster_gdb = New_file(root,rgdb)
    # Create the final map
    root = path 
    rgdb = "outraster_project_Final_Result.gdb"
    arcpy.env.workspace = path + "/outraster_project_Final_Result.gdb"
    rasters = arcpy.ListRasters("*", "GRID")
    nb_result = 1
    # calculate the number of file already create
    for raster in rasters:
        nb_result+=1
    arcpy.env.workspace = path + "/outraster_project_fourstep.gdb"
    root = path 
    rgdb = "outraster_project_Final_Result.gdb"
    raster_gdb = root+"/"+rgdb
    prec_raster = arcpy.Raster("prec_classify")
    dens_raster = arcpy.Raster("density_classify")
    gpd_raster = arcpy.Raster("gpd_classify")
    arcpy.env.workspace = path + "/outraster_project_Final_Result.gdb"
    # Compute the last raster with user criteria
    somme = prec_raster * a + dens_raster * c + gpd_raster * b
    somme = (somme - somme.minimum)/(somme.maximum-somme.minimum)*100
    somme = arcpy.Raster(somme)
    somme = arcpy.sa.Con(somme==3,somme,somme)
    raster_fianl_name = raster_gdb  + "/"+ "Result_final"+str(nb_result)
    print(raster_fianl_name)
    somme.save(raster_fianl_name)
    # Classify the new raster between 70 and 100
    somme2 =  arcpy.sa.Reclassify(somme,"Value", arcpy.sa.RemapRange([[0,somme.maximum-30,0]]))
    somme2 = (somme2 - somme2.minimum)/(somme2.maximum - somme2.minimum) * 100
    raster_fianl_name2 = raster_gdb  + "/"+ "Result_final_between_70_100_"+str(nb_result)
    somme2 = arcpy.Raster(somme2)
    somme2 = arcpy.sa.Con(somme2==100,somme2,somme2)
    print(raster_fianl_name2)
    somme2.save(raster_fianl_name2)


# In[18]:


# Enter the path of your files
path = "D:/Programme/Alpaga Project(2)/Alpaga Project"
AlpacaRegion(path)


# In[ ]:




