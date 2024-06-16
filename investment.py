import tkinter as tk
import random
from matplotlib import pyplot as plt
from datetime import datetime

from global_variables import FONTS, DEFAULT_PARAMS, COLORS, GRAPH_WIDTH, GRAPH_HEIGHT, SCREEN_HORIZONTAL_RES, random_list

class investment(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        self.controller = controller

        self.TITLE_FONT = FONTS['TITLE_FONT']
        self.HEAVY_BOLD_FONT = FONTS['HEAVY_BOLD_FONT']
        self.DEFAULT_FONT = FONTS['DEFAULT_FONT']

        # self.start = time.time()
        self.INITIAL_CONTRIBUTION = DEFAULT_PARAMS['INITIAL_CONTRIBUTION']
        self.YEARLY_CONTRIBUTION = DEFAULT_PARAMS['YEARLY_CONTRIBUTION']
        self.INFLATION_PERCENT = DEFAULT_PARAMS['INFLATION_PERCENT']
        self.INTEREST_EARNED_PERCENT = DEFAULT_PARAMS['INTEREST_EARNED']
        self.YEAR_START = datetime.now().year
        self.YEAR_END = datetime.now().year+14

        self.SPECIFIC_YEAR_HEIGHT = 28
        self.SPECIFIC_YEAR_WIDTH = 20
        self.OVERVIEW_HEIGHT = 17
        self.OVERVIEW_WIDTH = 20

        self.NEGATIVE_BAL_COLOR = COLORS['NEGATIVE_BAL_COLOR']
        self.POSITIVE_BAL_COLOR = COLORS['POSITIVE_BAL_COLOR']
        self.ALT_HIGHLIGHT = COLORS['ALT_HIGHLIGHT']
        self.INFLATION_GRAPH_COLOR = COLORS['INFLATION_GRAPH_COLOR']

        # self.GRAPH_SIZE = PLOT_SIZE

        self.investment_growth = []

        # used a frame to draw a horizontal line to partition areas of the GUI

        self.Separator_title = tk.Frame(self, bd=1, relief='flat', height=2, bg='black')
        self.Separator_title.grid(row=1, column=0, columnspan=6, sticky='ew', padx=(10,10), pady=(5, 5))

        self.Separator_overview = tk.Frame(self, bd=1, relief='flat', height=2, bg='black')
        self.Separator_overview.grid(row=9, column=0, columnspan=2, sticky='ew',padx=(10,10), pady=(10, 2))

        self.create_title()
        self.create_labels_and_entries()
        self.create_graph_check_box()
        self.create_submit_button()
        self.create_reset_button()
        self.create_overview_box()
        self.create_specific_year_box()

        self.bind("<Return>", lambda event: self.enter_to_submit())
        self.bind("r", lambda event: self.r_to_reset())
        self.bind("<Tab>", lambda event: self.tab_to_switch())

    def enter_to_submit(self, event=None):
        self.submit()

    def r_to_reset(self, event=None):
        self.reset()

    def tab_to_switch(self, event=None):
        self.master.show_frame('retirement')

    def create_title(self):

        page_name = tk.Label(self, text="Investment Calculator", font=self.TITLE_FONT)
        page_name.grid(row=0, column=0, columnspan=2, sticky="news",padx=(10, 10), pady=(5, 2))

        switch_button = tk.Button(self, text="Retirement", font=self.HEAVY_BOLD_FONT, command=lambda: [self.controller.show_frame('retirement'), plt.close(), self.controller.title(f'Retirement Calculator')])
        switch_button.grid(row=0, column=2, columnspan=1, sticky="ns", padx=(0,0), pady=(5, 2))

        switch_button.bind("<Enter>", self.controller.on_hover)
        switch_button.bind("<Leave>", self.controller.on_leave)

    def create_labels_and_entries(self):

        def format_input(*args):
            starting_balance = starting_balance_var.get().replace(',', '')  # remove existing commas
            yearly_contribution = yearly_contribution_var.get().replace(',', '')
            if starting_balance or yearly_contribution:
                try:
                    number = int(starting_balance)  # convert to integer
                    formatted = "{:,}".format(number)  # format with commas
                    starting_balance_var.set(formatted)  # update the StringVar

                    number_2 = int(yearly_contribution)  # convert to integer
                    formatted_2 = "{:,}".format(number_2)  # format with commas
                    yearly_contribution_var.set(formatted_2)  # update the StringVar
                except ValueError:
                    pass  # not a valid integer, ignore

        starting_balance_var = tk.StringVar()
        starting_balance_var.trace_add('write', format_input)

        yearly_contribution_var = tk.StringVar()
        yearly_contribution_var.trace_add('write', format_input)

        self.initial_contribution_label = tk.Label(self, text=' Initial Investment:', font=self.DEFAULT_FONT)
        self.initial_contribution_label.grid(row=2, sticky='w', padx=(1, 1), pady=(1, 1))
        self.initial_contribution_entry = tk.Entry(self, textvariable=starting_balance_var, font=self.DEFAULT_FONT)            
        self.initial_contribution_entry.insert(0, "{:,}".format(self.INITIAL_CONTRIBUTION))            
        self.initial_contribution_entry.grid(row=2, column=1, sticky='ew', padx=(20, 10), pady=(1, 1))

        self.yearly_contribution_label = tk.Label(self, text=' Yearly Cashflow:', font=self.DEFAULT_FONT)
        self.yearly_contribution_label.grid(row=3, sticky='w', padx=(1, 1), pady=(1, 1))
        self.yearly_contribution_entry= tk.Entry(self, textvariable=yearly_contribution_var, font=self.DEFAULT_FONT)
        self.yearly_contribution_entry.insert(0, "{:,}".format(self.YEARLY_CONTRIBUTION))
        self.yearly_contribution_entry.grid(row=3, column=1, sticky='ew', padx=(20, 10), pady=(1, 1))

        self.inflation_label = tk.Label(self, text=' Inflation %:', font=self.DEFAULT_FONT)
        self.inflation_label.grid(row=4, sticky='w', padx=(1, 1), pady=(1, 1))
        self.inflation_entry = tk.Entry(self, textvariable='', font=self.DEFAULT_FONT)
        self.inflation_entry.insert(0, self.INFLATION_PERCENT)
        self.inflation_entry.grid(row=4, column=1, sticky='ew', padx=(20, 10), pady=(1, 1))

        self.interest_label = tk.Label(self, text=' Interest Earned %:', font=self.DEFAULT_FONT)
        self.interest_label.grid(row=5, sticky='w', padx=(1, 1), pady=(1, 1))
        self.interest_entry = tk.Entry(self, textvariable='', font=self.DEFAULT_FONT)
        self.interest_entry.insert(0, self.INTEREST_EARNED_PERCENT)
        self.interest_entry.grid(row=5, column=1, sticky='ew', padx=(20, 10), pady=(1, 1))

        self.year_start_label = tk.Label(self, text=' Starting Year:', font=self.DEFAULT_FONT)
        self.year_start_label.grid(row=6, sticky='w', padx=(1, 1), pady=(1, 1))
        self.year_start_entry = tk.Entry(self, textvariable="", font=self.DEFAULT_FONT)
        self.year_start_entry.insert(0, self.YEAR_START)
        self.year_start_entry.grid(row=6, column=1, sticky='ew', padx=(20, 10), pady=(1, 1))

        self.year_end_label = tk.Label(self, text=' Ending Year:', font=self.DEFAULT_FONT)
        self.year_end_label.grid(row=7, sticky='w', padx=(1, 1), pady=(1, 1))
        self.year_end_entry = tk.Entry(self, textvariable='', font=self.DEFAULT_FONT)
        self.year_end_entry.insert(0, self.YEAR_END)
        self.year_end_entry.grid(row=7, column=1, sticky='ew',padx=(20, 10),pady=(1, 1))

        self.overview_label = tk.Label(self, text=f'Lifetime Overview:')
        self.overview_label.config(font=self.HEAVY_BOLD_FONT)
        self.overview_label.grid(row=10, sticky='nws', padx=(10, 2), pady=(1, 5), columnspan=2)

        self.yearly_label = tk.Label(self, text='Portfolio Growth:    ')
        self.yearly_label.config(font=self.HEAVY_BOLD_FONT)
        self.yearly_label.grid(row=2, column=2, sticky='news', padx=(5, 5), pady=(2, 2))

    def create_graph_check_box(self):
        '''allows users to choose if they want to create a graph of the data'''
        self.graph_button = tk.IntVar()
        self.graph_check = tk.Checkbutton(self, text='Create Graph', variable=self.graph_button)
        self.graph_check.config(font=self.HEAVY_BOLD_FONT)
        self.graph_check.grid(row=8, column=0, padx=(5, 1), pady=(10, 1), sticky='news')

    def submit(self):
        '''ensures valid entrys and puts limits on what can be entered'''
        def entry_error_check(self):
            '''make sure all the entries are valid numbers.'''

            self.overview.config(state='normal')
            self.specific_year.config(state='normal')

            def fill_in_blanks_with_zero(self, entry):
                if entry.get() == "": entry.insert(0, '0') 
   
            fill_in_blanks_with_zero(self, self.initial_contribution_entry)
            fill_in_blanks_with_zero(self, self.yearly_contribution_entry)
            fill_in_blanks_with_zero(self, self.inflation_entry)
            fill_in_blanks_with_zero(self, self.interest_entry)
            fill_in_blanks_with_zero(self, self.year_start_entry)

            if self.year_end_entry.get() == "": 
                self.year_end_entry.insert(0, int(self.year_start_entry.get())+20) 

            try:
                int(self.initial_contribution_entry.get().replace(',', ''))
                float(self.yearly_contribution_entry.get().replace(',', ''))
                float(self.inflation_entry.get().replace(',','.'))
                float(self.interest_entry.get().replace(',','.'))
                int(self.year_start_entry.get())
                int(self.year_end_entry.get())
            except:
                self.reset()
                self.overview.insert(tk.END, '\n    Invalid Entry\n\n    Resetting to default parameters')
                return True
            
            '''#cannot start in the past'''
            if int(self.year_start_entry.get()) < 0:
                self.reset()
                self.overview.insert(tk.END, f'\n   Starting year must be ≥ 0')
                return True

            '''# check if end year is before  start year'''
            if int(self.year_end_entry.get()) < int(self.year_start_entry.get()):
                
                self.reset()
                self.overview.insert(tk.END, '\n    Start Year > End year\n\n ')
                return True
            
            '''#check if years are too far apart'''
            if int(self.year_end_entry.get()) - int(self.year_start_entry.get()) > 1000:
                self.reset()
                self.overview.insert(tk.END, '\n    Year range must be ≤ 1000')
                return True

            if int(self.year_end_entry.get()) == int(self.year_start_entry.get()):
                self.reset()
                self.overview.insert(tk.END, '\n    End year ≠ Start year')
                return True
            
            '''#check if inflation and interest are within 0 and 100'''
            if not 0 <= float(self.inflation_entry.get().replace(',','.')) <= 100:
                self.reset()
                self.overview.insert(tk.END, '\n    Inflation Percent Error\n\n    Please use a number within 0 ≤ X ≤ 100')
                return True
            
            if not 0 <= float(self.interest_entry.get().replace(',','.')) <= 100:
                self.reset()
                self.overview.insert(tk.END, '\n    Interest Percent Error\n\n    Please use a number within 0 ≤ X ≤ 100')
                return True
            
            '''make sure starting balance and yearly contribution are ≥ 0'''
            
            if int(self.initial_contribution_entry.get().replace(',', '')) < 0:                    
                self.reset()
                self.overview.insert(tk.END, '\n    Initial Investment Error\n\n    Please use a number ≥ 0')
                return True
            
            if int(self.yearly_contribution_entry.get().replace(',', '')) < 0:                   
                self.reset()
                self.overview.insert(tk.END, '\n    Yearly Contribution Error\n\n    Please use a number ≥ 0')
                return True
                       
        if entry_error_check(self):
            self.overview.config(state='disabled')
            self.specific_year.config(state='disabled')
            return

        '''error checking section end'''

        def clear_variables_close_plot(self):
            """Clears the variables."""
            self.investment_growth.clear()
            self.overview.delete('1.0', tk.END)
            self.specific_year.delete('1.0', tk.END)
            plt.close()
            # if plt.get_fignums():
            #     plt.close()

        def get_variables_from_storage(self):
            """Grabs the variables from storage."""

            self.starting_balance = int(self.initial_contribution_entry.get().replace(',', ''))
            self.yearly_contribution = int(self.yearly_contribution_entry.get().replace(',', ''))
            self.inflation = float(self.inflation_entry.get().replace(',', '.')) * .01 + 1
            self.interest = float(self.interest_entry.get().replace(',', '.')) * .01 + 1
            self.year_start = int(self.year_start_entry.get())
            self.year_end = int(self.year_end_entry.get())

            self.total_years = self.year_end - self.year_start
            # year calculation using date.time()

            self.current_year = datetime.now().year

            self.years_inflation = self.year_end-self.year_start
            self.total_inflation = self.inflation**self.years_inflation

        def calculate_balances(self):

            self.investment_growth.append(self.starting_balance)

            for year in range(0, self.total_years+1):

                if year == 0:
                    self.investment_growth[0] = self.investment_growth[0]*self.interest
                else:
                    self.investment_growth.append((self.investment_growth[year-1]+self.yearly_contribution)*self.interest)


            """Calculates the balances for each year."""
        
        def insert_overview_text(self):
            """Inserts data into overview text."""

            self.overview.insert(tk.END, f'  Final Value: {round(self.investment_growth[-1]):,} in [{self.year_end}] \n', 'highlight')

            '''avoid typing- 0% Inflation from 2024 to 2039 @ 0.0%'''
            # if float(self.inflation_entry.get()) != 0:
            self.overview.insert(tk.END, f'\n     {round((self.investment_growth[-1])/self.total_inflation):,} in [{self.year_start}]\n')

            self.overview.insert(tk.END, f'\n     {round((self.total_inflation-1)*100)}% Inflation from [{self.year_start}] to [{self.year_end}]\n')

            self.overview.insert(tk.END, f'\n  Total Invested: {self.starting_balance+(self.yearly_contribution*self.total_years):,} @ {round((self.interest-1)*100,2)}% interest \n')

        def insert_specific_year_text(self):
            """Inserts the specific year text."""

            highlight = False

            for year, item in zip([year for year in range(self.year_start, self.year_end+1)],self.investment_growth):
                tag = 'default' if highlight else 'highlight'
                highlight = not highlight
                self.specific_year.insert(tk.END, f'   {year}: {round(item):,}\n', tag)

        def create_graph(self):
            '''creates a graph of the data'''
            year_start = int(self.year_start_entry.get())
            year_end = int(self.year_end_entry.get())+1
            inflation_adjusted = [self.investment_growth[year]/self.inflation**year for year in range(year_end-year_start)]
            portfolio_max_value = max(self.investment_growth) 
            portfolio_max_value_inflation_adjusted = max(inflation_adjusted)  

            px = 1/plt.rcParams['figure.dpi']
            '''ensure graph and app have same height. had to do this manually, as there was no way to get the height of matplotlib tool bar'''
            fig, ax = plt.subplots(figsize=(GRAPH_WIDTH*px, GRAPH_HEIGHT*px))
            ax.tick_params(labelcolor = COLORS['TEXT_COLOR'], labelsize=FONTS['DEFAULT_FONT'][1])
            plt.rcParams['text.color'] = COLORS['TEXT_COLOR']

            plt.suptitle(f'Investment Growth', fontsize=FONTS['TITLE_FONT'][1], fontweight='bold')

            def align_graph_with_app(self):
        
                geometry = self.winfo_toplevel().wm_geometry()
                _, calc_coord_x, calc_coord_y = geometry.split('+')
                calc_width, calc_height, = self.winfo_width(), self.winfo_height()

                '''if the width of the calculator app + width of graph exceeds right side of screen,
                put graph to the left side'''

                if calc_width + GRAPH_WIDTH + int(calc_coord_x) > SCREEN_HORIZONTAL_RES:
                    graph_position = f'+{str(int(calc_coord_x)-GRAPH_WIDTH-10)}+{calc_coord_y}' 
                else: 
                    graph_position = f'+{str(calc_width+int(calc_coord_x)+3)}+{str(int(calc_coord_y))}'
            
                '''set graph position to line up with calculator app'''
                mngr = plt.get_current_fig_manager()
                mngr.window.geometry(graph_position)
            
            align_graph_with_app(self)

            '''set color and text size of labels'''
            ax.tick_params(labelcolor= COLORS['TEXT_COLOR'], labelsize=FONTS['DEFAULT_FONT'][1])
        
            '''plot max value markers, matplot lib follows FILO. portfolio max will be on top of inflation in case of overlap'''
            '''if inflation is 0, no need to plot inflation graph'''
            if float(self.inflation_entry.get()) != 0:
                ax.plot([year for year in range(year_start, year_end)], inflation_adjusted, linestyle=(1,(5,1)), c=self.INFLATION_GRAPH_COLOR)
                '''marker for end value of inflation adjusted graph'''
                plt.plot(self.year_end, portfolio_max_value_inflation_adjusted, c=self.INFLATION_GRAPH_COLOR, marker='.', markersize=FONTS['DEFAULT_FONT'][1])

            '''investment growth graph'''
            ax.plot([year for year in range(year_start, year_end)], self.investment_growth, c=self.POSITIVE_BAL_COLOR)
            '''marker for end value of investment growth graph'''
            plt.plot(self.year_end, portfolio_max_value, c=self.POSITIVE_BAL_COLOR, marker='.', markersize=12)

            # only show ever other year for readability
            '''skip labels if the x axis becomes too crowded'''

            def skip_x_labels(self):
                ax.set_xticks([year for year in range(year_start, year_end)], minor=False)
                ax.tick_params(axis='x', rotation=45)
                ax.xaxis.grid(True, which='minor')

                x_label_total = len(ax.xaxis.get_ticklabels())
                if x_label_total <= 31:
                    for label in ax.xaxis.get_ticklabels()[1::2]:
                        label.set_visible(False)

                elif x_label_total <= 66:
                    indexes_to_keep = [kept_index for kept_index in ax.xaxis.get_ticklabels()[0::3]]
                    grid_lines = ax.get_xgridlines()
                    for index, label in enumerate(ax.xaxis.get_ticklabels()):
                        if label in indexes_to_keep:
                            continue
                        else:
                            label.set_visible(False)
                            '''set color to white or linewidth to 0 achieves same purpose'''
                            # grid_lines[index].set_color('white')
                            grid_lines[index].set_linewidth(0)

                elif x_label_total <= 101:
                    indexes_to_keep = [kept_index for kept_index in ax.xaxis.get_ticklabels()[0::5]]
                    grid_lines = ax.get_xgridlines()
                    for index, label in enumerate(ax.xaxis.get_ticklabels()):
                        if label in indexes_to_keep:
                            continue
                        else:
                            label.set_visible(False)
                            '''set color to white or linewidth to 0 achieves same purpose'''
                            # grid_lines[index].set_color('white')
                            grid_lines[index].set_linewidth(0)

                elif x_label_total <= 151:
                    indexes_to_keep = [kept_index for kept_index in ax.xaxis.get_ticklabels()[0::7]]
                    grid_lines = ax.get_xgridlines()
                    for index, label in enumerate(ax.xaxis.get_ticklabels()):
                        if label in indexes_to_keep:
                            continue
                        else:
                            label.set_visible(False)
                            '''set color to white or linewidth to 0 achieves same purpose'''
                            # grid_lines[index].set_color('white')
                            grid_lines[index].set_linewidth(0)

                else:
                    indexes_to_keep = [kept_index for kept_index in ax.xaxis.get_ticklabels()[0::10]]
                    grid_lines = ax.get_xgridlines()
                    for index, label in enumerate(ax.xaxis.get_ticklabels()):
                        if label in indexes_to_keep:
                            continue
                        else:
                            label.set_visible(False)
                            '''set color to white or linewidth to 0 achieves same purpose'''
                            # grid_lines[index].set_color('white')
                            grid_lines[index].set_linewidth(0)

            skip_x_labels(self)

            def format_y_axis(self):
                '''set y axis to start at 0, then end at 1.1*max value of portfolio'''
                ax.set_ylim(ymin=0)
                ax.set_ylim(ymax=max(self.investment_growth)*1.1)

                if portfolio_max_value < 1000000:
                    yticks = ax.get_yticks().tolist()
                    ax.set_yticks(yticks)
                    ax.set_yticklabels(['{:,}'.format(int(x)) for x in yticks], fontsize=FONTS['DEFAULT_FONT'][1])

                elif portfolio_max_value < 1000000000:
                    def formatter(x, pos):
                        return str(round(x / 1e6, 1)) 
                    
                    ax.yaxis.set_major_formatter(formatter)
                    '''top left label'''

                    ax.text(0, 1.05, "E6", transform = ax.transAxes, ha = "left", va = "top", fontsize=FONTS['HEAVY_BOLD_FONT'][1],fontweight='bold')
                    '''y axis label'''

                    ax.set_ylabel('Millions', fontsize=FONTS['HEAVY_BOLD_FONT'][1], fontweight='bold')

                elif portfolio_max_value < 1000000000000:
                    def formatter(x, pos):
                        return str(round(x / 1e9, 1)) 
                    
                    ax.yaxis.set_major_formatter(formatter)

                    ax.text(0, 1.05, "E9", transform = ax.transAxes, ha = "left", va = "top", fontsize=FONTS['HEAVY_BOLD_FONT'][1],fontweight='bold')

                    ax.set_ylabel('Billions', fontsize=FONTS['HEAVY_BOLD_FONT'][1], fontweight='bold')

                elif portfolio_max_value < 1000000000000000:
                    def formatter(x, pos):
                        return str(round(x / 1e12, 1)) 
                    
                    ax.yaxis.set_major_formatter(formatter)

                    ax.text(0, 1.05, "E12", transform = ax.transAxes, ha = "left", va = "top", fontsize=FONTS['HEAVY_BOLD_FONT'][1],fontweight='bold')   

                    ax.set_ylabel('Trillions', fontsize=FONTS['HEAVY_BOLD_FONT'][1], fontweight='bold')

            format_y_axis(self)

            #text box for information
            props = dict(boxstyle='round', facecolor='white', alpha=1, edgecolor='black')

            textstr = f'Initial: {self.starting_balance:,}\nYearly: {self.yearly_contribution:,}\nInflation: {self.inflation_entry.get()}%\nInterest: {self.interest_entry.get()}%\nWindow: {year_end-year_start} Yrs'

            ax.text(.02, .975, textstr, transform=ax.transAxes, fontsize=FONTS['DEFAULT_FONT'][1], verticalalignment='top', horizontalalignment='left', bbox=props)

            '''max value annotation'''
            ax.annotate(f'{round(portfolio_max_value):,} in {self.year_end}', (self.year_end, portfolio_max_value), textcoords="offset points", xytext=(-20,15), ha='center', fontsize=FONTS['DEFAULT_FONT'][1], bbox=props)

            '''inflation adjusted max value annotation. move down if too close to portfolio max value'''

            if float(self.inflation_entry.get()) != 0:

                if portfolio_max_value < portfolio_max_value_inflation_adjusted*1.1:       

                    ax.annotate(f'Inflation Adj: {round(inflation_adjusted[-1]):,}', (self.year_end, portfolio_max_value_inflation_adjusted), textcoords="offset points", xytext=(-20,-20), ha='center', fontsize=FONTS['DEFAULT_FONT'][1], bbox=props)

                else:
                    ax.annotate(f'Inflation Adj: {round(inflation_adjusted[-1]):,}', (self.year_end, portfolio_max_value_inflation_adjusted), textcoords="offset points", xytext=(-20, 15), ha='center', fontsize=FONTS['DEFAULT_FONT'][1], bbox=props)

            ax.grid(True)
            ax.format_coord = lambda x,y: f"$ {int(round(y,-3)):,}\n{round(x)}"

            '''format y axis labels with commas if portfolio max under one million, prevent scientific notation'''

            # plt.tight_layout()
            ax.set_axisbelow(True) 
            plt.tight_layout()
            plt.show()

        clear_variables_close_plot(self)
        get_variables_from_storage(self)
        calculate_balances(self)

        self.overview_label.config(text=f'Lifetime Overview: {self.year_end-self.year_start+1} years')  

        if self.year_end-self.year_start > 100:
            self.controller.title(f'Investment Calculator for {random.choice(random_list)}')
        else:
            self.controller.title(f'Investment Calculator')

        self.overview.config(state='normal')
        self.specific_year.config(state='normal')
        insert_overview_text(self)
        insert_specific_year_text(self)
        self.overview.config(state='disabled')
        self.specific_year.config(state='disabled')
        
        plt.close()
        if self.graph_button.get():
            create_graph(self)

        '''copy the values to retirement calculator. ending year of investment is starting year of retirement. final balance of investment is initial balance of retirement'''
        self.controller.frames["retirement"].starting_balance_entry.delete(0, tk.END)
        self.controller.frames["retirement"].starting_balance_entry.insert(0, round(self.investment_growth[-1]))

        self.controller.frames["retirement"].year_start_entry.delete(0, tk.END)
        self.controller.frames["retirement"].year_start_entry.insert(0, self.year_end_entry.get())

        self.controller.frames["retirement"].year_end_entry.delete(0, tk.END)
        self.controller.frames["retirement"].year_end_entry.insert(0, int(self.year_end_entry.get())+30)

        self.controller.frames["retirement"].overview.config(state='normal')
        self.controller.frames["retirement"].overview.delete('1.0', tk.END)
        self.controller.frames["retirement"].overview.insert(tk.END, f'  Initial balance & Starting Year Copied')
        self.controller.frames["retirement"].overview.config(state='disabled')

    def create_submit_button(self):
        # button that calls the submit 
        sub_btn = tk.Button(self, text=' Submit ', command=self.submit)
        sub_btn.config(font=self.HEAVY_BOLD_FONT)
        sub_btn.grid(row=8, column=1, padx=(10,1), pady=(10,1), sticky='w')

        sub_btn.bind("<Enter>", self.controller.on_hover)
        sub_btn.bind("<Leave>", self.controller.on_leave)

    def reset(self):
        '''resets all entries to the default values'''
        self.overview.config(state='normal')
        self.specific_year.config(state='normal')

        self.initial_contribution_entry.delete(0, tk.END)
        self.yearly_contribution_entry.delete(0, tk.END)
        self.inflation_entry.delete(0, tk.END)
        self.interest_entry.delete(0, tk.END)
        self.year_start_entry.delete(0, tk.END)
        self.year_end_entry.delete(0, tk.END)

        self.initial_contribution_entry.insert(0, "{:,}".format(self.INITIAL_CONTRIBUTION))
        self.yearly_contribution_entry.insert(0,"{:,}".format(self.YEARLY_CONTRIBUTION))
        self.inflation_entry.insert(0, self.INFLATION_PERCENT)
        self.interest_entry.insert(0, self.INTEREST_EARNED_PERCENT)
        self.year_start_entry.insert(0, self.YEAR_START)
        self.year_end_entry.insert(0, self.YEAR_END)
        self.overview.delete('1.0', tk.END)
        self.specific_year.delete('1.0', tk.END)
        
        # self.master.title(f'Investment Calculator')
        self.overview_label.config(text=f'Lifetime Overview:') 

        if plt.get_fignums():
                plt.close()

        self.controller.frames["retirement"].starting_balance_entry.delete(0, tk.END)
        self.controller.frames["retirement"].starting_balance_entry.insert(0, DEFAULT_PARAMS['STARTING_BALANCE'])

    def create_reset_button(self):
        
        reset_btn = tk.Button(self, text=' Reset ', command=self.reset)
        reset_btn.config(font=self.HEAVY_BOLD_FONT)
        reset_btn.grid(row=8, column=1, padx=(1, 10), pady=(10, 1), sticky='e')

        reset_btn.bind("<Enter>", self.controller.on_hover)
        reset_btn.bind("<Leave>", self.controller.on_leave)

    def create_overview_box(self):
        '''gives the overview of what the calculation shows total years, initial and final withdrawal, remaining balance, total lifetime withdrawal, and if the account goes negative, the year it goes negative and how many years short it is. see submit method'''

        self.overview = tk.Text(self, height=self.OVERVIEW_HEIGHT, width=self.OVERVIEW_WIDTH)
        self.overview.config(font=self.DEFAULT_FONT, selectbackground='gray95', selectforeground="blue")
        self.overview.grid(row=11, column=0, columnspan=2, rowspan=5, padx=(10, 10), pady=(2, 10), sticky='news')

        self.overview.tag_config('neg_bal_color', foreground=self.NEGATIVE_BAL_COLOR)
        self.overview.tag_config('highlight', background=self.ALT_HIGHLIGHT)
        self.overview.tag_config('BOLD', font='bold')

        self.overview.config(state='disabled')

    def create_specific_year_box(self):
        '''textbox to show the portfolio growth data data'''

        # shows the withdrawal pertaining to the specific year
        self.specific_year = tk.Text(self, height=self.SPECIFIC_YEAR_HEIGHT, width=self.SPECIFIC_YEAR_WIDTH)
        self.specific_year.config(font=self.DEFAULT_FONT, selectbackground='gray95', selectforeground="blue")
        self.specific_year.grid(row=3, column=2, rowspan=13, padx=(5, 0), pady=(0, 10), sticky='news')

        # this tag is used to highlight years where the balance goes negative
        self.specific_year.tag_config('neg_bal_color', foreground=self.NEGATIVE_BAL_COLOR)
        # this tag is used to highlight every other year for readability
        self.specific_year.tag_config('highlight', background=self.ALT_HIGHLIGHT)
        self.specific_year.tag_config('default', background='white')

        self.specific_year_Scrollbar = tk.Scrollbar(self, command=self.specific_year.yview)
        self.specific_year.configure(yscrollcommand=self.specific_year_Scrollbar.set)
        self.specific_year_Scrollbar.grid(row=3, column=3, rowspan=13, columnspan=1, sticky='news', padx=(0, 5), pady=(0, 10))

        self.specific_year.config(state='disabled')
        
