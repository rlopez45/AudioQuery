class VisualizationModule(object):
	'''
	Instantiates a VisualizationModule

	inputs: 
	data:  pandas dataframe
	ctype: request chart type

	returns:
	VM object


	TODO: 1) Use input column number, column dtype to make judegement for potential chart type (might not be one-to-one relationship, may need better methods)
#       potentially a decision trees with several trees
#       2) make judgment on columns types and assign to right axis (should have decent generating rules) 
#       3) take a look for reference on RawGraph and data2vis project 
	'''

	def __init__(self, data, ctype): 
		self.source_df= data
		self.ctype = ctype


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