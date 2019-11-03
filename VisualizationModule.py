import pandas as pd
import seaborn as sns
import warnings
import matplotlib.pyplot as plt

'''
    Instantiates a VisualizationModule

    inputs: 
    data:  whole pandas dataframe 
    ctype: request chart type

    returns:
    VM object

    '''

class VisualizationModule(object):


    def __init__(self, df):
        
        self.df= df
        self.type_dict = dict()
        self.col_lists = list(self.df.columns)
    
    def visualization_suggestion(self):
        potential_chart_list = []
        chart_dict = {'bar': 0, 'horizontal bar': 0, 'line': 0, 'histogram': 0, 'scatter' : 0}
        types_grouped  = self.df.columns.to_series().groupby(self.df.dtypes).groups
        self.type_dict ={k.name: v for k, v in types_grouped.items()}
        
        
        # TODO: Add more chart type detection suggestion
        # TODO: need to add smart methods for detect datatime type for simple line chart
        if ( ('datetime64[ns]' in self.type_dict) |('datetime64[ms]' in self.type_dict) | ('datetime64[D]' in self.type_dict)) :
            chart_dict['line'] = 1

        if ( ('int64' in self.type_dict) |('float64' in self.type_dict)) :
            
            if(len(self.col_lists)==1):
                chart_dict['histogram'] = 1
        
            
            if (('object' in self.type_dict)) :
                chart_dict['bar'] = 1
                chart_dict['horizontal bar'] = 1    
        
        for chart, flag in chart_dict.items():  
            if (flag == 1):
                potential_chart_list.append(chart)
    
        # Print out chart suggestions
        if (len(potential_chart_list) != 0):
            print (">>> The potential chart types for this dataset could be:\n\n{}".format(potential_chart_list))
            return 1
    
        else: 
            print (">>> There is no available chart type for this dataset.")
            return 0

	
    def dataset_to_visualization(self, ctype):
		
		
        tag = 0 
        col_types  = self.df.columns.to_series().groupby(self.df.dtypes).groups
        c = {k.name: v for k, v in col_types.items()}
        type_list  = list(c.keys())
        if ctype == 'bar':
            tag = self.make_bar()	
        
        if ctype == 'line':
            tag = self.make_line()

        if ctype == 'histogram':
            tag = self.make_histogram()

        if ctype == 'horizontal bar':
            tag = self.make_horizontal_bar()

        if tag == 1: 
            print("\n>>> visualization Generating Succeed!")
        if tag == 0:
            print("\n>>> visulization Generating failed :(")

    def make_bar(self):
        
        col_types = self.df.dtypes
        x_axis = ''
        y_axis = ''

        if (len(self.col_lists)!=2):
            print('>>> Only two columns are allowed for simple bar chart, please check :)')
            return 0
        else:

            for t in col_types: 
                if t in ['object']:
                    x_axis = col_types[col_types==t].index[0]
                if t in ['int64','float64']:
                    y_axis = col_types[col_types==t].index[0]
                
            print("\nColumns for simple bar chart are: {}".format(self.col_lists))
            sns.set(style="whitegrid")
            f, axes = plt.subplots(figsize = (18,7))
            sns.barplot(x=x_axis, y=y_axis, data=self.df) 
            plt.show(block=True)
            plt.savefig('bar_test.png')
            return 1

    
    def make_horizontal_bar(self):
        
        col_types = self.df.dtypes
        x_axis = ''
        y_axis = ''
        if (len(self.col_lists)!=2):
            print('>>> Only two columns are allowed for simple bar chart, please check :)')
        else: 
            for t in col_types: 
                if t in ['object']:
                    y_axis = col_types[col_types==t].index[0]
                if t in ['int64','float64']:
                    x_axis = col_types[col_types==t].index[0]
                
            print("\nColumns for horizontal bar chart are: {}".format(self.col_lists))
            sns.set(style="whitegrid")
            f, axes = plt.subplots(figsize = (18,7))
            sns.barplot(x=x_axis, y=y_axis, data=self.df)

            plt.savefig('horizontal_bar_test.png')
            return 1 

    # TODO: fix the bug here
    # TODO: Adjust xaxis range
    def make_line(self):
        #
        col_types = self.df.dtypes
        x_axis = ''
        y_axis = ''
        if (len(self.col_lists)!=2):
            print('\n>>> Only two columns are allowed for simple line chart, please check :)')
            return 0
        else: 
            for t in col_types: 
                
                if t in ['datetime64[ns]','datetime64[D]', 'datetime64[ms]']:
                    x_axis = col_types[col_types==t].index[0]
                if t in ['int64','float64']:
                    y_axis = col_types[col_types==t].index[0]
                
            print("\nColumns for simple line chart are: {}".format(self.col_lists))
            sns.set(style="whitegrid")
            #f, axes = plt.subplots(figsize = (18,7))
            sns.lineplot(x=x_axis, y=y_axis, data=self.df) 
            plt.savefig('line_test.png')

            return 1
    
   
    def make_histogram(self):
        
        col_types = self.df.dtypes
        
        if (len(self.col_lists)!=1):
            print('>>> Only one numerical column is allowed for simple histogram chart, please check :)')
            return 0
        
        else: 
            
            print(">>>\nColumns for simple histogram chart are: {}".format(self.col_lists))
            sns.set(style="whitegrid")
            f, axes = plt.subplots(figsize = (18,7))
            sns.distplot(self.df) 
            plt.savefig('histogram_test.png')
            return 1

    def make_scatter(self):
        
        col_types = self.df.dtypes
        x_axis = ''
        y_axis = ''
        if (len(col_lists)!=2):
            print('>>>Only two columns numerical are allowed for simple scatter plot, please check :)')
            return 0
        else: 
            c = 0
            for t in col_types: 
                if t in ['int64','float64']:
                    c = c+1          
            if (c==2):
                x_axis = col_lists[0]
                y_axis = col_lists[1]
                
            print(">>>\nColumns for simple scatter plot are: {}".format(self.col_lists))
            sns.set(style="whitegrid")
            sns.relplot(x=x_axis, y=y_axis, data=self.df); 


    # TODO: finish the model
    def make_grouped_bar(self):
        pass


# finished the initiated functions.
if __name__ == "__main__":

    # design test
    dist_pop = pd.read_csv("data/dist_pop.txt", delimiter="|")
    candidates = pd.read_csv("data/candidate.txt", delimiter="|")
    cand_summary = pd.read_csv("data/cand_summary.txt", delimiter="|")
    
    bar_test_df = dist_pop[['state','population']].groupby('state').sum().reset_index()
    line_test_df = candidates.merge(cand_summary, on='CAND_ID', how='left')[['CAND_ELECTION_YR','TTL_RECEIPTS']].groupby('CAND_ELECTION_YR').sum().reset_index()
    line_test_df['CAND_ELECTION_YR'] =  pd.to_datetime(line_test_df['CAND_ELECTION_YR'])
    hist_test_df = bar_test_df[['population']]
    scatter_test_df = cand_summary[['TTL_RECEIPTS','TTL_DISB']]

    #module start here
    vm = VisualizationModule(hist_test_df)
    vm.visualization_suggestion()
    type_input = input("\n>>> Which chart visualization you want?")

    print("\n>>> Your current input are: {}".format(type_input))
    
    # Add similarity module later to mapping the input to types of charts
    chart_type = type_input
    print('\n>>> Your choice chart is: {}'.format(chart_type))
    print(">>> Generating initial visualization >>>")

    vm.dataset_to_visualization(chart_type)
    #vmObject.make_bar(bar_test_df)

