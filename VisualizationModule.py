import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
import warnings


class VisualizationModule(object):
	'''
	Instantiates a VisualizationModule

	inputs: 
	data:  whole pandas dataframe 
	ctype: request chart type

	returns:
	VM object

	'''

	def __init__(self, data, ctype): 
		self.data= data
		self.ctype = ctype

    # TODO: based on whole dataset, make suggesstions for potential chart types based on rules. 
    def visualization_suggestion(df):
    
        # create a chart possible dictionary
        potential_chart_list = []
        chart_dict = {'bar': 0, 'horizontal bar': 0, 'line': 0, 'histogram':0}
    
        types_grouped  = df.columns.to_series().groupby(df.dtypes).groups
        type_dict ={k.name: v for k, v in types_grouped.items()}
        
        # TODO: need to check all different data type for numerical, category data
        # TODO: Adding more chart type detection suggestion
        if ( ('int64' in type_dict) |('float64' in type_dict)) :
            chart_dict['histogram'] = 1
        
            # TODO: need to add method for detect datatime type for simple line chart
            if (('object' in type_dict)) :
                chart_dict['bar'] = 1
                chart_dict['horizontal bar'] = 1    
        
        # Adding possible chart types into output list
        for chart, flag in chart_dict.items():  
            if (flag == 1):
                potential_chart_list.append(chart)
    
        # Print out chart suggestions
        if (len(potential_chart_list) != 0):
            print ("\nThe potential chart types for this dataset will be: {}".format(potential_chart_list))
            return 1
    
        else: 
            print ("\nThere is no available chart type for this dataset.")
            return 0

	
    def dataset_to_visualization(source_df, ctype):
		
		# detect  dataframe columnes types and create list of the type. 
		tag = 0 
		col_types  = df.columns.to_series().groupby(df.dtypes).groups
   	 	c = {k.name: v for k, v in col_types.items()}
    	type_list  = list(c.keys())
    	if ctype == 'bar':
    		tag = make_bar(source_df)	

    	if ctype == 'line':
    		tag = make_line(source_df)

    	if ctype == 'histogram':
    		tag = make_histogram(source_df)

    	if ctype == 'hbar':
    		tag = make_horizontal_bar(source_df)

   
    def make_bar(source_df):
        col_lists = list(source_df.columns)
        col_types = source_df.dtypes
        x_axis = ''
        y_axis = ''

        if (len(col_lists)!=2):
            print('Only two columns are allowed for simple bar chart, please check.')
        else:

            for t in col_types: 
                if t in ['object']:
                    x_axis = col_types[col_types==t].index[0]
                if t in ['int64','float64']:
                    y_axis = col_types[col_types==t].index[0]
                
        print("Columns for simple bar chart are: {}".format(col_lists))
        sns.set(style="whitegrid")
        f, axes = plt.subplots(figsize = (18,7))
        sns.barplot(x=x_axis, y=y_axis, data=source_df) 

    
    def make_horizontal_bar(source_df):
        col_lists = list(source_df.columns)
        col_types = source_df.dtypes
        x_axis = ''
        y_axis = ''
        if (len(col_lists)!=2):
            print('Only two columns are allowed for simple bar chart, please check.')
        else: 
            for t in col_types: 
                if t in ['object']:
                    y_axis = col_types[col_types==t].index[0]
                if t in ['int64','float64']:
                    x_axis = col_types[col_types==t].index[0]
                
        print("Columns for horizontal bar chart are: {}".format(col_lists))
        sns.set(style="whitegrid")
        f, axes = plt.subplots(figsize = (18,7))
        sns.barplot(x=x_axis, y=y_axis, data=source_df) 



    #TODO: not finished, add auto detect datetime column even in 'object' or 'int' format
	def make_line(source_df):
    	col_lists = list(source_df.columns)
        col_types = source_df.dtypes
        x_axis = ''
        y_axis = ''
        if (len(col_lists)!=2):
            print('Only two columns are allowed for simple line chart, please check.')
        else: 
            for t in col_types: 
                if t in ['object']:
                    y_axis = col_types[col_types==t].index[0]
                if t in ['int64','float64']:
                    x_axis = col_types[col_types==t].index[0]
                
        print("Columns for simple line chart are: {}".format(col_lists))
        sns.set(style="whitegrid")
        f, axes = plt.subplots(figsize = (18,7))
        sns.lineplot(x=col_lists[1], y=col_lists[0], data=source_df) 

    
   
    def make_histogram(source_df):
        col_lists = list(source_df.columns)
        col_types = source_df.dtypes
        
        if (len(col_lists)>1):
            print('Only one column is allowed for simple histogram chart, please check.')
        else: 
            print("Columns for simple hi chart are: {}".format(col_lists))
            sns.set(style="whitegrid")
            f, axes = plt.subplots(figsize = (18,7))
            sns.distplot(source_df) 


    # TODO: not finishied, further changes and rules
	def make_grouped_bar(source_df):
		pass
