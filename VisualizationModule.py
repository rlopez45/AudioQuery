import pandas as pd
import seaborn as sns
import warnings
import matplotlib.pyplot as plt
import itertools

# Up to date version

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
        self.col_lists = list(self.df.columns)
        self.plt = plt
        self.chart_dict = {1: 'bar', 2: 'horizontal bar', 3: 'scatter', 4: 'histogram', 5: 'line'}
        self.possible_chart_dict = dict()
        #self.possible_column_combination_dict = dict()
        self.modify_dict = {1: 'Add Title', 2: 'Switch X, Y axises'}
        self.dataset = None
        self.visual_count = 0

    
    def visualization_receommendation(self):
        possible_chart_list = []
        chart_flag_dict = {'bar': 0, 'horizontal bar': 0, 'line': 0, 'histogram': 0, 'scatter' : 0}
        types_grouped  = self.df.columns.to_series().groupby(self.df.dtypes).groups
        type_dict ={k.name: v for k, v in types_grouped.items()}   
        
        # if dataframe contains time type date, could do "line"
        if ( ('datetime64[ns]' in type_dict) |('datetime64[ms]' in type_dict) | ('datetime64[D]' in type_dict)) :
            chart_flag_dict['line'] = 1

        # if dataframe includes at leaest on numerical: 
        if ( ('int64' in type_dict) |('float64' in type_dict)) :
            
            # if dataframe only has one column, then do 'histogram'
            if(len(self.col_lists)==1):
                chart_flag_dict['histogram'] = 1
        
            # if dataframe also one as category type, then could do 'bar' or 'horizontal bar'
            if (('object' in type_dict)) :
                chart_flag_dict['bar'] = 1
                chart_flag_dict['horizontal bar'] = 1   
       
            if((len(type_dict.get('int64','empty')) + len(type_dict.get('float64','empty'))) > 1):
                chart_flag_dict['scatter'] = 1
        
        for chart, flag in chart_flag_dict.items():  
            if (flag == 1):
                possible_chart_list.append(chart)
        
        # chart_typt_dic is predefined, so the potential chart list should be matched the predefinned chart_type_dic
        for k, v in self.chart_dict.items():
            for chart in possible_chart_list:
                if v == chart: 
                    self.possible_chart_dict[k] = v

        return self.possible_chart_dict

    
    def chart_to_columns_recommendation(self, ctype):
    
        if ctype == 'bar':
            
            bar_col_list = []
            sub_col_pairs = list(itertools.combinations(self.col_lists, 2))

            for s in sub_col_pairs:
                sub_df = self.df[list(s)]   
                sub_df_col_types = sub_df.dtypes
                x_axis = ''
                y_axis = ''

                for t in sub_df_col_types: 
                    if t in ['object']:
                        x_axis = sub_df_col_types[sub_df_col_types==t].index[0]
                    if t in ['int64','float64']:
                        y_axis = sub_df_col_types[sub_df_col_types==t].index[0]
             
                if (x_axis != '') & (y_axis != ''):
                    bar_col_list.append([x_axis, y_axis])  

            return bar_col_list
        

        if ctype == 'horizontal bar':

            hbar_col_list =[]
            sub_col_pairs = list(itertools.combinations(self.col_lists, 2))

            for s in sub_col_pairs:
                sub_df = self.df[list(s)]   
                sub_df_col_types = sub_df.dtypes
                x_axis = ''
                y_axis = ''

                for t in sub_df_col_types: 
                    if t in ['object']:
                        y_axis = sub_df_col_types[sub_df_col_types==t].index[0]
                    if t in ['int64','float64']:
                        x_axis = sub_df_col_types[sub_df_col_types==t].index[0]
             
                if (x_axis != '') & (y_axis != ''):
                    hbar_col_list.append([x_axis, y_axis])  

            return hbar_col_list
            # self.possible_column_combination_dict = {v: k for v, k in enumerate(hbar_col_list)}

        
        if ctype == 'scatter':

            scatter_col_list = []
            sub_col_pairs = list(itertools.combinations(self.col_lists, 2))
            
            for s in sub_col_pairs:
                sub_df = self.df[list(s)]
                sub_df_col_types = sub_df.dtypes
                
                x_axis = ''
                y_axis = ''
        
                c = 0
                for t in col_types: 
                    if t in ['object']:
                        return 0
                    if t in ['int64','float64']:
                        c = c+1          
            
                if (c==2):
                x_axis = self.col_lists[0]
                y_axis = self.col_lists[1]
        
            #TODO:
                if (x_axis != '') & (y_axis != ''):
                    scatter_col_list.append([x_axis, y_axis])

             return scatter_col_list





    def dataset_to_visualization(self, column_combo, ctype):
                
        sub_df = self.df[column_combo]

        tag = 0
        if ctype == 'bar':
            tag = self.make_bar(sub_df)
            

        if ctype == 'horizontal bar':
            tag = self.make_horizontal_bar(sub_df)
 
        
        if ctype == 'line':
            tag = self.make_line()

        if ctype == 'histogram':
            tag = self.make_histogram()
       

        if ctype == 'scatter':
            tag = self.make_scatter(sub_df)
            

        if tag == 1: 
            print("\nStep 3: Visualization Generated Succeefully!")
        if tag == 0:
            print("\nStep 3: visulization Generating failed :(")


    def make_bar(self, test_df):
        col_lists = list(test_df.columns)
        col_types = test_df.dtypes
        x_axis = ''
        y_axis = ''
        
        for t in col_types: 
            if t in ['object']:
                x_axis = col_types[col_types==t].index[0]
            if t in ['int64','float64']:
                y_axis = col_types[col_types==t].index[0]
             
        if (x_axis == '') | (y_axis == ''):
            return 0  

        else:
            print("Columns for bar chart: {}".format(col_lists))
            sns.set(style="whitegrid")
            f, axes = plt.subplots(figsize = (18,7))
            sns.barplot(x=x_axis, y=y_axis, data=test_df)
            plt.savefig('bar.png')
            return 1   

    
    def make_horizontal_bar(self, test_df):
        
        col_lists = list(test_df.columns)
        col_types = test_df.dtypes
        x_axis = ''
        y_axis = ''

        for t in col_types: 
            if t in ['object']:
                y_axis = col_types[col_types==t].index[0]
            if t in ['int64','float64']:
                x_axis = col_types[col_types==t].index[0]
        
        if (x_axis == '') | (y_axis == ''):
            return 0  

        else:    
            print("\nColumns for horizontal bar chart: {}".format(col_lists))
            sns.set(style="whitegrid")
            f, axes = plt.subplots(figsize = (18,7))
            sns.barplot(x=x_axis, y=y_axis, data=test_df)

            plt.savefig('horizontal_bar.png')
            return 1 

    def make_scatter(self, test_df, count):
        
        col_lists = list(test_df.columns)
        col_types = test_df.dtypes
        x_axis = ''
        y_axis = ''
        
        c = 0
        for t in col_types: 
            if t in ['object']:
                return 0
            if t in ['int64','float64']:
                c = c+1          
        if (c==2):
            x_axis = self.col_lists[0]
            y_axis = self.col_lists[1]
        
        if (x_axis == '') | (y_axis == ''):
            return 0  

        else:     
            print(">>>\nColumns for simple scatter plot are: {}".format(col_lists))
            sns.set(style="whitegrid")
            sns.relplot(x=x_axis, y=y_axis, data=test_df)
            plt.savefig('scatter_{}.png'.format(count))
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
            plt.savefig('line.png')

            return 1
    
   
    def make_histogram(self):
        
        col_types = self.df.dtypes
        
        if (len(self.col_lists)!=1):
            print('>>> Only one numerical column is allowed for simple histogram chart, please check :)')
            return 0
        
        else: 
            
            print("Columns for histogram chart are: {}".format(self.col_lists))
            sns.set(style="whitegrid")
            f, axes = plt.subplots(figsize = (18,7))
            sns.distplot(self.df) 
            plt.savefig('histogram.png')
            return 1

    


    # TODO: finish the model
    def make_grouped_bar(self):
        pass

    def visualization_to_modification(self):
    
        self.plt.savefig('modfied_chart_test.png')

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
    agg_fn = {
            'CAND_ID': 'count',
            'TTL_RECEIPTS': 'sum',
            'TTL_DISB': 'sum'}    
    multiple_bar = cand_summary.groupby(['PTY_AFFILIATION']).agg(agg_fn).reset_index()
    #module start here
    vm = VisualizationModule(multiple_bar)
    type_dict = vm.visualization_receommendation()
    print('The potential chart types for this dataset: {}'.format(type_dict))
    type_input = input("Step 1: Which chart visualization you want? provide the number\n>>>")

    #print("\n>>> Your current input are: {}".format(type_input))
    
    # Add similarity module later to mapping the input to types of charts
    chart_id = int(type_input)
    print('Your choice chart is: {}\n'.format(vm.possible_chart_dict[chart_id]))
    potential_columns_combinations = vm.chart_to_columns_recommendation(vm.possible_chart_dict[chart_id])
    print (potential_columns_combinations)
    
    columns_input = input("Step 2: which columns combinations you want? choose the number\n>>>")

    print(vm.possible_column_combination_dict[int(columns_input)])
    print("Generating the visualization .....")
    vm.dataset_to_visualization(vm.possible_column_combination_dict[int(columns_input)], vm.possible_chart_dict[chart_id])
    
    #vm.visualization_to_modification()
    

