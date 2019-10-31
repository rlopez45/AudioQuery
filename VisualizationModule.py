class VisualizationModule(object):
	'''
	Instantiates a VisualizationModule

	inputs: 
	data:  pandas dataframe
	ctype: request chart type

	returns:
	VM object


	TLearning Objects:

	Step 1 (optional): select a subset of fields to focus on for creating data visualization: (rules like some of the columns cannot be together for visualizations)
	Step 2: dectect subset's types (numeric, string, temporal, ordinal, categorical)
	Step 3: based on chart type to decide select columns 
	

	'''

	def __init__(self, data, ctype): 
		self.data= data
		self.ctype = ctype



	def axis_from_data (df, ctype):
		
		# detect  dataframe columnes types and create list of the type.  
		col_types  = df.columns.to_series().groupby(df.dtypes).groups
   	 	c = {k.name: v for k, v in col_types.items()}
    	type_list  = list(c.keys())

    	if ctype == 'bar': 
    		pass 

    	if ctype == 'groupbar':
    		pass

    		
	def chart_columns (ctype): 
		if ctype == 'bar': 
			tag = Query_SimpleBar (source_df)

		if ctype == 'groupbar':
			tag = Query_GroupedBar(source_df)

		if tag == 1:
			print ('Visulization Generated!')

	def Query_SimpleBar(source_df):
		col_list = list(source_df.columns)
		if (len(col_list)!=2):
			print('Only two columns are allowed for Simple Bar Chart.')
			return 0
		else:
			print(col_list)
			sns.set(style="whitegrid")
			f, axes = plt.subplots(figsize = (18,7))
			sns.barplot(x=col_list[1], y=col_list[0], data=source_df) 
			return 1

	def Query_GroupedBar(source_df):
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