from news_content import *
from news_list import *

import PySimpleGUI as sg

sg.theme('Dark Blue 3')  # please make your windows colorful

file_path_input = sg.Input(key='file_path', readonly=True)
layout = [[sg.Text('List Filename')],
          [file_path_input, sg.FileBrowse()],
          [sg.Button('Read'), sg.Button('Clear'), sg.Spin([i for i in range(1, 100)], initial_value=1, key='num'),
           sg.Button('Start', visible=False),
           sg.Button('GetList')],
          [sg.Text('Content Filename')],
          [sg.Input(key='content_file_path', readonly=True), sg.FileBrowse()],
          [sg.Button('ReadContentFile'), sg.Button('DownloadContent')],
          [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progressbar')],
          [sg.Multiline('Please read csv file', size=(45, 5), auto_refresh=True, key='status_display')]]

window = sg.Window('Collect News', layout)


# with this function, it returns one list for news_link_exist and one empty df
def init_read_news(file_path):
    news_df_ = format_df()
    news_link_exist, df_exist = read_news_link_exist(file_path)
    return news_link_exist, news_df_, df_exist


# main program to cycle from 0 to 85 to get the news list with information mentioned before
def get_new_news_list_df(num, news_link_exist, news_df_):
    for i in range(num):
        html_data = return_html(str(i))
        df = parse_df(html_data)
        df_new = df[~df['link'].isin(news_link_exist)]
        news_df_ = pd.concat([news_df_, df_new], axis=0)
        sleeptime = random.randint(5, 10)
        bar_progress_int = int(1000 / num)
        window['progressbar'].update_bar(bar_progress_int * (i + 1) + 1)
        time.sleep(sleeptime)
    return news_df_


# save news content
def save_news_content(news_num, links_exist, news_detail_df_link, news_detail_df):
    for i in range(news_num, -1, -1):
        html_data = return_html_content(links_exist[i])
        df = parse_html_content(html_data, links_exist[i])
        news_detail_df_new = df[~df['link'].isin(news_detail_df_link)]
        news_detail_df = pd.concat([news_detail_df, news_detail_df_new], axis=0)
        if links_exist[i] not in news_detail_df_link:
            get_img(html_data, links_exist[i])
            window['status_display'].update('---downloading--' + links_exist[i] + '-----')
        sleeptime = random.randint(5, 10)
        window['progressbar'].update_bar(int(1000 / news_num) * (news_num - i + 1) + 2)
        time.sleep(sleeptime)
    return news_detail_df


if __name__ == '__main__':
    # initial variables
    flag = 0
    flag_content = 0
    df_exist = pd.DataFrame
    news_detail_df = pd.DataFrame
    news_df_ = format_df()
    news_link_exist = []
    num_list = 0
    num_content = 0
    links_exist = []
    news_detail_df_link = []

    while True:
        # initial the GUI
        event, values = window.read()
        # if the file path is not filled, then the textbox will display 'Please read csv file'
        if values['file_path'] == '':
            window['status_display'].update('Please read csv file')
        # Close the window
        if event == sg.WIN_CLOSED or event == 'Close':
            window.close()
            break
        # clear the file path
        if event == 'Clear':
            window.find_element('file_path')('')
            window['content_file_path'].update('')
        if values['file_path'] != '' and event == 'Read':
            # get the exist news link and empty dataframe
            news_link_exist, news_df_, df_exist = init_read_news(values['file_path'])
            # read the file path and display on the textbox
            window['status_display'].update('read ' + values['file_path'] + ' ...done')
            num_list = len(df_exist)
            flag = 100
            # for i in range(1000):
            #     time.sleep(1)
            #     window['progressbar'].update_bar(i + 10)
        if flag == 100 and event == 'GetList':
            num = values['num']
            window['status_display'].update('Loading News list...')
            news_df_ = get_new_news_list_df(num, news_link_exist, news_df_)
            num_list = len(news_df_) + len(df_exist)
            flag_content = 100
            window['status_display'].update(
                'News list download successfully\n' + "---------  " + str(len(news_df_)) + " news added---------")
            save_csv_file(news_df_, df_exist)
        elif event == 'GetList':
            window['status_display'].update('Please read csv file first')
        # if flag_content == 100 and event == 'GetContent':
        if values['content_file_path'] != '' and event == 'ReadContentFile':
            news_detail_df, news_detail_df_link = read_news_detail_df(values['content_file_path'])
            links_exist = read_existed_news_link(values['file_path'])
            num_content = len(news_detail_df)
            # read the file path and display on the textbox
            window['status_display'].update('read ' + values['content_file_path'] + ' ...done')
            flag_content = 100
            # for i in range(1000):
            #     time.sleep(1)
            #     window['progressbar'].update_bar(i + 10)
        if flag_content == 100 and event == 'DownloadContent':
            news_num = num_list - num_content
            if news_num == 0:
                sg.popup('There is no new news to be updated...')
                break
            window['status_display'].update('Loading News Content...')
            news_detail_df = save_news_content(news_num, links_exist, news_detail_df_link, news_detail_df)
            window['status_display'].update(
                'News Content download successfully\n' + '-------  ' + str(news_num) + ' news added--------')
            save_news_detail_df(news_detail_df)
        elif event == 'DownloadContent':
            window['status_display'].update('Please read csv file first')
