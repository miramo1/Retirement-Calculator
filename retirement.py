import tkinter as tk
import random
from matplotlib import pyplot as plt
from datetime import datetime

from global_variables import FONTS, DEFAULT_PARAMS, COLORS, GRAPH_WIDTH, GRAPH_HEIGHT, SCREEN_HORIZONTAL_RES, random_list

class retirement(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        self.controller = controller
        
        self.TITLE_FONT = FONTS['TITLE_FONT']
        self.HEAVY_BOLD_FONT = FONTS['HEAVY_BOLD_FONT']
        self.DEFAULT_FONT = FONTS['DEFAULT_FONT']

        self.STARTING_BALANCE = DEFAULT_PARAMS['STARTING_BALANCE']
        self.WITHDRAWAL_PERCENT = DEFAULT_PARAMS['WITHDRAWAL_PERCENT']
        self.INFLATION_PERCENT = DEFAULT_PARAMS['INFLATION_PERCENT']

        '''2% is the federal reserve target inflation rate, 3.77% is the average inflation rate since 1971, 2.5% is the average inflation rate since 2000'''
        self.INTEREST_EARNED_PERCENT = DEFAULT_PARAMS['INTEREST_EARNED']

        '''10% is the average return of S&P 500 Index for the last 100 years. 8% is a conservative estimate'''
        self.YEAR_START = datetime.now().year+14
        self.YEAR_END = self.YEAR_START+30

        self.SPECIFIC_YEAR_HEIGHT = 28
        self.SPECIFIC_YEAR_WIDTH = 20
        self.OVERVIEW_HEIGHT = 17
        self.OVERVIEW_WIDTH = 20

        self.NEGATIVE_BAL_COLOR = COLORS['NEGATIVE_BAL_COLOR']
        self.POSITIVE_BAL_COLOR = COLORS['POSITIVE_BAL_COLOR']
        self.ALT_HIGHLIGHT = COLORS['ALT_HIGHLIGHT']

        self.years = []
        self.remaining_balance = []
        self.withdrawals = []

        '''used two frames to draw horizontal lines to partition areas of the GUI'''

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
        self.master.show_frame('investment')

    def create_title(self):

        # page_name = tk.Label(self, text="Retirement Calculator", font=self.controller.FONTS["TITLE_FONT"])
        page_name = tk.Label(self, text="Retirement Calculator", font=self.TITLE_FONT)
        page_name.grid(row=0, column=0, columnspan=2, sticky="news",padx=(10, 10), pady=(5, 2))

        '''switch button to swap apps, also closes plot if open'''
        switch_button = tk.Button(self, text="Investment", font=self.HEAVY_BOLD_FONT, command=lambda: [self.controller.show_frame('investment'), plt.close(), self.controller.title('Investment Calculator')])
        switch_button.grid(row=0, column=2, columnspan=1, sticky="ns", padx=(0,0), pady=(5, 2))
        
        switch_button.bind("<Enter>", self.controller.on_hover)
        switch_button.bind("<Leave>", self.controller.on_leave)

    def create_labels_and_entries(self):
        '''used a trace to format the starting balance entry with commas. also used a try except to make sure the entry is a valid integer. if not, it ignores the error and does nothing. this is to prevent the user from entering a non integer value. the same is done for the other entries. see submit method for error checking.'''
        def add_commas_to_initial_balance(*args):
            value = starting_balance_var.get().replace(',', '')  # remove existing commas
            if value:
                try:
                    number = int(value)  # convert to integer
                    formatted = "{:,}".format(number)  # format with commas
                    starting_balance_var.set(formatted)  # update the StringVar
                except ValueError:
                    pass  # not a valid integer, ignore
                  
        starting_balance_var = tk.StringVar()
        starting_balance_var.trace('w', add_commas_to_initial_balance)

        self.starting_balance_label = tk.Label(self, text=' Initial Balance:', font=self.DEFAULT_FONT)
        self.starting_balance_label.grid(row=2, sticky='w', padx=(1, 1), pady=(1, 1))
        self.starting_balance_entry = tk.Entry(self, textvariable=starting_balance_var, font=self.DEFAULT_FONT)            
        self.starting_balance_entry.insert(0, "{:,}".format(self.STARTING_BALANCE))            
        self.starting_balance_entry.grid(row=2, column=1, sticky='ew', padx=(20, 10), pady=(1, 1))

        self.starting_withdrawal_label = tk.Label(self, text=' Withdrawal %:', font=self.DEFAULT_FONT)
        self.starting_withdrawal_label.grid(row=3, sticky='w', padx=(1, 1), pady=(1, 1))
        self.starting_withdrawal_entry = tk.Entry(self, textvariable='', font=self.DEFAULT_FONT)
        self.starting_withdrawal_entry.insert(0, self.WITHDRAWAL_PERCENT)
        self.starting_withdrawal_entry.grid(row=3, column=1, sticky='ew', padx=(20, 10), pady=(1, 1))

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

        self.yearly_label = tk.Label(self, text='Yearly Withdrawals:')
        self.yearly_label.config(font=self.HEAVY_BOLD_FONT)
        self.yearly_label.grid(row=2, column=2, sticky='news', padx=(5, 5), pady=(2, 2))

    def create_graph_check_box(self):
        '''option create a graph of the data with matplotlib.'''
        self.graph_button = tk.IntVar()
        self.graph_check = tk.Checkbutton(self, text='Create Graph', variable=self.graph_button)
        self.graph_check.config(font=self.HEAVY_BOLD_FONT)
        self.graph_check.grid(row=8, column=0, padx=(5, 1), pady=(10, 1), sticky='news')

    def entry_error_checker(self):

        def fill_in_blanks_with_zero(self, entry):
            if entry.get().replace(" ", "") == "": entry.insert(0, '0') 

        fill_in_blanks_with_zero(self, self.starting_balance_entry)
        fill_in_blanks_with_zero(self, self.starting_withdrawal_entry)
        fill_in_blanks_with_zero(self, self.inflation_entry)
        fill_in_blanks_with_zero(self, self.interest_entry)

        '''open text boxes to allow error messages to be printed.'''
        self.overview.config(state='normal')
        self.specific_year.config(state='normal')

        '''make sure all entries are numbers, including decimals'''
        try:
            int(self.starting_balance_entry.get().replace(',', ''))
            float(self.starting_withdrawal_entry.get().replace(',', '.'))
            float(self.inflation_entry.get().replace(',','.'))
            float(self.interest_entry.get().replace(',','.'))
            int(self.year_start_entry.get())
            int(self.year_end_entry.get())
        except:
            self.reset()
            self.overview.insert(tk.END, '\n    Invalid Entry\n\n    Resetting to default parameters')
            return True

        '''check if starting year is negative'''
        if int(self.year_start_entry.get()) < datetime.now().year:
            self.reset()
            self.overview.insert(tk.END, f'\n   Starting year must be ≥ {datetime.now().year}')
            return True
                
        '''check if ending year is before starting year'''  
        if int(self.year_end_entry.get()) < int(self.year_start_entry.get()):
            self.reset()
            self.overview.insert(tk.END, '\n    Start Year > End year')
            return True

        '''check if years are too far apart. prevents integer overflow.'''
        if int(self.year_end_entry.get()) - int(self.year_start_entry.get()) > 200:
            self.reset()
            self.overview.insert(tk.END, '\n   Year range must be ≤ 200')
            return True
        
        '''end year must be different from start year'''
        if int(self.year_end_entry.get()) == int(self.year_start_entry.get()):
            self.reset()
            self.overview.insert(tk.END, '\n    End year ≠ Start year')
            return True
        
        '''#withdrawal, inflation and interest percents must be within 0<x<100. prevents integer overflow'''

        if float(self.starting_withdrawal_entry.get().replace(',', '.')) > 100 or float(self.starting_withdrawal_entry.get().replace(',', '.')) < 0: 
            self.reset()
            self.overview.insert(tk.END, '\n    Withdrawal Percent Error\n\n    Please use a number within 0 ≤ X ≤ 100')
            return True
        
        if float(self.inflation_entry.get().replace(',','.')) > 100 or float(self.inflation_entry.get().replace(',','.')) < 0:
            self.reset()
            self.overview.insert(tk.END, '\n    Inflation Percent Error\n\n    Please use a number within 0 ≤ X ≤ 100')
            return True
        
        if float(self.interest_entry.get().replace(',','.')) > 100 or float(self.interest_entry.get().replace(',','.')) < 0:
            self.reset()
            self.overview.insert(tk.END, '\n    Interest Percent Error\n\n    Please use a number within 0 ≤ X ≤ 100')
            return True

        #check if starting balance is negative
        if int(self.starting_balance_entry.get().replace(',', '')) <= 0:
            self.reset()
            self.overview.insert(tk.END, '\n    Starting Balance Error\n\n    Please use a positive number')
            return True
            
    def submit(self):

        # if there is an error, break out of the submit button    
        if self.entry_error_checker():
            '''close check boxes to prevent user from entering data while error message is displayed.'''
            self.overview.config(state='disabled')
            self.specific_year.config(state='disabled')
            return
        
        '''start of submit button functions.'''

        def clear_variables_close_plot(self):
            """Clears the variables."""
            self.years.clear()
            self.remaining_balance.clear()
            self.withdrawals.clear()
            self.overview.delete('1.0', tk.END)
            self.specific_year.delete('1.0', tk.END)

            # if plt.get_fignums():
            #     plt.close()

        def get_variables_from_storage(self):
            """Grabs the variables from storage. This part is what allows user entered data to be used in the calculations."""

            self.balance = float(self.starting_balance_entry.get().replace(',', ''))
            self.starting_withdrawal = float(self.starting_withdrawal_entry.get().replace(',', '.')) * .01 * self.balance
            self.inflation = float(self.inflation_entry.get().replace(',', '.')) * .01 + 1
            self.interest = float(self.interest_entry.get().replace(',', '.')) * .01 + 1
            self.year_start = int(self.year_start_entry.get())
            self.year_end = int(self.year_end_entry.get())+1

            self.years_inflation = self.year_start-datetime.now().year
            self.total_inflation = self.inflation**self.years_inflation

        def calculate_balances(self):
            """Calculates the balances for each year."""

            self.negative = False
            self.date_of_first_negative = 0

            for i in range(self.year_start, self.year_end):
                self.years.append(i)
                self.withdrawals.append(round(self.starting_withdrawal))

                '''if the balance goes negative, we want to record it. negative balances are later highlighted in red'''
                if self.balance - self.starting_withdrawal <= 0:
                    if not self.negative:
                        self.date_of_first_negative = i
                        self.negative = True
                    self.balance -= self.starting_withdrawal
                    self.starting_withdrawal *= self.inflation
                    self.remaining_balance.append(round(self.balance))
                else:
                    self.balance -= self.starting_withdrawal
                    self.starting_withdrawal *= self.inflation
                    self.balance *= self.interest
                    self.remaining_balance.append(round(self.balance))

        def insert_overview_text(self):
            """Inserts data into overview text."""

            # '''eg. 6% of 500,000 at 2.5% inflation'''
            # self.overview.insert(tk.END, f'  {self.starting_withdrawal_entry.get()}% of {
            #                     self.starting_balance_entry.get()} at {self.inflation_entry.get()}% inflation\n\n')
            
            '''eg. Initial Withdrawal: 30,000 in 2039'''
            self.overview.insert(tk.END, f'  Initial Withdrawal: {
                                self.withdrawals[0]:,} in [{self.year_start}]\n', 'highlight')
            
            '''eg. 20,714 @ 1,726 monthly in 2024'''

            self.overview.insert(tk.END, f'\n     Equal to {round(self.withdrawals[0]/self.total_inflation):,} in [{datetime.now().year}]\n')

            self.overview.insert(tk.END, f'\n          {round(self.withdrawals[0]/self.total_inflation/12):,} Monthly\n\n')


            '''eg. Total Lifetime Withdrawals: 1,380,009'''
            self.overview.insert(tk.END, f'  Total Lifetime Withdrawals:', 'highlight')
            self.overview.insert(tk.END, f' {sum(self.withdrawals):,}\n', 'highlight')
            '''eg. Last withdrawal: 62,927'''
            self.overview.insert(tk.END, f'\n    Last withdrawal: {self.withdrawals[-1]:,}\n\n')

            '''if balance goes negative, highlights it with the neg_bal_color tag'''
            if self.negative:
                '''show final balance in red'''
                self.overview.insert(tk.END, f' Final Balance:', 'highlight')
                self.overview.insert(tk.END, f' {self.remaining_balance[-1]:,}', 'neg_bal_and_highlight')
                self.overview.insert(tk.END, f' in [{self.year_end-1}]\n', 'highlight')

                '''show inflation adjusted final balance in red'''
                if self.year_start < datetime.now().year:
                    pass
                else:
                    self.overview.insert(tk.END, f'\n    {round(self.remaining_balance[-1]/self.inflation**(self.year_end-datetime.now().year)):,}', 'neg_bal_color')
                    self.overview.insert(tk.END, f' in [{datetime.now().year}] dollars\n')

                '''prints out years short plural vs singular'''
                self.overview.insert(tk.END, f'\n    Negative in {self.date_of_first_negative}, ')
                if self.year_end-self.date_of_first_negative == 1:
                    self.overview.insert(tk.END, f'{self.year_end-self.date_of_first_negative} Year Short')
                else:
                    self.overview.insert(tk.END, f'{self.year_end-self.date_of_first_negative} Years Short')

                numer = self.date_of_first_negative-self.year_start
                denom = self.year_end-self.year_start

                self.overview.insert(tk.END, f'\n\n    Positive Balance for {round((numer/denom)*100)}% of retirement')

            else:
                
                self.overview.insert(tk.END, f'  Final Balance:', 'highlight')
                self.overview.insert(tk.END, f' {self.remaining_balance[-1]:,}', 'positive_bal_and_highlight')
                self.overview.insert(tk.END, f' in [{self.year_end-1}]\n', 'highlight')

                self.overview.insert(tk.END, f'\n    {round(self.remaining_balance[-1]/self.inflation**(self.year_end-datetime.now().year)):,}', 'positive_bal_color')
                self.overview.insert(tk.END, f' in [{datetime.now().year}] dollars')

        def insert_specific_year_text(self):
            """Inserts the specific year text. Highlight tag is flipped every iteration for better visibility"""

            highlight = False
            for withdrawal, year in zip(self.withdrawals, self.years):
                tag = 'default' if highlight else 'highlight'
                highlight = not highlight
                if self.negative and year >= self.date_of_first_negative:
                    self.specific_year.insert(tk.END, f'   {year}: {withdrawal:,}\n', ('neg_bal_color', tag))
                else:
                    self.specific_year.insert(tk.END, f'   {year}: {withdrawal:,}\n', ('highlight', tag))

        def create_graph(self):
            portfolio_max_value = max(self.remaining_balance)
            portfolio_max_year = self.years[self.remaining_balance.index(portfolio_max_value)]
            
            '''ensure graph and app have same height. had to do this manually, as there was no way to get the height of matplotlib tool bar'''
            px = 1/plt.rcParams['figure.dpi']
            fig, ax = plt.subplots(figsize=(GRAPH_WIDTH*px, GRAPH_HEIGHT*px))
            
            '''creates a graph of the data'''
            ax.plot(self.years, self.remaining_balance, c=self.POSITIVE_BAL_COLOR, label='Remaining Balance', lw=2)

            '''set color and font of labels and text'''
            ax.tick_params(labelcolor = COLORS['TEXT_COLOR'], labelsize=FONTS['DEFAULT_FONT'][1])
            plt.rcParams['text.color'] = COLORS['TEXT_COLOR']

            '''Title, and super title'''
            plt.suptitle(f'Retirement Account Balance', fontsize=self.TITLE_FONT[1], fontweight='bold')

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

            '''only show every other year on x axis for readability'''
            def format_x_axis(self):

                ax.set_xticks([year for year in range(self.year_start, self.year_end)], minor=False)
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

            format_x_axis(self)    

            '''format y axis labels with commas if portfolio max under one million, prevents scientific notation'''

            def format_y_axis(self):
                
                '''if graph has negative values, extend y axis by extra 5 percent of both min/max balance'''
                if self.remaining_balance[-1] < 0:
                    ax.set_ylim(ymin=min(self.remaining_balance)*1.05)
                    ax.set_ylim(ymax=max(self.remaining_balance)*1.15)
                    '''y axis extened by extra 10 percent of negative min balance'''
                else:
                    ax.set_ylim(ymax=max(self.remaining_balance)*1.075)
                    ax.set_ylim(ymin=min(self.remaining_balance)*.925)  

                if abs(max(self.remaining_balance, key=abs)) < 1000000:
                    yticks = ax.get_yticks().tolist()
                    ax.set_yticks(yticks)
                    ax.set_yticklabels(['{:,}'.format(int(x)) for x in yticks], fontsize=FONTS['DEFAULT_FONT'][1])
                elif abs(max(self.remaining_balance, key=abs)) < 1000000000:
                    def formatter(x, pos):
                        return str(round(x / 1e6, 1)) 
                    ax.yaxis.set_major_formatter(formatter)

                    ax.text(0, 1.05, "E6", transform = ax.transAxes, ha = "left", va = "top", fontsize=FONTS['HEAVY_BOLD_FONT'][1],fontweight='bold')

                    '''y axis label'''
                    ax.set_ylabel('Millions', fontsize=FONTS['HEAVY_BOLD_FONT'][1], fontweight='bold')

                else:
                    def formatter(x, pos):
                        return str(round(x / 1e9, 1)) 
                    ax.yaxis.set_major_formatter(formatter)

                    ax.text(0, 1.05, "E9", transform = ax.transAxes, ha = "left", va = "top", fontsize=FONTS['HEAVY_BOLD_FONT'][1],fontweight='bold')
                    '''y axis label'''

                    ax.set_ylabel('Billions', fontsize=FONTS['HEAVY_BOLD_FONT'][1],fontweight='bold')

            format_y_axis(self)

            '''marker for starting balance'''
            plt.plot(self.year_start, self.remaining_balance[0], c=self.POSITIVE_BAL_COLOR, marker='.', markersize=FONTS['DEFAULT_FONT'][1])

            '''text box for information- withdrawal, inflation, interest, max value, final value'''
            props = dict(boxstyle='round', facecolor='white', alpha=1, edgecolor='black')

            '''marker and textbox for highest balance'''
            plt.plot(portfolio_max_year, portfolio_max_value, c=self.POSITIVE_BAL_COLOR, marker='.', markersize=FONTS['DEFAULT_FONT'][1])
            
            '''offset y coordinate for portfolio max, and final balance labels.'''
            max_label_vertical_offset = self.winfo_height()/50
            final_label_vertical_offset = -self.winfo_height()/30

            '''portfolio max value and year annotation. always shown.'''
            ax.annotate(f'Max: {portfolio_max_value:,}', (portfolio_max_year, portfolio_max_value), textcoords="offset points", xytext=(-20,max_label_vertical_offset), ha='center', fontsize=FONTS['DEFAULT_FONT'][1], bbox=props) 

            '''final balance marker. always shown. if negative, red marker will override in subsequent code.'''
            plt.plot(self.years[-1], self.remaining_balance[-1], c=self.POSITIVE_BAL_COLOR, marker='.', markersize=FONTS['DEFAULT_FONT'][1])

            def info_box_top_left(self):
                    textstr = f'{self.remaining_balance[0]+self.withdrawals[0]:,} Initial Balance\nWithdrawal: {self.starting_withdrawal_entry.get()}%\nInflation: {self.inflation_entry.get()}%\nInterest: {self.interest_entry.get()}%'

                    ax.text(.02, .975, textstr, transform=ax.transAxes, fontsize=FONTS['DEFAULT_FONT'][1], verticalalignment='top', horizontalalignment='left', bbox=props)

            def info_box_bottom_left(self):
                    textstr = f'{self.remaining_balance[0]+self.withdrawals[0]:,} Initial Balance\nWithdrawal: {self.starting_withdrawal_entry.get()}%\nInflation: {self.inflation_entry.get()}%\nInterest: {self.interest_entry.get()}%'

                    ax.text(.02, .185, textstr, transform=ax.transAxes, fontsize=FONTS['DEFAULT_FONT'][1], verticalalignment='top', horizontalalignment='left', bbox=props)

            def final_balance_marker_red_dot(self):
                plt.plot(self.years[-1], self.remaining_balance[-1], c=self.NEGATIVE_BAL_COLOR, marker='.', markersize=FONTS['DEFAULT_FONT'][1])

            def final_balance_annotation_red_text(self):
                ax.annotate(f'Final: {self.remaining_balance[-1]:,}', (self.years[-1],self.remaining_balance[-1]), textcoords="offset points", xytext=(-20,max_label_vertical_offset), ha='center', fontsize=FONTS['DEFAULT_FONT'][1], bbox=props, c=self.NEGATIVE_BAL_COLOR) 

            def final_balance_annotation_green_text(self):
                ax.annotate(f'Final: {self.remaining_balance[-1]:,}', (self.years[-1],self.remaining_balance[-1]), textcoords="offset points", xytext=(-20,final_label_vertical_offset), ha='center', fontsize=FONTS['DEFAULT_FONT'][1], bbox=props) 

            '''if final balance and portfolio max is same, only plot marker for max'''
            if portfolio_max_value == self.remaining_balance[-1]:

                info_box_top_left(self)

            elif self.remaining_balance[-1] < 0:
                '''if final balance is negative, add a red marker and red annotized text, else green'''

                final_balance_marker_red_dot(self)
                final_balance_annotation_red_text(self)
                info_box_bottom_left(self)

            elif portfolio_max_value * .9 < self.remaining_balance[-1]:
                '''if final balance and portfolio max very close, shift final balance annotion down to avoid clipping with portfolio max annotation'''

                final_balance_annotation_green_text(self)

                info_box_top_left(self)

            else:

                ax.annotate(f'Final: {self.remaining_balance[-1]:,} in {self.years[-1]}', (self.years[-1],self.remaining_balance[-1]), textcoords="offset points", xytext=(-20,max_label_vertical_offset), ha='center', fontsize=FONTS['DEFAULT_FONT'][1], bbox=props) 

                info_box_bottom_left(self)    


            ax.grid(True)
            plt.axhline(0, color=self.NEGATIVE_BAL_COLOR, lw=2) # highlight 0 on x axis 
            '''# disable scientific notation for x,y in bottom left'''

            ax.format_coord = lambda x,y: f"$ {int(round(y,-3)):,}\n{round(x)}" 
            plt.tight_layout()
            plt.show()

        '''submit button function called'''
        clear_variables_close_plot(self)
        get_variables_from_storage(self)
        calculate_balances(self)

        self.overview_label.config(text=f'Lifetime Overview: {self.year_end-self.year_start} years')

        if self.year_end-self.year_start > 100:
            self.controller.title(f'Retirement Calculator for {random.choice(random_list)}')
        else:
            self.controller.title(f'Retirement Calculator')

        self.overview.config(state='normal')
        self.specific_year.config(state='normal')
        insert_overview_text(self)
        insert_specific_year_text(self)
        self.overview.config(state='disabled')
        self.specific_year.config(state='disabled')

        plt.close()
        if self.graph_button.get() == 1:
            create_graph(self)

    def create_submit_button(self):
        # button that calls the submit 
        sub_btn = tk.Button(self, text=' Submit ', command=self.submit)
        sub_btn.config(font=self.HEAVY_BOLD_FONT)
        sub_btn.grid(row=8, column=1, padx=(10,1), pady=(10,1), sticky='w')

        sub_btn.bind("<Enter>", self.controller.on_hover)
        sub_btn.bind("<Leave>", self.controller.on_leave)
    
    '''resets all entries to the default values'''
    def reset(self):

        self.overview.config(state='normal')
        self.specific_year.config(state='normal')

        self.starting_balance_entry.delete(0, tk.END)
        self.starting_withdrawal_entry.delete(0, tk.END)
        self.inflation_entry.delete(0, tk.END)
        self.interest_entry.delete(0, tk.END)
        self.year_start_entry.delete(0, tk.END)
        self.year_end_entry.delete(0, tk.END)

        self.starting_balance_entry.insert(
                0, "{:,}".format(self.STARTING_BALANCE))
        self.starting_withdrawal_entry.insert(0, self.WITHDRAWAL_PERCENT)
        self.inflation_entry.insert(0, self.INFLATION_PERCENT)
        self.interest_entry.insert(0, self.INTEREST_EARNED_PERCENT)
        self.year_start_entry.insert(0, self.YEAR_START)
        self.year_end_entry.insert(0, self.YEAR_END)
        self.overview.delete('1.0', tk.END)
        self.specific_year.delete('1.0', tk.END)

        self.controller.title(f'Retirement Calculator')
        self.overview_label.config(text=f'Lifetime Overview:') 

        if plt.get_fignums():
                plt.close()

        '''overview and specific year not are set to "disabled" in case reset() is called in the error checking function and an error needs to be written into the overview box. '''

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
        self.overview.tag_config('neg_bal_and_highlight', foreground=self.NEGATIVE_BAL_COLOR, background=self.ALT_HIGHLIGHT)
        self.overview.tag_config('positive_bal_color', foreground=self.POSITIVE_BAL_COLOR)
        self.overview.tag_config('positive_bal_and_highlight', foreground=self.POSITIVE_BAL_COLOR, background=self.ALT_HIGHLIGHT)
        self.overview.tag_config('highlight', background=self.ALT_HIGHLIGHT)
        self.overview.tag_config('BOLD', font='bold')
        self.overview.tag_config('positive_bal_color', foreground=self.POSITIVE_BAL_COLOR)

        '''prevent user input into the text box'''
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
        
