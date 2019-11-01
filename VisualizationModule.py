class VisualizationModule(object):
	'''
	Instantiates a VisualizationModule

	inputs: 
	data:  pandas dataframe
	ctype: request chart type

	returns:
	VM object

	'''

	def __init__(self, data, ctype): 
		self.data= data
		self.ctype = ctype


	def data_to_visualization(df, ctype):
		
		# detect  dataframe columnes types and create list of the type. 
		tag = 0 
		col_types  = df.columns.to_series().groupby(df.dtypes).groups
   	 	c = {k.name: v for k, v in col_types.items()}
    	type_list  = list(c.keys())
    	if ctype == 'bar':
    		tag = make_bar(df)	

    	if ctype == 'line':
    		tag = make_line(df)

    	if ctype == 'histogram':
    		tag = make_histogram(df)

    	if ctype == 'hbar':
    		tag = make_horizontal_bar(df)

   
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
		col_list = list(source_df.columns)
		if (len(col_list)!=3):
			print('Only three columns are allowed for Simple Bar Chart.')
			return 0
		else:
			print(col_list)
			sns.set(style="whitegrid")
			f, axes = plt.subplots(figsize = (18,7))
			sns.barplot(y=col_list[2], hue=col_list[1], x=col_list[0], data=source_df)
			return 1