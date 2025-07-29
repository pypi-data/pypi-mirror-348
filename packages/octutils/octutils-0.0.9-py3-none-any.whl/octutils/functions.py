#!/usr/bin/env python
# coding: utf-8

# ## Notebook 3
# 
# New notebook

# In[1]:


import sempy.fabric as fabric 
from datetime import datetime
from notebookutils import mssparkutils
import json
import pytz
import pandas as pd
from pandas import json_normalize
from pyspark.sql.types import StructType, StructField, StringType, IntegerType,TimestampType
from pyspark.sql import functions as F
from pyspark.sql.functions import col, trim, lower, lit, when, udf, expr
from pyspark.sql import SparkSession,DataFrame
import numpy as np
import warnings
import re
from pyspark.sql import DataFrame
from collections import deque
from sempy.fabric.exceptions._exceptions import FabricHTTPException
from pyspark.sql.functions import concat, lit, when, regexp_replace,col


# In[2]:


from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("octutils") \
    .getOrCreate()


# In[3]:


spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "false")
warnings.filterwarnings("ignore")


# In[4]:


def get_executer_alias():
    try:
        executing_user = mssparkutils.env.getUserName()
        at_pos = executing_user.find('@')
        executing_user = executing_user[:at_pos]
    except Exception as e:
        msg = str(e)
        msg = msg.replace('"',"'")
        executing_user = msg = msg.replace("'",'"')
    return executing_user


# In[5]:


def get_modifiedtimestamp():
    try:
        pst_timezone = pytz.timezone('US/Pacific')
        current_time_utc = datetime.now(pytz.utc)
        current_time_pst = current_time_utc.astimezone(pst_timezone)
        current_time_pst = current_time_pst.replace(microsecond=0)
        current_time_pst = current_time_pst.replace(tzinfo=None)
    except Exception as e:
        current_time_pst = datetime(1900, 1, 1, 0, 0, 0)
    return current_time_pst


# In[6]:


def insert_update_stage_oct(spark_df, oct_table_name, on_name, parameter="No"):
    distinct_values = tuple(row[on_name] for row in spark_df.select(on_name).distinct().collect())
    if len(distinct_values) == 1:
        spark.sql(f"DELETE FROM {oct_table_name} WHERE {on_name} = '{distinct_values[0]}'")
    elif len(distinct_values) == 0:
        pass
    else:
        spark.sql(f"DELETE FROM {oct_table_name} WHERE {on_name} IN {distinct_values}")
    spark_df.write.format("delta").mode("append").saveAsTable(oct_table_name) 
    return "Merge Operation Completed"


# In[7]:


def get_workspace_name(WorkspaceID,get_all= "No"):
    alias = get_executer_alias()
    modified_time = get_modifiedtimestamp()
    try:
        WorkspaceID = WorkspaceID.lower()
        client = fabric.FabricRestClient()
        url = f'https://api.fabric.microsoft.com/v1/workspaces/{WorkspaceID}/'
        response = client.get(url)
        metadata = response.json()

        WorkspaceName = metadata.get('displayName','Unknown')
        message = f"{WorkspaceName} workspace name retrieval is successfull "

    except FabricHTTPException as e:
        error_response = e.response.json()
        error_code = error_response.get("errorCode", "UnknownError")
        error_msg = error_response.get("message", "No message found")
        message = f"{error_code} - {error_msg}"
        message = message.replace('"', "'").replace("'", '"')
        WorkspaceName = "Unknown"
    except Exception as e:
        message = str(e)
        message = message.replace('"', "'").replace("'", '"')
        WorkspaceName = "Unknown"
    
    if get_all == "Yes":
        pass
    else:
        schema = StructType([
        StructField("ID", StringType(), True),
        StructField("Name", StringType(), True),
        StructField("Info", StringType(), True),
        StructField("Alias", StringType(), True),
        StructField("ModifiedTime", TimestampType(), True)
        ])
        spark_df = spark.createDataFrame([(WorkspaceID,WorkspaceName,message,alias,modified_time)], schema)
        info = insert_update_stage_oct(spark_df = spark_df, oct_table_name = "workspacelist", on_name = "ID",parameter = "Yes")
    return (WorkspaceID,WorkspaceName,message,alias,modified_time)


# In[8]:


from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from datetime import datetime

def get_dataset_name(WorkspaceID, DatasetID,get_all = "No"):
    alias = get_executer_alias()
    modified_time = get_modifiedtimestamp()
    try:
        WorkspaceID = WorkspaceID.lower()
        DatasetID = DatasetID.lower()
        client = fabric.FabricRestClient()
        url = f'https://api.fabric.microsoft.com/v1/workspaces/{WorkspaceID}/items/{DatasetID}'
        response = client.get(url)
        metadata = response.json()
        dataset_name = metadata.get("displayName", "Unknown")
        message = f"{dataset_name} dataset name is retrieved"
    except FabricHTTPException as e:
        error_response = e.response.json()
        error_code = error_response.get("errorCode", "UnknownError")
        error_msg = error_response.get("message", "No message found")
        message = f"{error_code} - {error_msg}"
        dataset_name = "Unknown"
        message = message.replace('"', "'").replace("'", '"')
    except Exception:
        message = str(e)
        dataset_name = "Unknown"
        message = message.replace('"', "'").replace("'", '"')
    if get_all == "Yes":
        pass
    else:
        schema = StructType([
        StructField("WorkspaceID", StringType(), True),
        StructField("ID", StringType(), True),
        StructField("Name", StringType(), True),
        StructField("Info", StringType(), True),
        StructField("Alias", StringType(), True),
        StructField("ModifiedTime", TimestampType(), True)
        ])
        spark_df = spark.createDataFrame([(WorkspaceID,DatasetID,dataset_name,message,alias,modified_time)], schema)
        info = insert_update_stage_oct(spark_df = spark_df, oct_table_name = "datasetlist", on_name = "ID",parameter = "Yes")
    return (WorkspaceID, DatasetID, dataset_name, message, alias, modified_time)


# In[9]:


def get_lakehouse_name(WorkspaceID,LakehouseID,get_all = "No"):
    alias = get_executer_alias()
    modified_time = get_modifiedtimestamp()

    try:
        WorkspaceID = WorkspaceID.lower()
        LakehouseID = LakehouseID.lower()
        client = fabric.FabricRestClient()
        url = f'https://api.fabric.microsoft.com/v1/workspaces/{WorkspaceID}/items/{LakehouseID}'
        response = client.get(url)
        metadata = response.json()
        LakehouseName = metadata.get("displayName", "Unknown")
        message = f"{LakehouseName} dataset name is retrieved"
    except FabricHTTPException as e:
        LakehouseName = "Unknown"
        error_response = e.response.json()
        error_code = error_response.get("errorCode", "UnknownError")
        error_msg = error_response.get("message", "No message found")
        message = f"{error_code} - {error_msg}"
    except Exception:
        LakehouseName = "Unknown"
        message = str(e)
        message = message.replace('"', "'").replace("'", '"')
    if get_all == "Yes":
        pass
    else:
        schema = StructType([
        StructField("WorkspaceID", StringType(), True),
        StructField("ID", StringType(), True),
        StructField("Name", StringType(), True),
        StructField("Info", StringType(), True),
        StructField("Alias", StringType(), True),
        StructField("ModifiedTime", TimestampType(), True)
        ])
        spark_df = spark.createDataFrame([(WorkspaceID,LakehouseID,LakehouseName,message,alias,modified_time)], schema)
        info = insert_update_stage_oct(spark_df = spark_df, oct_table_name = "lakehouselist", on_name = "ID",parameter = "Yes")
    return (WorkspaceID,LakehouseID,LakehouseName,message,alias,modified_time)


# In[10]:


def build_path(node_id, parent_map):
    path = []
    while node_id is not None:
        path.insert(0, node_id)
        node_id = parent_map.get(node_id)
    return ">".join(path)


# In[11]:


def process_shortcuts():
    df = spark.sql("""SELECT Initial_Path,
                            CASE
                            WHEN source_path LIKE '%https://msit-onelake.dfs.fabric.microsoft.com/nan/nan/nan%' THEN NULL
                            ELSE source_path
                            END AS SourcePath
                    FROM oct_shortcuts_stage""")
    parent_map = dict(df.rdd.map(lambda row: (row["Initial_Path"], row["SourcePath"])).collect())

    # Perform recursive resolution in Python
    path_data = [(key, build_path(key, parent_map)) for key in parent_map.keys()]
    path_df = spark.createDataFrame(path_data, ["Initial_Path", "path"])
    df_with_path = df.join(path_df, on="Initial_Path", how="left")

    df_final = df_with_path.withColumn(
        "Final_Source_Path",
        expr("""
            CASE
                WHEN INSTR(path, '>') > 0 THEN SUBSTRING(path, LENGTH(path) - INSTR(REVERSE(path), '>') + 2)
                ELSE path
            END
        """)
    )
    df_final.createOrReplaceTempView("Final_Source_path_Extraction_view")

    final = spark.sql(""" 
        create or replace table oct_shortcuts as
        select a.initial_workspace_id as InitialWorkspaceID,
                a.initial_lakehouse_id as InitialLakehouseID,
                l.Name as InitialLakehouseName,
                concat("https://msit.powerbi.com/groups/",a.initial_workspace_id,"lakehouses/",a.initial_lakehouse_id,"?experience=power-bi") as InitialLakehouseLink,
                a.Initial_Path,
                a.shortcutName as Initial_Shortcut_Name,
                split(regexp_replace(b.Final_Source_Path, '^https://msit-onelake\.dfs\.fabric\.microsoft\.com/', ''), '/')[0] AS FinalSourceWorkspaceID,
                split(regexp_replace(b.Final_Source_Path, '^https://msit-onelake\.dfs\.fabric\.microsoft\.com/', ''), '/')[1] AS FinalSourceLakehouseID,
                fl.Name as FinalSourceLakehouseName,
                concat("https://msit.powerbi.com/groups/",split(regexp_replace(b.Final_Source_Path, '^https://msit-onelake\.dfs\.fabric\.microsoft\.com/', ''), '/')[0],"lakehouses/",split(regexp_replace(b.Final_Source_Path, '^https://msit-onelake\.dfs\.fabric\.microsoft\.com/', ''), '/')[1],"?experience=power-bi") as FinalSourceLakehouseLink,
                b.Final_Source_Path,
                case when a.initial_adls_path <> "nannan" then a.initial_adls_path
                        when a.initial_adls_path == "nannan" and c.initial_adls_path <> "nannan" then c.initial_adls_path
                        when a.initial_adls_path == "nannan" and c.initial_adls_path == "nannan" then Null
                        else "Failed Extraction"
                        end as Source_ADLS_Path,
                case when d.Lakehouse_ID is null then "Yes" else "No" end as OSOTLakehouseFlag,
                d.Lakehouse_Type as SourceLakehouseType,
                d.`Area/Domain` as Source_Area_Domain,
                a.Alias,
                a.ModifiedTime
        from oct_shortcuts_stage a 
        join Final_Source_path_Extraction_view b on a.initial_path = b.Initial_Path
        left join oct_shortcuts_stage c on b.Final_Source_Path = c.initial_path
        left join delta.`abfss://ed6737e8-6e3a-4d64-ac9c-3441eec71500@msit-onelake.dfs.fabric.microsoft.com/1df68066-3cfa-44a9-86fe-16135cd86ae8/Tables/OSOT_Lakehouses` d on lcase(trim(split(regexp_replace(b.Final_Source_Path, '^https://msit-onelake\.dfs\.fabric\.microsoft\.com/', ''), '/')[1])) = lcase(trim(d.Lakehouse_ID))
        left join lakehouselist l on lcase(trim(l.ID)) = lcase(trim(a.initial_lakehouse_id))  
        left join lakehouselist fl on lcase(trim(fl.ID))  = lcase(trim(split(regexp_replace(b.Final_Source_Path, '^https://msit-onelake\.dfs\.fabric\.microsoft\.com/', ''), '/')[1]))
    """)   
    return "Operation Completed"


# In[12]:


def get_lakehouse_shortcuts(WorkspaceID,LakehouseID,memorylakehouseset,get_all= "No",force_reload = False):
    Alias = get_executer_alias()
    ModifiedTime = get_modifiedtimestamp()
    try:
        df_table = spark.sql(f"select * from oct_shortcuts_stage where initial_lakehouse_id = '{LakehouseID}'")
        if df_table.rdd.isEmpty():
            exists = 0
            latency = 9999
        else: 
            exists = 1 
            PrevLoadTime = df_table.select("ModifiedTime").first()[0]

            latency = abs((ModifiedTime - PrevLoadTime).days)
        if force_reload:
            condition = False
        else:
            condition = (exists==1 and latency <=2)
            
        if condition:
            error_schema = StructType([
            StructField("Workspace_ID", StringType(), True),
            StructField("Item_Type", StringType(), True),
            StructField("Item_ID", StringType(), True),
            StructField("Error_Message", StringType(), True),
            StructField("Alias", StringType(), True),
            StructField("ModifiedTime", TimestampType(), True)
            ])
            schema = StructType([
                StructField("initial_workspace_id", StringType(), True),
                StructField("initial_lakehouse_id", StringType(), True),
                StructField("ShortcutName", StringType(), True),
                StructField("initial_path", StringType(), True),
                StructField("initial_adls_path", StringType(), True),
                StructField("source_workspace_id", StringType(), True),
                StructField("source_lakehouse_id", StringType(), True),
                StructField("source_path", StringType(), True),
                StructField("Alias", StringType(), True),
                StructField("ModifiedTime", TimestampType(), True)
            ])
            shortcuts = spark.createDataFrame([],schema)
            errors = spark.createDataFrame([],error_schema) 
        else:
            client = fabric.FabricRestClient()
            response = client.get(f"https://api.fabric.microsoft.com/v1/workspaces/{WorkspaceID}/items/{LakehouseID}/shortcuts")
            json_data = response.json().get("value", [])
            shortcutsAPI_Schema = StructType([ StructField("name", StringType(), True),
                                            StructField("path", StringType(), True),
                                            StructField("target", StructType([StructField("type", StringType(), True), StructField("oneLake", StructType([StructField("itemId",StringType(), True), StructField("path",StringType(), True), StructField("workspaceId",StringType(), True)]), True),StructField("adlsGen2", StructType([StructField("connectionId",StringType(), True), StructField("location",StringType(), True), StructField("subpath",StringType(), True)]), True) ]), True),
                    ])
            shortcuts = spark.createDataFrame(json_data,shortcutsAPI_Schema)
            shortcuts = shortcuts.withColumn("Alias", lit(Alias)) \
                                .withColumn("ModifiedTime", lit(ModifiedTime)) \
                                .withColumn("initial_workspace_id", lit(WorkspaceID)) \
                                .withColumn("initial_lakehouse_id", lit(LakehouseID)) \
                                .withColumn("ShortcutName",concat(when(col("path").contains("/Tables/"),concat(regexp_replace(col("path"), "/Tables/", ""), lit("."))).when(col("path").contains("/Tables"),concat(regexp_replace(col("path"), "/Tables", "dbo"), lit("."))).otherwise(lit("")),col("name"))) \
                                .select(col("initial_workspace_id"),
                                                    col("initial_lakehouse_id"),
                                                    col("ShortcutName"),
                                                    concat(lit("https://msit-onelake.dfs.fabric.microsoft.com/"), col("initial_workspace_id"),lit("/") ,col("initial_lakehouse_id"),col('path'),lit("/"),col('name')).alias("initial_path"),
                                                    concat(col("target.adlsGen2.location"),col("target.adlsGen2.subpath")).alias("initial_adls_path"),
                                                    col("target.oneLake.workspaceId").alias("source_workspace_id"),
                                                    col("target.oneLake.itemId").alias("source_lakehouse_id"),
                                                    concat(lit("https://msit-onelake.dfs.fabric.microsoft.com/"),col("source_workspace_id"),lit("/"),col("source_lakehouse_id"),lit("/"),col('target.oneLake.path')).alias("source_path"),
                                                    col("Alias"),
                                                    col("ModifiedTime")
                                                    )
            source_spark_df = shortcuts.select(col("source_workspace_id"),col("source_lakehouse_id")).dropDuplicates(["source_workspace_id", "source_lakehouse_id"]) \
                                            .filter(col("source_workspace_id").isNotNull() & col("source_lakehouse_id").isNotNull())
            memorylakehouseset.add(LakehouseID)
            if source_spark_df.rdd.isEmpty():
                pass
            else:
                for row in source_spark_df.toLocalIterator():
                    source_workspace_id = row["source_workspace_id"]
                    source_lakehouse_id = row["source_lakehouse_id"]
                    if source_lakehouse_id in memorylakehouseset:
                        continue
                    else:
                        get_workspace_name(WorkspaceID =source_workspace_id)
                        get_lakehouse_name(WorkspaceID =source_workspace_id,LakehouseID = source_lakehouse_id,get_all="No")
                        shortcuts_stage, errors_stage, memorylakehouseset_stage = get_lakehouse_shortcuts(WorkspaceID=source_workspace_id,LakehouseID=source_lakehouse_id,memorylakehouseset=memorylakehouseset)
                        memorylakehouseset.update(memorylakehouseset_stage)
                        shortcuts = shortcuts.unionByName(shortcuts_stage)
            
            error_schema = StructType([
                StructField("Workspace_ID", StringType(), True),
                StructField("Item_Type", StringType(), True),
                StructField("Item_ID", StringType(), True),
                StructField("Error_Message", StringType(), True),
                StructField("Alias", StringType(), True),
                StructField("ModifiedTime", TimestampType(), True)
            ])
            errors = spark.createDataFrame([],error_schema)

    except FabricHTTPException as e:
        error_schema = StructType([
            StructField("Workspace_ID", StringType(), True),
            StructField("Item_Type", StringType(), True),
            StructField("Item_ID", StringType(), True),
            StructField("Error_Message", StringType(), True),
            StructField("Alias", StringType(), True),
            StructField("ModifiedTime", TimestampType(), True)
        ])
        schema = StructType([
            StructField("initial_workspace_id", StringType(), True),
            StructField("initial_lakehouse_id", StringType(), True),
            StructField("ShortcutName", StringType(), True),
            StructField("initial_path", StringType(), True),
            StructField("initial_adls_path", StringType(), True),
            StructField("source_workspace_id", StringType(), True),
            StructField("source_lakehouse_id", StringType(), True),
            StructField("source_path", StringType(), True),
            StructField("Alias", StringType(), True),
            StructField("ModifiedTime", TimestampType(), True)
        ])
        shortcuts = spark.createDataFrame([],schema)
        error_response = e.response.json()
        error_code = error_response.get("errorCode", "UnknownError")
        error_msg = error_response.get("message", "No message found")
        message = f"{error_code} - {error_msg}"
        message = message.replace('"', "'").replace("'", '"')
        errors = spark.createDataFrame([(WorkspaceID, "Shortcuts", LakehouseID, str(message), Alias, ModifiedTime)],error_schema) 
    except Exception as e:
        error_schema = StructType([
            StructField("Workspace_ID", StringType(), True),
            StructField("Item_Type", StringType(), True),
            StructField("Item_ID", StringType(), True),
            StructField("Error_Message", StringType(), True),
            StructField("Alias", StringType(), True),
            StructField("ModifiedTime", TimestampType(), True)
        ])
        schema = StructType([
            StructField("initial_workspace_id", StringType(), True),
            StructField("initial_lakehouse_id", StringType(), True),
            StructField("ShortcutName", StringType(), True),
            StructField("initial_path", StringType(), True),
            StructField("initial_adls_path", StringType(), True),
            StructField("source_workspace_id", StringType(), True),
            StructField("source_lakehouse_id", StringType(), True),
            StructField("source_path", StringType(), True),
            StructField("Alias", StringType(), True),
            StructField("ModifiedTime", TimestampType(), True)
        ])
        shortcuts = spark.createDataFrame([],schema)
        errors = spark.createDataFrame([(WorkspaceID, "Shortcuts", LakehouseID, str(e), Alias, ModifiedTime)],error_schema)
    if get_all == "Yes" or not(condition):
        pass
    else: 
        msg = insert_update_stage_oct(spark_df = shortcuts, oct_table_name = "oct_shortcuts_stage" , on_name = "initial_lakehouse_id", parameter = "No")
        error_msg = insert_update_stage_oct(spark_df = errors, oct_table_name = "oct_errors" , on_name = "Item_ID", parameter = "No")
        process_shortcuts() 
    return shortcuts,errors,memorylakehouseset


# In[13]:


def get_all_lakehouse_shortcuts():
    get_all = "Yes"
    force_reload = True
    memorylakehouseset = set()
    spark_shortcuts = spark.createDataFrame([],schema)
    spark_errors = spark.createDataFrame([],error_schema)
    lakehouselist_table = spark.sql("select WorkspaceID,ID from lakehouselist")
    for row in lakehouselist_table.collect():
        WorkspaceID = row['WorkspaceID']
        ID = row['ID']
        spark_shortcuts_stage, spark_errors_stage, memorylakehouseset  = get_lakehouse_shortcuts(WorkspaceID=WorkspaceID , LakehouseID = ID, memorylakehouseset = memorylakehouseset,get_all = get_all, force_reload = force_reload)
        spark_shortcuts = spark_shortcuts.union(spark_shortcuts_stage)
        spark_errors = spark_errors.union(spark_errors_stage)
    msg = insert_update_stage_oct(spark_df = spark_shortcuts, oct_table_name = "oct_shortcuts_stage" , on_name = "initial_lakehouse_id", parameter = "No")
    error_msg = insert_update_stage_oct(spark_df = spark_errors, oct_table_name = "oct_errors" , on_name = "Item_ID", parameter = "No")
    process_shortcuts() 
    return spark_shortcuts,spark_errors,memorylakehouseset


# In[14]:


def get_tmsl(Workspace,Dataset):
    tmsl_script = fabric.get_tmsl(Dataset,Workspace)
    tmsl_dict = json.loads(tmsl_script)
    return tmsl_dict


# In[15]:


def extract_right_of_dot(s):
    if "." in s:
        newstring = s.split(".", 1)[1]
    else:
        newstring = s
    return newstring


# In[16]:


def clean_text(text):
    new_string = text.replace("[", "")
    new_string = new_string.replace("]", "")
    new_string = new_string.split('#')[0].strip()
    new_string = new_string.split(')')[0].strip()
    return new_string


# In[17]:


def get_dataset_lineage(WorkspaceID,DatasetID,get_all = "No"):
    
    tables_df =  pd.DataFrame(columns = ['Workspace_ID','Dataset_ID','Mode','Source_Type','Expression',"Table_Name","Source_Table_Name","Alias","ModifiedTime"])
    expressions_df =  pd.DataFrame(columns = ['Workspace_ID','Dataset_ID',"Name","Expression","Alias","ModifiedTime"])
    columns_df = pd.DataFrame(columns = ['Workspace_ID','Dataset_ID',"Table_Name","Column_Name","Data_Type","Alias","ModifiedTime"])
    measures_df = pd.DataFrame(columns = ['Workspace_ID','Dataset_ID',"Table_Name","Measure_Name","Expression","Description","Format","Alias","ModifiedTime"])
    relationships_df = pd.DataFrame(columns = ['WorkspaceID','DatasetID','Name', 'FromTable', 'FromColumn', 'ToTable', 'ToColumn', 'State','CrossFilteringBehavior','SecurityFilteringBehavior', 'Active','ToCardinality', 'RelationshipModifiedTime', 'RefreshedTime',"Alias","ModifiedTime"])
    model_df = pd.DataFrame(columns = ['WorkspaceID','DatasetID','DatasetName','createdTimestamp',"Last_Update","Last_Schema_Update","Last_Processed","Alias","ModifiedTime"])
    roles_df = pd.DataFrame(columns = ['WorkspaceID','DatasetID',"RoleName","RoleModelPermission","RoleModifiedTime",'TableName',"TableFilterExpression","TablemodifiedTime","Alias","ModifiedTime"])
    Alias = get_executer_alias()
    ModifiedTime = get_modifiedtimestamp()
    try: 
        tmsl = get_tmsl(Workspace = WorkspaceID,Dataset = DatasetID)
        model_name = tmsl.get('name','Unknown') 
        model_createdTimestamp = tmsl.get('createdTimestamp','')
        model_last_update = tmsl.get('lastUpdate','')
        model_last_schema_update = tmsl.get('lastSchemaUpdate','')
        model_last_processed = tmsl.get('lastProcessed','')
        model_df.loc[len(model_df)+1] = [WorkspaceID,DatasetID,model_name,model_createdTimestamp,model_last_update,model_last_schema_update,model_last_processed,Alias,ModifiedTime]
        model = tmsl.get('model',{}) 
        relationships = model.get('relationships',[])
        for relindex in range(len(relationships)):
            relationship = relationships[relindex]
            RelationshipName = relationship.get('name','')
            fromTable = relationship.get('fromTable','')
            fromColumn = relationship.get('fromColumn','')
            toTable = relationship.get('toTable','')
            toColumn = relationship.get('toColumn','')
            state = relationship.get('state','')
            crossFilteringBehavior = relationship.get('crossFilteringBehavior','OneDirection')
            SecurityFilteringBehavior = relationship.get('securityFilteringBehavior','OneDirection')
            Active = relationship.get('isActive','true')
            toCardinality = relationship.get('toCardinality','One') 
            modifiedTime = relationship.get('modifiedTime','')
            refreshedTime = relationship.get('refreshedTime','')
            relationships_df.loc[len(relationships_df)+1] = [WorkspaceID,DatasetID,RelationshipName,fromTable,fromColumn,toTable,toColumn,state,crossFilteringBehavior,SecurityFilteringBehavior,Active,toCardinality,modifiedTime,refreshedTime,Alias,ModifiedTime]
        
        roles = model.get('roles',[])
        for roleindex in range(len(roles)):
            role = roles[roleindex]
            rolename = role.get('name','Unknown')
            rolemodelpermission = role.get('modelPermission','Unknown')
            rolemodifiedTime= role.get('modifiedTime','Unknown')
            rolemembers = role.get('members',[])
            tablePermissions = role.get('tablePermissions',[])
            
            if len(tablePermissions)>0:
                for tablepermissionindex in range(len(tablePermissions)):
                    tablepermissionname = tablePermissions[tablepermissionindex].get('name','')
                    tablepermissionfilterExpression = tablePermissions[tablepermissionindex].get('filterExpression','')
                    tablepermissionmodifiedTime = tablePermissions[tablepermissionindex].get('modifiedTime','')
                roles_df.loc[len(roles_df)+1] = [WorkspaceID,DatasetID,rolename,rolemodelpermission,rolemodifiedTime,tablepermissionname,tablepermissionfilterExpression,tablepermissionmodifiedTime,Alias,ModifiedTime]
            else:
                roles_df.loc[len(roles_df)+1] = [WorkspaceID,DatasetID,rolename,rolemodelpermission,rolemodifiedTime,"Not Applicable","Not Applicable","Not Applicable",Alias,ModifiedTime]
        
        tables = model.get('tables',"Not Present") 

        if tables != "Not Present":
            for index in range(len(tables)):
                table_name = tables[index]["name"] if "name" in tables[index] else "Not Present"
                partitions = tables[index]["partitions"][0] if "partitions" in tables[index] else "Not Present"
                if partitions != "Not Present":
                    mode = partitions["mode"] if "mode" in partitions else "Default"
                    source = partitions["source"] if "source" in partitions else "Not Present"
                    if source != "Not Present":
                        expression = source["expression"] if "expression" in source else "Not Present"
                        expression_type = source["type"] if "type" in source else "Not Present"
                        if expression_type == "calculated":
                            source_table_name = "Calculated in model"
                            source_type = "Power BI/Semantic Model"
                        elif "entityName" in source:
                            source_type = "Microsoft Fabric"
                            source_table_name = source["schemaName"] + '.' + source["entityName"] if "schemaName" in source else source["entityName"]  
                            expression = source["expressionSource"] if "expressionSource" in source else "Not Present"
                        elif 'Sql.Database' in expression:
                            source_type = "SQL Server Database"
                            if 'Item=\"' in expression:
                                if 'Schema=\"' in expression:
                                    source_table_name = expression.split('Schema=\"')[1].split('"')[0] + '.' + expression.split('Item=\"')[1].split('"')[0]
                                else:
                                    source_table_name = expression.split('Item=\"')[1].split('"')[0]
                            elif 'Query=\"' in expression:
                                pattern1 = r'(?<=\bFROM)\s+(\w+\S*)'
                                pattern2 = r'(?<=\bJOIN)\s+(\w+\S*)'
                                pattern3 = r'(delta\.\s+)(\S+)+'
                                pattern4 = r'(parquet\.\s+)(\S+)+'
                                pattern5 = r'(?<=\bfrom)\s+(\[\w+\S*)'
                                pattern6 = r'(?<=\bjoin)\s+(\[\w+\S*)'
                                Query = expression.split('Query=\"')[1].split('"]')[0]
                                pattern_from = re.findall(pattern1, Query, re.IGNORECASE)
                                pattern_join = re.findall(pattern2, Query, re.IGNORECASE)
                                pattern_delta = re.findall(pattern3, Query, re.IGNORECASE)
                                pattern_parquet = re.findall(pattern4, Query, re.IGNORECASE)
                                pattern_from_brace = re.findall(pattern5, Query, re.IGNORECASE)
                                pattern_join_brace = re.findall(pattern6, Query, re.IGNORECASE)
                                source_table_name_list = pattern_from + pattern_join + pattern_delta + pattern_parquet + pattern_from_brace + pattern_join_brace
                                source_table_name = [clean_text(s) for s in source_table_name_list]
                            elif 'Navigation = Source{[Schema = \"' in expression:
                                schema_name = expression.split('Navigation = Source{[Schema = \"')[1].split('"')[0]
                                if 'Item = \"' in expression: 
                                    source_table_name = expression.split('Item = \"')[1].split('"')[0]
                                    source_table_name = source_table_name = schema_name + "." + source_table_name
                                else:
                                    source_table_name = "Item not found"
                            else:
                                source_table_name = "Not Found"
                        elif 'StaticTable' in expression:
                            source_table_name = 'StaticTable'
                            source_type = 'StaticTable'
                        elif 'Row(\"' in expression:
                            source_table_name = 'StaticTable'
                            source_type = 'StaticTable'
                        elif 'Navigation = Source{[Name = \"' in expression:
                            source_table_name = expression.split('Navigation = Source{[Name = \"')[1].split('"')[0]
                            source_type = "Azure" if 'AzureStorage.DataLake' in expression else "Naviagation type Not Defined in code"
                        elif 'Navigation = Source{[Name=\"' in expression:
                            source_table_name = expression.split('Navigation = Source{[Name=\"')[1].split('"')[0]
                            source_type = "Azure" if 'AzureStorage.DataLake' in expression else "Naviagation type Not Defined in code"   
                        elif 'Json.Document(Binary.Decompress(Binary.FromText(\"' in expression:
                            source_table_name = expression.split('Json.Document(Binary.Decompress(Binary.FromText(\"')[1].split('"')[0]
                            source_type = "binary Json Document" if 'Json.Document(Binary' in expression else "Json type Not Defined in code"
                        elif 'Excel.Workbook(File.Contents(\"' in expression:
                            source_table_name = expression.split('Excel.Workbook(File.Contents(\"')[1].split('"')[0]
                            source_type = "Excel Workbook" if 'Excel.Workbook(File.Contents(\"' in expression else "Excel Workbook type Not Defined in code"
                        elif 'Excel.Workbook(Web.Contents(\"' in expression:
                            source_table_name = expression.split('Excel.Workbook(Web.Contents(\"')[1].split('"')[0]
                            source_type = "Excel Workbook" if 'Excel.Workbook(Web.Contents(\"' in expression else "Excel Workbook type Not Defined in code"
                        elif 'Csv.Document(Web.Contents(\"' in expression:
                            source_table_name = expression.split('Csv.Document(Web.Contents(\"')[1].split('"')[0]
                            source_type = "Csv Document" if 'Csv.Document(Web.Contents(\"' in expression else "CSV Document type Not Defined in code"
                        elif 'Source = DateTime.LocalNow()' in expression:
                            source_table_name = 'Calculated DateTime function'
                            source_type = "Calculated Datetime" if 'Source = DateTime.LocalNow()' in expression else "datetime type Not Defined in code"
                        elif 'Source = AzureStorage.DataLake(\"' in expression:
                            source_table_name = expression.split('Source = AzureStorage.DataLake(\"')[1].split('"')[0]
                            source_type = "AzureStorage DataLake" if 'Source = AzureStorage.DataLake(\"' in expression else "AzureStorage DataLake type Not Defined in code"
                        elif 'SharePoint.Tables(\"' in expression:
                            source_table_name = expression.split('SharePoint.Tables(\"')[1].split('"')[0]
                            source_type = "SharePoint" if 'SharePoint.Tables(\"' in expression else "Sharepoint type Not Defined in code"
                        elif 'SharePoint.Files(\"' in expression:
                            source_table_name = expression.split('SharePoint.Files(\"')[1].split('"')[0]
                            source_type = "SharePoint" if 'SharePoint.Files(\"' in expression else "Sharepoint type Not Defined in code"
                        elif 'Databricks.Catalogs(' in expression:
                            try:
                                source_table_name = re.findall(r'Name="(.*?)",Kind="Table"', expression)
                                source_table_name = source_table_name[0]
                                source_type = "Azure Databricks"
                            except Exception as e:
                                source_table_name = str(e)
                                source_type = "Azure Databricks"
                        elif 'Table.Combine({' in expression:
                            source_table_name = "Calculated in model"
                            source_type = "Table Combine"
                        elif 'Table.FromRows(' in expression:
                            source_table_name = "StaticTable"
                            source_type = "StaticTable"
                        elif expression_type == "calculationGroup":
                            source_table_name = "calculationGroup"
                            source_type == expression_type
                        elif 'AnalysisServices.Database' in expression:
                            source_table_name = 'Out of Scope'
                            source_type = 'Out of scope'
                        else:
                            source_type = "Notdefined"
                            source_table_name = "Notdefined"
                        if isinstance(source_table_name, list):
                            for stname in source_table_name:
                                #Source_Table_Name_wo_Schema = extract_right_of_dot(s=stname)
                                tables_df.loc[len(tables_df)+1] = [WorkspaceID,DatasetID,mode,source_type,expression,table_name,stname,Alias,ModifiedTime]
                        else:
                            #Source_Table_Name_wo_Schema = extract_right_of_dot(s=source_table_name)
                            tables_df.loc[len(tables_df)+1] = [WorkspaceID,DatasetID,mode,source_type,expression,table_name,source_table_name,Alias,ModifiedTime]

                
                if 'columns' in tables[index].keys():
                    columns = tables[index]["columns"]
                    for colindex in range(len(columns)):
                        column_name = columns[colindex]["name"] if "name" in columns[colindex] else "Not Present"
                        column_datatype = columns[colindex]["dataType"] if "dataType" in columns[colindex] else "Not Present"
                        columns_df.loc[len(columns_df)+1] = [WorkspaceID,DatasetID,table_name,column_name,column_datatype,Alias,ModifiedTime]
        
                
                if "measures" in tables[index].keys():
                    measures = tables[index]["measures"]
                    for measureindex in range(len(measures)):
                        measure_name = measures[measureindex]["name"] if "name" in measures[measureindex] else "Not Present"
                        measure_expression = measures[measureindex]["expression"] if "expression" in measures[measureindex] else "Not Present"
                        measure_description = measures[measureindex]["description"] if "description" in measures[measureindex] else ""
                        measure_format = measures[measureindex]["formatString"] if "formatString" in measures[measureindex] else ""
                        measures_df.loc[len(measures_df)+1] = [WorkspaceID,DatasetID,table_name,measure_name,measure_expression,measure_description,measure_format,Alias,ModifiedTime]
        
        express = model.get("expressions",[])
        if express:
            for index in range(len(express)):
                expression_name = express[index]["name"]
                expression = express[index]["expression"]
                expressions_df.loc[len(expressions_df)+1] = [WorkspaceID,DatasetID,expression_name,expression,Alias,ModifiedTime]
        
        if get_all == "Yes":
            pass
        else:
            schema_tables = StructType([
                StructField("Workspace_ID", StringType(), True),   
                StructField("Dataset_ID", StringType(), True),    
                StructField("Mode", StringType(), True),
                StructField("Source_Type", StringType(), True), 
                StructField("Expression", StringType(), True), 
                StructField("Table_Name", StringType(), True), 
                StructField("Source_Table_Name", StringType(), True), 
                StructField("Alias", StringType(), True), 
                StructField("ModifiedTime", TimestampType(), True)
            ])
            schema_expressions = StructType([
                    StructField("Workspace_ID", StringType(), True),   
                    StructField("Dataset_ID", StringType(), True),    
                    StructField("Name", StringType(), True),
                    StructField("Expression", StringType(), True),
                    StructField("Alias", StringType(), True), 
                    StructField("ModifiedTime", TimestampType(), True)
                ])
            schema_columns = StructType([
                        StructField("Workspace_ID", StringType(), True),   
                        StructField("Dataset_ID", StringType(), True),    
                        StructField("Table_Name", StringType(), True),
                        StructField("Column_Name", StringType(), True),
                        StructField("Data_Type", StringType(), True),       
                        StructField("Alias", StringType(), True), 
                        StructField("ModifiedTime", TimestampType(), True)
                    ])
            schema_measures = StructType([
                    StructField("Workspace_ID", StringType(), True),   
                    StructField("Dataset_ID", StringType(), True),    
                    StructField("Table_Name", StringType(), True),
                    StructField("Measure_Name", StringType(), True),
                    StructField("Expression", StringType(), True),    
                    StructField("Description", StringType(), True),
                    StructField("Format", StringType(), True),
                    StructField("Alias", StringType(), True), 
                    StructField("ModifiedTime", TimestampType(), True)
                ])
            schema_relationships = StructType([
                    StructField("Workspace_ID", StringType(), True),   
                    StructField("DatasetID", StringType(), True),    
                    StructField("Name", StringType(), True),
                    StructField("FromTable", StringType(), True),
                    StructField("FromColumn", StringType(), True),    
                    StructField("ToTable", StringType(), True),
                    StructField("ToColumn", StringType(), True),
                    StructField("State", StringType(), True),
                    StructField("CrossFilteringBehavior", StringType(), True),
                    StructField("SecurityFilteringBehavior", StringType(), True),
                    StructField("Active", StringType(), True),
                    StructField("ToCardinality", StringType(), True),
                    StructField("RelationshipModifiedTime", StringType(), True),
                    StructField("RefreshedTime", StringType(), True),
                    StructField("Alias", StringType(), True), 
                    StructField("ModifiedTime", TimestampType(), True)
                ])
            schema_model = StructType([
                    StructField("Workspace_ID", StringType(), True),   
                    StructField("DatasetID", StringType(), True),    
                    StructField("DatasetName", StringType(), True),
                    StructField("createdTimestamp", StringType(), True),
                    StructField("Last_Update", StringType(), True),    
                    StructField("Last_Schema_Update", StringType(), True),
                    StructField("Last_Processed", StringType(), True),
                    StructField("Alias", StringType(), True), 
                    StructField("ModifiedTime", TimestampType(), True)
                ])
            schema_role = StructType([
                    StructField("Workspace_ID", StringType(), True),   
                    StructField("DatasetID", StringType(), True),    
                    StructField("RoleName", StringType(), True),
                    StructField("RoleModelPermission", StringType(), True),
                    StructField("RoleModifiedTime", StringType(), True),    
                    StructField("TableName", StringType(), True),
                    StructField("TableFilterExpression", StringType(), True),
                    StructField("TablemodifiedTime", StringType(), True),
                    StructField("Alias", StringType(), True), 
                    StructField("ModifiedTime", TimestampType(), True)
                ]) 
            spark_tables = spark.createDataFrame(tables_df,schema_tables)
            spark_expressions = spark.createDataFrame(expressions_df,schema_expressions)
            spark_columns = spark.createDataFrame(columns_df,schema_columns)
            spark_measures = spark.createDataFrame(measures_df,schema_measures)
            spark_relationship = spark.createDataFrame(relationships_df,schema_relationships)
            spark_model = spark.createDataFrame(model_df,schema_model)
            spark_roles = spark.createDataFrame(roles_df,schema_role)
            
            msg = insert_update_stage_oct(spark_df = spark_tables, oct_table_name = "oct_tables" , on_name = "Dataset_ID", parameter = "No")
            msg = insert_update_stage_oct(spark_df = spark_expressions, oct_table_name = "oct_expression" , on_name = "Dataset_ID", parameter = "No")
            msg = insert_update_stage_oct(spark_df = spark_columns, oct_table_name = "oct_column" , on_name = "Dataset_ID", parameter = "No")
            msg = insert_update_stage_oct(spark_df = spark_measures, oct_table_name = "oct_measures" , on_name = "Dataset_ID", parameter = "No")
            msg = insert_update_stage_oct(spark_df = spark_relationship, oct_table_name = "oct_relationship" , on_name = "DatasetID", parameter = "No")
            msg = insert_update_stage_oct(spark_df = spark_model, oct_table_name = "oct_model" , on_name = "DatasetID", parameter = "No")
            msg = insert_update_stage_oct(spark_df = spark_roles, oct_table_name = "oct_roles" , on_name = "DatasetID", parameter = "No")
    except Exception as e:
        error_schema = StructType([
            StructField("Workspace_ID", StringType(), True),
            StructField("Item_Type", StringType(), True),
            StructField("Item_ID", StringType(), True),
            StructField("Error_Message", StringType(), True),
            StructField("Alias", StringType(), True),
            StructField("ModifiedTime", TimestampType(), True)
        ])

        errors_df = spark.createDataFrame([(WorkspaceID, "Dataset", DatasetID, str(e), Alias, ModifiedTime)],error_schema)
        error_msg = insert_update_stage_oct(spark_df = errors_df, oct_table_name = "oct_errors" , on_name = "Item_ID", parameter = "No")
    return (expressions_df,tables_df,columns_df,measures_df,relationships_df,model_df,roles_df)    


# In[18]:


def get_all_dataset_lineage():
    schema_tables = StructType([
                StructField("Workspace_ID", StringType(), True),   
                StructField("Dataset_ID", StringType(), True),    
                StructField("Mode", StringType(), True),
                StructField("Source_Type", StringType(), True), 
                StructField("Expression", StringType(), True), 
                StructField("Table_Name", StringType(), True), 
                StructField("Source_Table_Name", StringType(), True), 
                StructField("Alias", StringType(), True), 
                StructField("ModifiedTime", TimestampType(), True)
            ])
    schema_expressions = StructType([
            StructField("Workspace_ID", StringType(), True),   
            StructField("Dataset_ID", StringType(), True),    
            StructField("Name", StringType(), True),
            StructField("Expression", StringType(), True),
            StructField("Alias", StringType(), True), 
            StructField("ModifiedTime", TimestampType(), True)
        ])
    schema_columns = StructType([
                StructField("Workspace_ID", StringType(), True),   
                StructField("Dataset_ID", StringType(), True),    
                StructField("Table_Name", StringType(), True),
                StructField("Column_Name", StringType(), True),
                StructField("Data_Type", StringType(), True),       
                StructField("Alias", StringType(), True), 
                StructField("ModifiedTime", TimestampType(), True)
            ])
    schema_measures = StructType([
            StructField("Workspace_ID", StringType(), True),   
            StructField("Dataset_ID", StringType(), True),    
            StructField("Table_Name", StringType(), True),
            StructField("Measure_Name", StringType(), True),
            StructField("Expression", StringType(), True),    
            StructField("Description", StringType(), True),
            StructField("Format", StringType(), True),
            StructField("Alias", StringType(), True), 
            StructField("ModifiedTime", TimestampType(), True)
        ])
    schema_relationships = StructType([
            StructField("Workspace_ID", StringType(), True),   
            StructField("DatasetID", StringType(), True),    
            StructField("Name", StringType(), True),
            StructField("FromTable", StringType(), True),
            StructField("FromColumn", StringType(), True),    
            StructField("ToTable", StringType(), True),
            StructField("ToColumn", StringType(), True),
            StructField("State", StringType(), True),
            StructField("CrossFilteringBehavior", StringType(), True),
            StructField("SecurityFilteringBehavior", StringType(), True),
            StructField("Active", StringType(), True),
            StructField("ToCardinality", StringType(), True),
            StructField("RelationshipModifiedTime", StringType(), True),
            StructField("RefreshedTime", StringType(), True),
            StructField("Alias", StringType(), True), 
            StructField("ModifiedTime", TimestampType(), True)
        ])
    schema_model = StructType([
            StructField("Workspace_ID", StringType(), True),   
            StructField("DatasetID", StringType(), True),    
            StructField("DatasetName", StringType(), True),
            StructField("createdTimestamp", StringType(), True),
            StructField("Last_Update", StringType(), True),    
            StructField("Last_Schema_Update", StringType(), True),
            StructField("Last_Processed", StringType(), True),
            StructField("Alias", StringType(), True), 
            StructField("ModifiedTime", TimestampType(), True)
        ])
    schema_role = StructType([
            StructField("Workspace_ID", StringType(), True),   
            StructField("DatasetID", StringType(), True),    
            StructField("RoleName", StringType(), True),
            StructField("RoleModelPermission", StringType(), True),
            StructField("RoleModifiedTime", StringType(), True),    
            StructField("TableName", StringType(), True),
            StructField("TableFilterExpression", StringType(), True),
            StructField("TablemodifiedTime", StringType(), True),
            StructField("Alias", StringType(), True), 
            StructField("ModifiedTime", TimestampType(), True)
        ]) 
    get_all = "Yes"
    memorylakehouseset = set()
    spark_tables = spark.createDataFrame([],schema_tables)
    spark_expressions = spark.createDataFrame([],schema_expressions)
    spark_columns = spark.createDataFrame([],schema_columns)
    spark_measures = spark.createDataFrame([],schema_measures)
    spark_relationship = spark.createDataFrame([],schema_relationships)
    spark_model = spark.createDataFrame([],schema_model)
    spark_roles = spark.createDataFrame([],schema_role)
    datasetlist_table = spark.sql("select WorkspaceID,ID from datasetlist")
    for row in datasetlist_table.collect():
        WorkspaceID = row['WorkspaceID']
        ID = row['ID']
        expressions_df,tables_df,columns_df,measures_df,relationships_df,model_df,roles_df  = get_dataset_lineage(WorkspaceID = WorkspaceID,DatasetID = ID,get_all = get_all)
        spark_tables_stage = spark.createDataFrame(tables_df,schema_tables)
        spark_expressions_stage = spark.createDataFrame(expressions_df,schema_expressions)
        spark_columns_stage = spark.createDataFrame(columns_df,schema_columns)
        spark_measures_stage = spark.createDataFrame(measures_df,schema_measures)
        spark_relationship_stage = spark.createDataFrame(relationships_df,schema_relationships)
        spark_model_stage = spark.createDataFrame(model_df,schema_model)
        spark_roles_stage = spark.createDataFrame(roles_df,schema_role)
        spark_tables = spark_tables.union(spark_tables_stage)
        spark_expressions = spark_expressions.union(spark_expressions_stage)
        spark_columns = spark_columns.union(spark_columns_stage)
        spark_measures = spark_measures.union(spark_measures_stage)
        spark_relationship = spark_relationship.union(spark_relationship_stage)
        spark_model = spark_model.union(spark_model_stage)
        spark_roles = spark_roles.union(spark_roles_stage)

    msg = insert_update_stage_oct(spark_df = spark_tables, oct_table_name = "oct_tables" , on_name = "Dataset_ID", parameter = "No")
    msg = insert_update_stage_oct(spark_df = spark_expressions, oct_table_name = "oct_expression" , on_name = "Dataset_ID", parameter = "No")
    msg = insert_update_stage_oct(spark_df = spark_columns, oct_table_name = "oct_column" , on_name = "Dataset_ID", parameter = "No")
    msg = insert_update_stage_oct(spark_df = spark_measures, oct_table_name = "oct_measures" , on_name = "Dataset_ID", parameter = "No")
    msg = insert_update_stage_oct(spark_df = spark_relationship, oct_table_name = "oct_relationship" , on_name = "DatasetID", parameter = "No")
    msg = insert_update_stage_oct(spark_df = spark_model, oct_table_name = "oct_model" , on_name = "DatasetID", parameter = "No")
    msg = insert_update_stage_oct(spark_df = spark_roles, oct_table_name = "oct_roles" , on_name = "DatasetID", parameter = "No")
    return "Operation Completed"


# In[19]:


def create_datasetlistv1_table():
    ps = spark.read.csv('Files/PowerBIDatasetInfo.csv', header=True)
    ds = spark.sql("select * from datasetlist")
    om = spark.sql("select * from oct_model")
    ps = ps.alias("ps")
    ds = ds.alias("ds")
    om = om.alias("om")
    df = ds.join(ps, col("ds.ID") == col("ps.DatasetId"), "left") \
           .join(om, col("om.DatasetID") == col("ds.ID"), "left")
    df = df.select(
        col("ds.WorkspaceID").alias("WorkspaceID"),
        col("ds.ID").alias("DatasetID"),
        col("ds.Name").alias("Name"),
        col("ds.Alias").alias("ExecuterAlias"),
        col("ds.Info").alias("Info"),
        col("ds.ModifiedTime").alias("ModifiedTime"),
        col("ps.ConfiguredBy").alias("ConfiguredBy"),
        col("ps.IsRefreshable").alias("IsRefreshable"), 
        col("om.createdTimestamp").alias("createdTimeStamp"),
        col("om.Last_Update").alias("LastUpdatedTime"),
        col("om.Last_Schema_Update").alias("LastSchemaUpdateTime"),
        col("om.Last_Processed").alias("LastProcessed")
    )

    df.write.format("delta").mode("overwrite").saveAsTable("datasetlistv1")
    return df


# In[20]:


def save_factocttable():
    factoct= spark.sql("""create or replace table factoct as 
                            select t.Workspace_ID
                                ,t.Dataset_ID
                                ,t.Mode
                                ,t.Source_Type
                                ,t.Expression
                                ,t.Table_Name
                                ,t.Source_Table_Name
                                ,s.InitialWorkspaceID
                                ,s.InitialLakehouseID
                                ,s.InitialLakehouseName
                                ,s.InitialLakehouseLink
                                ,s.Initial_Path
                                ,s.Initial_Shortcut_Name
                                ,s.FinalSourceWorkspaceID
                                ,s.FinalSourceLakehouseID
                                ,s.FinalSourceLakehouseName
                                ,s.FinalSourceLakehouseLink
                                ,s.Final_Source_Path
                                ,s.Source_ADLS_Path
                                ,s.OSOTLakehouseFlag
                                ,s.SourceLakehouseType
                                ,s.Source_Area_Domain
                                ,t.Alias as ExecutorAlias
                                ,t.ModifiedTime as ExecutorModifiedTIme
                                ,CASE WHEN instr(t.source_table_name, '.') > 0 THEN split(t.source_table_name, '\\.')[1] 
                                      ELSE t.source_table_name END AS source_table_wo_schema 
                         from oct_tables t 
                         left join oct_parameters p on lcase(trim(t.Dataset_ID)) = lcase(trim(p.DatasetID))
                         left join oct_shortcuts s on lcase(trim(t.Source_Table_Name)) = lcase(trim(s.Initial_Shortcut_Name)) 
                         and lcase(trim(p.LakehouseID)) = lcase(trim(s.InitialLakehouseID))""")
    return factoct


# In[ ]:


def refresh_dataset():
    try:
        refreshworkspace = "OCT-Dev"
        refreshdataset = "OCT Report"
        tmsl_model_refresh_script = {
            "refresh": {
                "type": "full",
                "objects": [
                    {
                        "database": refreshdataset,
                    }
                ]
            }
        }
        fabric.execute_tmsl(workspace=refreshworkspace, script=tmsl_model_refresh_script)
        msg = "refresh is triggered"
    except Exception as e: 
        msg = e
    return msg


# In[35]:


def run(WorkspaceID,DatasetID,LakehouseWorkspaceID = "NA",LakehouseID = "NA",force_reload = False):
    try:
        expressions_df = tables_df = columns_df = measures_df = relationships_df = model_df = roles_df = shortcuts_df = None
        Alias = get_executer_alias()
        ModifiedTime = get_modifiedtimestamp()
        get_workspace_name(WorkspaceID = WorkspaceID,get_all = "No")
        get_dataset_name(WorkspaceID = WorkspaceID,DatasetID = DatasetID,get_all = "No")
        expressions_df,tables_df,columns_df,measures_df,relationships_df,model_df,roles_df = get_dataset_lineage(WorkspaceID = WorkspaceID,DatasetID = DatasetID,get_all = "No")
        if isinstance(tables_df, pd.DataFrame):
            tables_df = spark.createDataFrame(tables_df)
        distinct_modes = tables_df.select("Mode").distinct().collect()
        tables_df_cleaned = tables_df.withColumn("Mode", F.lower(F.col("Mode")))
        directlake_check = tables_df_cleaned.filter(F.col("Mode") == "directlake").count()
        if directlake_check == 0 and LakehouseWorkspaceID == "NA" and LakehouseID == "NA":
            print("Warning:Since it is not directlake mode model, we require Lakehouse ID & Lakehouse Workspace details to process the shortcuts.")
        elif directlake_check >= 1 and LakehouseWorkspaceID == "NA" and LakehouseID == "NA":
            print("Capaturing the lakehouse lineage details from model")
        else:
            print("Capturing the lakehouse details from provided LakehouseWorkspaceID and LakehouseID")
        if LakehouseID == "NA" or LakehouseWorkspaceID == "NA":
            df_parameter = fabric.evaluate_dax(dataset= DatasetID,workspace = WorkspaceID,dax_string = """select [rootlocation] from $SYSTEM.TMSCHEMA_DELTA_TABLE_METADATA_STORAGES""")
            if len(df_parameter)==0:
                LakehouseID = "NA"
                LakehouseWorkspaceID = "NA"
            else:
                df_parameter[['LakehouseWorkspaceID', 'LakehouseID']] = df_parameter['rootlocation'].str.extract(r'^/([^/]+)/([^/]+)/')
                df_parameter = df_parameter[['LakehouseWorkspaceID', 'LakehouseID']].drop_duplicates()
                LakehouseWorkspaceID = df_parameter['LakehouseWorkspaceID'][0]
                LakehouseID = df_parameter['LakehouseID'][0]
        get_workspace_name(WorkspaceID = LakehouseWorkspaceID,get_all = "No")    
        get_lakehouse_name(WorkspaceID = LakehouseWorkspaceID,LakehouseID= LakehouseID,get_all = "No")
        parameterschema = StructType([
        StructField("WorkspaceID", StringType(), True),
        StructField("DatasetID", StringType(), True),
        StructField("LakehouseWorkspaceID", StringType(), True),
        StructField("LakehouseID", StringType(), True),
        StructField("Alias", StringType(), True),
        StructField("ModifiedTime", TimestampType(), True)
        ])
        shortcuts_df, errors, memorylakehouseset = get_lakehouse_shortcuts(WorkspaceID = LakehouseWorkspaceID, LakehouseID= LakehouseID , memorylakehouseset = set(),get_all = "No",force_reload=force_reload)
        parameters = spark.createDataFrame([(WorkspaceID, DatasetID, LakehouseWorkspaceID, LakehouseID, Alias, ModifiedTime)],schema=parameterschema)
        msg = insert_update_stage_oct(spark_df = parameters, oct_table_name = "oct_parameters" , on_name = "DatasetID", parameter = "No")
        create_datasetlistv1_table()
        save_factocttable()
        refresh_dataset()
    except Exception as e:
        print(e)
    return expressions_df,tables_df,columns_df,measures_df,relationships_df,model_df,roles_df,shortcuts_df


# In[25]:


def run_pipeline():
    spark.sql("delete from oct_errors")
    Alias = get_executer_alias()
    ModifiedTime = get_modifiedtimestamp()
    get_all_dataset_lineage()
    get_all_lakehouse_shortcuts()
    datasetlist_spark = spark.sql("select * from datasetlist")
    schema = StructType([StructField("WorkspaceID", StringType(), True),
                         StructField("DatasetID", StringType(), True),
                         StructField("LakehouseWorkspaceID", StringType(), True),
                         StructField("LakehouseID", StringType(), True),
                         StructField("Alias", StringType(), True), 
                         StructField("ModifiedTime", TimestampType(), True)
                         ])
    df_parameters = spark.createDataFrame([], schema)
    for row in datasetlist_spark.collect():
        WorkspaceID = row['WorkspaceID'] 
        DatasetID = row['ID'] 
        try:
            df_parameter = fabric.evaluate_dax(dataset= DatasetID,workspace = WorkspaceID,dax_string = """select [rootlocation] from $SYSTEM.TMSCHEMA_DELTA_TABLE_METADATA_STORAGES""")
        except Exception as e:
            #print(e)
            df_parameter = []
        if len(df_parameter)==0: 
            df_parameter = spark.createDataFrame([(WorkspaceID, DatasetID,"NA", "NA",Alias,ModifiedTime)], schema)
            df_parameters = df_parameters.union(df_parameter)
        else:
            df_parameter[['LakehouseWorkspaceID', 'LakehouseID']] = df_parameter['rootlocation'].str.extract(r'^/([^/]+)/([^/]+)/')
            df_parameter = df_parameter[['LakehouseWorkspaceID', 'LakehouseID']].drop_duplicates()
            df_parameter['WorkspaceID'] = WorkspaceID
            df_parameter['DatasetID'] = DatasetID
            df_parameter['Alias'] = Alias
            df_parameter['ModifiedTime'] = ModifiedTime
            df_parameter = df_parameter[['WorkspaceID','DatasetID','LakehouseWorkspaceID', 'LakehouseID','Alias','ModifiedTime']]
            df_parameter = spark.createDataFrame(df_parameter)
            df_parameters = df_parameters.union(df_parameter)
    msg = insert_update_stage_oct(spark_df = df_parameters, oct_table_name = "oct_parameters" , on_name = "DatasetID", parameter = "No")
    create_datasetlistv1_table()
    save_factocttable()
    return "Operation Completed"

